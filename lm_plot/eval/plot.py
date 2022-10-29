import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

DEFAULT_METRICS = ["acc", "ppl"]

def _plot_multi(
    df,
    multiplot_axis,
    x_axis,
    title_prefix=None,
    metric=None,
    legend=True,
    **axes,
):      
    col_num = 3
    plot_dim = (7, 5)
    primary_vals = args[primary_axis]
    row_num = (len(primary_vals) + (col_num - 1)) // col_num
    f = plt.figure(figsize=(plot_dim[0] * col_num, plot_dim[1] * row_num))

    gs = f.add_gridspec(row_num, col_num)

    for i in range(len(primary_vals)):
        primary_val = primary_vals[i]
        cur_args = args
        cur_args[primary_axis] = primary_val
        ax = f.add_subplot(gs[i // col_num, i % col_num])
        _plot_one(df, **args)

def _plot_one(
    df,
    x_axis,
    title_prefix=None,
    metric=None,
    legend=True,
    **axes
):
    df, title, display_metric, hue = _data(
        df,
        x_axis=x_axis,
        title_prefix=title_prefix,
        metric=metric,
        **axes
    )

    p = sns.lineplot(data=df, x=x_axis, y=display_metric, hue=hue, style=hue)
    p.set_title(title)

    return p

def _display_name(axis, value):
    return value.replace('_', ' ')

def _metric_display_name(metric):
    if metric == "acc":
        return "accuracy"
    return _display_name("metric", metric)

def _data(df, x_axis, title_prefix=None, metric=None, **axes):
    if metric is None:
        metric = _default_metric(df)
    
    axes_flat = []
    for key in axes.keys():
        if axes[key] is not None:
            axes_flat.append((key, axes[key]))
    display_metric = _metric_display_name(metric)
    
    expr = df[x_axis].notnull() & (df["metric"] == metric)
    lists = 0
    hue = None
    hue_constraint = None
    title = title_prefix
    
    for axis, constraint in axes_flat:
        if type(constraint) is not list:
            expr = expr & (df[axis] == constraint)
            
            constraint_display = _display_name(axis, constraint)
            if title is None:
                title = constraint_display
            else:
                title = title + ", " + constraint_display
        else:
            expr = expr & (df[axis].isin(constraint))
            hue = axis
            hue_constraint = constraint
            lists = lists + 1
    if lists > 1:
        raise ValueError("At most one of the axes can be a list")

    df = df[expr].rename(columns={"value": display_metric})
    if hue is not None:
        df[hue] = df[hue].astype(
            pd.CategoricalDtype(hue_constraint, ordered=True)
        )
    return df, title, display_metric, hue

def _default_metric(df):
    def_met = DEFAULT_METRICS

    metric_id = min(
        def_met.index(m) if m in def_met else len(def_met)
        for m in df["metric"]
    )

    return def_met[metric_id] if metric_id < len(def_met) else None