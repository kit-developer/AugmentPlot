import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, to_rgb
from matplotlib import patches
from matplotlib.patches import Polygon
from matplotlib.artist import _XYPair

from tools.common import get_center_axes, get_axes_obj


plt_obj_manager = {}


def plot_gradation(x, y, plt_obj=(), label=None):

    ax = get_axes_obj(plt_obj)

    ax_id = id(ax)
    if ax_id not in plt_obj_manager:
        plt_obj_manager[ax_id] = [label]
    else:
        plt_obj_manager[ax_id].append(label)
    color_id = plt_obj_manager[ax_id].index(label)

    color = [c["color"] for c in plt.rcParams["axes.prop_cycle"]][color_id]
    opacity = 0.25
    color = to_rgb(color)

    np_x = np.array(x)
    np_y = np.array(y)
    min_x, max_x = np.min(np_x), np.max(np_x)
    min_y, max_y = np.min(np_y), np.max(np_y)
    np_x = np.insert(np_x, [0, len(np_x)], [np_x[0], np_x[-1]])
    np_y = np.insert(np_y, [0, len(np_y)], [min_y, min_y])

    np_v = np.array([np_x, np_y])
    pos = np_v.T

    resolution = 256
    frame = np.zeros((resolution, 4))
    for i in range(resolution):
        alpha = i * opacity / resolution
        frame[i] = (color[0], color[1], color[2], alpha)
    grad = np.array(frame).reshape((-1, 1, 4))[::-1]

    ax.autoscale(False)
    img = ax.imshow(grad, extent=[min_x, max_x, min_y, max_y], aspect='auto')
    img._sticky_edges = _XYPair([], [])

    polygon = Polygon(pos, closed=True, facecolor='none', edgecolor='none')
    ax.add_patch(polygon)
    img.set_clip_path(polygon)

    ax.autoscale(True)
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
