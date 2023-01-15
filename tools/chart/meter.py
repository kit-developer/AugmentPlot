import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

from tools.common import get_center_axes, get_axes_obj


def multi_circle_meter(values, max_value=None, min_value=None, plt_obj=(),
                       colormap=None, gauge_width=100, activate_negative=False,
                       text_color="gray", text_size=40, font_family="sans-serif", font_weight="normal"):

    if max_value is None:
        max_value = 1
    if min_value is None:
        min_value = -1

    rates = []
    for i in range(len(values)):
        if hasattr(max_value, "__iter__"):
            max_v = max_value[i]
            min_v = min_value[i]
        else:
            max_v = max_value
            min_v = min_value
        if activate_negative:
            max_v = max_v if values[i] >= 0 else - min_v
            min_v = 0
        rate = (values[i] - min_v) / (max_v - min_v) if max_v - min_v != 0 else np.finfo(np.float32).eps
        rates.append(rate)

    norm = mpl.colors.Normalize(0, 2 * np.pi)
    ax, colormap = build_meter("", colormap, plt_obj, False,
                               text_color, text_size, font_family, font_weight)

    # インジケーターを作成
    for i, rate in enumerate(rates):
        pn = rate / abs(rate)
        if activate_negative:
            circle_len = 1 * np.pi
            c_rate = rate / 2 + 0.5
            cval = np.arange(0.5 * 2 * np.pi, c_rate * 2 * np.pi, 0.01 * pn)
        else:
            circle_len = 2 * np.pi
            cval = np.arange(0, rate * 2 * np.pi, 0.01 * pn)
        xval = np.arange(0, rate * circle_len, 0.01 * rate / abs(rate))
        yval = np.full_like(xval, 1 + i / len(rates) * 0.7)
        ax.scatter(xval, yval, c=cval, s=gauge_width, cmap=colormap, norm=norm, linewidths=0)

    ax.set_yticks([])
    ax.set_ylim(0, 2)
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)

    return ax


def sector_meter(value, max_value=100, min_value=0, plt_obj=(), angle=200, colormap=None, gauge_width=1, shape="solid",
                 text_color="gray", text_size=40, font_family="sans-serif", font_weight="normal"):

    norm = mpl.colors.Normalize(0, 2 * np.pi)
    ax, colormap = build_meter(value, colormap, plt_obj, True,
                               text_color, text_size, font_family, font_weight)

    rate = (value - min_value) / (max_value - min_value)\
        if type(value) != str and max_value - min_value != 0 else 0

    if shape == "round":
        xval = np.arange(0, rate * 2 * np.pi * angle / 360, 0.01)
        yval = np.ones_like(xval)
        bg_xval = np.arange(0, 2 * np.pi * angle / 360, 0.01)
        bg_yval = np.ones_like(bg_xval)
        ax.scatter(bg_xval, bg_yval, s=gauge_width*100/4, color="#CCCCCC", norm=norm, linewidths=0)
        ax.scatter(xval, yval, c=xval, s=gauge_width*100, cmap=colormap, norm=norm, linewidths=0)
    else:
        ax.barh(1, 2 * np.pi * angle / 360, color="#CCCCCC", height=gauge_width)
        ax.barh(1, rate * 2 * np.pi * angle / 360, color=colormap(rate), height=gauge_width)

    ax.set_yticks([])
    ax.set_ylim(-3, 3)

    ax.set_theta_zero_location(loc="N", offset=angle/2)
    ax.set_theta_direction(-1)

    return ax


def build_meter(value, colormap, plt_obj=(), set_text=True,
                text_color="gray", text_size=40, font_family="sans-serif", font_weight="normal"):

    ax = get_axes_obj(plt_obj, polar=True)
    ax.axis("off")

    if set_text:
        text = str(value)
        text_x, text_y = get_center_axes(ax)
        ax.text(text_x, text_y, text, size=text_size,
                color=text_color,
                horizontalalignment="center",
                verticalalignment="center",
                fontfamily=font_family,
                fontweight=font_weight,
                transform=plt.gcf().transFigure)

    if colormap is None:
        colors = [c["color"] for c in plt.rcParams["axes.prop_cycle"]][0:2]
        colormap = LinearSegmentedColormap.from_list('custom', colors)

    return ax, colormap


def test_design():
    plt.style.use("D:\PycharmProjects\AugmentPlot\original.mplstyle")
    value = [30, 60, 40]
    multi_circle_meter(value, max_value=100)
    # sector_meter(round(value, 1), max_value=100, min_value=0, shape="solid")
    plt.show()


if __name__ == '__main__':
    test_design()
