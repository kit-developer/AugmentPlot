import matplotlib.pyplot as plt
import numpy as np
import copy

from scipy import interpolate
from matplotlib.colors import LinearSegmentedColormap

from tools.chart import meter, heatmap, bar
from tools.common import get_axes_obj, get_value


# 最新の値
def last_value_meter(**kwargs):

    axis = kwargs["axis"]
    plt_obj = kwargs["plt_obj"]

    max_min_offset = 0
    ys = [datas[-1] for datas in axis["y"]]
    max_v = [np.max(datas) * (1 + max_min_offset) for datas in axis["y"]]
    min_v = [np.min(datas) * (1 + max_min_offset) for datas in axis["y"]]
    ax = meter.multi_circle_meter(ys, plt_obj=plt_obj, max_value=max_v, min_value=min_v, activate_negative=True,
                                  gauge_width=80)

    return ax


# 最新の微分値
def last_differential_meter(**kwargs):

    axis = kwargs["axis"]
    plt_obj = kwargs["plt_obj"]
    values = kwargs["values"]

    x, y = axis["x"][0], axis["y"][0]
    dim = get_value(values, "dim", default=1)

    np_x = np.array(x)
    np_y = np.array(y)
    diff_x = np.diff(np_x)
    for i in range(dim):
        np_y = np.diff(np_y) / diff_x
        diff_x = np.array([diff_x[j] + diff_x[j+1] for j in range(len(diff_x)-1)])

    if len(np_y) < 1 or np_y[-1] == np.inf:
        ax = meter.sector_meter("N/A", plt_obj=plt_obj, shape="round")
    else:
        max_v = np.max(np_y)
        min_v = np.min(np_y)
        ax = meter.sector_meter(round(np_y[-1], 1), max_value=max_v, min_value=min_v, plt_obj=plt_obj, shape="round")
    return ax


def color_differential(**kwargs):

    axis = kwargs["axis"]
    plt_obj = kwargs["plt_obj"]
    values = kwargs["values"]

    tape_width = 3
    gap_width = 1

    xlims = get_value(values, "xlim")
    dim = get_value(values, "dim", default=2)

    img = np.zeros((gap_width, 100, 4))

    datas = [(axis["x"][i], axis["y"][i]) for i in range(len(axis["x"]))]
    for d_i, data in enumerate(datas):
        x, y = data
        np_x = np.array(x)
        np_y = np.array(y)
        diff_x = np.diff(np_x)
        for i in range(dim):
            np_y = np.diff(np_y) / diff_x
            diff_x = np.array([diff_x[j] + diff_x[j+1] for j in range(len(diff_x)-1)])
        np_y[(np_y == np.inf) | (np_y == -np.inf)] = 0
        if len(np_y) < 1:
            tape_img = np.zeros((tape_width, 100, 4))  # 細長画像
        else:
            tape_img = heatmap.color_bar_horizontal(np_x[:-dim], np_y, xlims[d_i], width=tape_width)

        img = np.append(img, tape_img, axis=0)
        img = np.append(img, np.zeros((gap_width, 100, 4)), axis=0)

    ax = get_axes_obj(plt_obj)
    ax.imshow(img, aspect='auto')

    return ax


def frequency(**kwargs):

    axis = kwargs["axis"]
    plt_obj = kwargs["plt_obj"]
    values = kwargs["values"]
    labels = kwargs["labels"]

    sampling_num = get_value(values, "sampling_num", default=10000)
    complement_way = get_value(values, "complement_way", default="linear")
    delta = get_value(values, "dt(sec)", default=1)
    bar_chart = get_value(values, "bar_chart", default=False)

    ax = get_axes_obj(plt_obj)

    datas = [(axis["x"][i], axis["y"][i]) for i in range(len(axis["x"]))]
    for d_i, data in enumerate(datas):

        cw = complement_way[d_i]
        sn = sampling_num[d_i]
        dt = delta[d_i]
        label = labels[d_i]

        x, y = data
        np_x = np.array(x)
        np_y = np.array(y)
        diff_x = np.diff(np_x)

        # xが等間隔でない場合、等間隔になるように補完
        if len(np.unique(diff_x)) > 1:
            f = interpolate.interp1d(np_x, np_y, kind=cw)
            np_x = np.linspace(np.min(np_x), np.max(np_x), sn)
            np_y = f(np_x)

        # フーリエ変換
        fourier = np.fft.fft(np_y)
        freq = np.fft.fftfreq(sn, d=dt)
        amp = np.abs(fourier / (sn / 2))

        if bar_chart:
            ax = bar.dotted_bar(freq[1:int(sn/2)], amp[1:int(sn/2)], max_y=1.0,
                                plt_obj=plt_obj, q_step=0.02)
        else:
            ax.plot(freq[1:int(sn/2)], amp[1:int(sn/2)], label=label)
            ax.legend(loc='upper right', fontsize=8)
    return ax
