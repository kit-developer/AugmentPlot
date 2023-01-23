import numpy as np
import copy
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb
import cv2

from tools.common import get_size_axes, get_axes_obj, PltObjManager
from tools.colors import gradation, set_imaged_polygon


"""
    参考
    https://analytics-note.xyz/programming/matplotlib-radar-chart/
"""


plt_obj_manager = PltObjManager()


def rader(values, ticks=None, item_names=(), plt_obj=(),
          label=None, opacity=0.5, fill="grad"):

    if ticks is None:
        ticks = [0, 20, 40, 60, 80, 100]
    min_tick, max_tick = min(ticks), max(ticks)

    ax = get_axes_obj(plt_obj, polar=True)
    color_id = plt_obj_manager.set_label(ax, label)

    value_color = [c["color"] for c in plt.rcParams["axes.prop_cycle"]][color_id]
    label_color = plt.rcParams["axes.labelcolor"]
    frame_color = (np.array(to_rgb(plt.rcParams["axes.labelcolor"]))
                   + np.array(to_rgb(plt.rcParams["axes.edgecolor"]))) / 2

    # 軸本体の準備
    ax.set_rlim([min_tick, max_tick])
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    ax.axis("off")

    # 直交系軸の準備（グラデーション塗りつぶし等の用途）
    tick_range = max_tick - min_tick
    ax_xy_layer = ax.inset_axes([0, 0, 1, 1])
    ax_xy_layer.set_xlim(-tick_range, tick_range)
    ax_xy_layer.set_ylim(-tick_range, tick_range)
    ax_xy_layer.axis("off")

    values = np.array(values)
    radar_values = np.concatenate([values, [values[0]]])
    angles = np.linspace(0, 2 * np.pi, len(radar_values), endpoint=True)

    # 目盛り線（縦糸）の描画
    for i, v in enumerate(values):
        ax.plot([angles[i], angles[i]], [min_tick, max_tick], color=frame_color, linewidth=0.5)

    # 目盛り線（横糸）の描画
    for grid_value in ticks:
        grid_values = [grid_value] * (len(values) + 1)
        ax.plot(angles, grid_values, color=frame_color, linewidth=0.5)
        ax.text(x=0, y=grid_value, s=grid_value, color=label_color)

    if fill == "plane":
        ax.fill(angles, radar_values, color=value_color, alpha=0.2)

    elif fill == "grad":
        x, y = (radar_values - min_tick) * np.sin(angles), (radar_values - min_tick) * np.cos(angles)
        grad_direction = - np.arctan2(np.sum(y), np.sum(x)) / np.pi * 180 + 90
        resolution = 256
        color = to_rgb(value_color)
        grad = gradation(resolution, resolution,
                         (color[0] * 255, color[1] * 255, color[2] * 255, 255 * opacity),
                         (color[0] * 255, color[1] * 255, color[2] * 255, 0),
                         direction=grad_direction)
        set_imaged_polygon(ax_xy_layer, x=x, y=y, image=grad)
        ax_xy_layer.plot(x, y, color=value_color)

    # 値の描画
    ax.plot(angles, radar_values, color=value_color)

    # 項目名の描画
    for i, label in enumerate(item_names):
        ax.text(x=angles[i], y=(max(ticks)-min(ticks))*1.1, s=label, color=label_color,
                horizontalalignment="center", verticalalignment="center")

    return ax


def test_design():
    plt.style.use("D:\PycharmProjects\AugmentPlot\original.mplstyle")

    values = [31, 18, 96, 53, 40, 23]
    labels = [f"data{i}" for i in range(1, len(values) + 1)]
    rader(values, item_names=labels)

    values = [20, 39, 16, 63, 80, 49]
    labels = [f"data{i}" for i in range(1, len(values) + 1)]
    rader(values, item_names=labels)

    plt.show()


if __name__ == '__main__':
    test_design()

