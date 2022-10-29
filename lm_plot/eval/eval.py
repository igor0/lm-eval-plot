import json

from lm_plot.eval.plot import _plot_one, _plot_multi, _data

class _Eval:
    def __init__(self, df):
        self.df_ = df
    
    def to_pickle(self, path):
        self.df_.to_feather(path)

    def plot(
        self,
        x_axis,
        title_prefix=None,
        metric=None,
        legend=True,
        **axes,
    ):
        return _plot_one(
            self.df_,
            x_axis,
            title_prefix=title_prefix,
            metric=metric,
            legend=legend,
            **axes,
        )

    def plot_multi(
        self,
        multiplot_axis,
        x_axis,
        title_prefix=None,
        metric=None,
        legend=True,
        **axes,
    ):
        return _plot_multi(
            self.df_,
            multiplot_axis,
            x_axis,
            title_prefix=None,
            metric=None,
            legend=True,
            **axes,
        )

    def data(self, x_axis, title_prefix=None, metric=None, **axes):
        selected_df, _title, _display_metric, _hue = _data(
            self.df_,
            x_axis,
            title_prefix,
            metric,
            **axes
        )

        return selected_df

    def raw(self):
        return self.df_
