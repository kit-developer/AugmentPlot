"""
    グラデーションの棒グラフ
    https://matplotlib.org/stable/gallery/lines_bars_and_markers/gradient_bar.html

    FancyBboxPatchを使って、周波数用の棒グラフ
    https://www.yutaka-note.com/entry/matplotlib_patches#%E5%9B%9B%E8%A7%92%E5%BD%A2
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib import patches

from tools.common import get_axes_obj


def dotted_bar(x, y, max_y=100, plt_obj=(), colormap=None, w_rate=0.7, q_step=0.25, cell_h_rate=0.5, cell_r_rate=0.2):

    ax = get_axes_obj(plt_obj)

    min_x_gap = np.min(np.diff(np.array(x)))
    cell_w = min_x_gap * w_rate

    np_v = np.array([x, y])
    pos = np_v.T

    cell_round = q_step * cell_h_rate * cell_r_rate
    if cell_round > cell_w / 2:
        cell_round = cell_w / 2
    ps = _make_patches_round_box(pos, max_y, cell_w, q_step=q_step, cell_h_rate=cell_h_rate, cell_round=cell_round,
                                 colormap=colormap)
    for p in ps:
        ax.add_patch(p)
    ax.autoscale_view()
    return ax


def _make_patches_round_box(center_poses, max_y, w, q_step=0.25, cell_h_rate=0.5, cell_round=0.025, colormap=None):

    box_style = patches.BoxStyle("Round", pad=cell_round)

    if colormap is None:
        colors = [c["color"] for c in plt.rcParams["axes.prop_cycle"]][0:2][::-1]
        colormap = LinearSegmentedColormap.from_list('custom', colors)

    ps = []
    for center_pos in center_poses:

        width = w - cell_round * 2
        height = (1 - cell_h_rate) * q_step - cell_round * 2

        for n in range(int(center_pos[1] / q_step)):

            y = n * q_step + q_step / 2
            pos = [center_pos[0] - width / 2, y - height / 2]
            color = colormap(y/max_y)
            p = patches.FancyBboxPatch(pos, width, height, boxstyle=box_style, color=color)
            ps.append(p)

    return ps


def test_design():
    plt.style.use("D:\PycharmProjects\AugmentPlot\original.mplstyle")

    x = [2, 4, 6]
    y = [4, 6, 7]
    ax = dotted_bar(x, y, max_y=6)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)

    plt.show()


if __name__ == '__main__':
    test_design()
