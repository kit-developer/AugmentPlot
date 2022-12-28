import matplotlib.pyplot as plt
import numpy as np
import copy
from matplotlib.colors import LinearSegmentedColormap

from tools.chart import meter, heatmap
from tools.common import get_axes_obj, get_value


# 最新の値
def last_value_meter(axis, plt_obj, values=()):

    ys = [datas[-1] for datas in axis["y"]]
    max_v = [np.max(datas) for datas in axis["y"]]
    ax = meter.multi_circle_meter(ys, plt_obj=plt_obj, max_value=max_v)

    return ax


# 最新の微分値
def last_differential_meter(axis, plt_obj, values=()):
    x, y = axis["x"][0], axis["y"][0]
    dim = get_value(values, "dim", default=1)

    np_x = np.array(x)
    np_y = np.array(y)
    diff_x = np.diff(np_x)
    for i in range(dim):
        np_y = np.diff(np_y) / diff_x
        diff_x = np.array([diff_x[j] + diff_x[j+1] for j in range(len(diff_x)-1)])

    if len(np_y) < 1:
        ax = meter.sector_meter("N/A", plt_obj=plt_obj, shape="round")
    else:
        max_v = np.max(np_y)
        min_v = np.min(np_y)
        ax = meter.sector_meter(round(np_y[-1], 1), max_value=max_v, min_value=min_v, plt_obj=plt_obj, shape="round")
    return ax


def color_differential(axis, plt_obj, values=()):
    x, y = axis["x"][0], axis["y"][0]
    xlim = get_value(values, "xlim")[0]
    dim = get_value(values, "dim", default=2)

    np_x = np.array(x)
    np_y = np.array(y)
    diff_x = np.diff(np_x)
    for i in range(dim):
        np_y = np.diff(np_y) / diff_x
        diff_x = np.array([diff_x[j] + diff_x[j+1] for j in range(len(diff_x)-1)])

    img = heatmap.color_bar_horizontal(np_x[:-dim], np_y, xlim)

    ax = get_axes_obj(plt_obj)
    hmap = ax.imshow(img, aspect='auto')
    # ax.axis("off")

    # ax.colorbar(hmap, ax=ax)

    return ax
