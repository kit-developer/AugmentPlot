import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb

from tools.common import get_axes_obj, PltObjManager
from tools.colors import gradation, set_imaged_polygon


plt_obj_manager = PltObjManager()


def plot_gradation(x, y, plt_obj=(), label=None, opacity=0.25):

    ax = get_axes_obj(plt_obj)
    color_id = plt_obj_manager.set_label(ax, label)

    color = [c["color"] for c in plt.rcParams["axes.prop_cycle"]][color_id]
    color = to_rgb(color)

    np_x = np.array(x)
    np_y = np.array(y)

    resolution = 256
    grad = gradation(resolution, resolution,
                     (color[0]*255, color[1]*255, color[2]*255, 255*opacity),
                     (color[0]*255, color[1]*255, color[2]*255, 0))

    np_x = np.insert(np_x, [0, len(np_x)], [np_x[0], np_x[-1]])
    np_y = np.insert(np_y, [0, len(np_y)], [np.min(np_y), np.min(np_y)])
    set_imaged_polygon(ax, np_x, np_y, grad, aspect='auto')

    ax.plot(x, y, color=color, label=label)
    return ax


def test_design():
    plt.style.use("D:\PycharmProjects\AugmentPlot\original.mplstyle")

    x = [2, 4, 6]
    y = [4, 6, 7]
    ax = plot_gradation(x, y)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)

    plt.show()


if __name__ == '__main__':
    test_design()
