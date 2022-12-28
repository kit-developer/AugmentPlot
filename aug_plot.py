import copy
from pprint import pprint
import numpy as np
import matplotlib.pyplot as plt

from tools.block_handler import block_handle
from tools.common import get_size_axes
from tools.analyse_preset.plot import common
from templates import construct


# 仕様
# 折れ線グラフ
class AugmentPlot:
    def __init__(self, figsize=(12, 7), grid=(5, 3), main_canvas=((0, 3), (0, 1)),
                 stylesheet="D:\PycharmProjects\AugmentPlot\original.mplstyle"):

        plt.style.use(stylesheet)
        self.fig = plt.figure(figsize=figsize)

        # メインキャンバスの位置を整理
        gs = self.fig.add_gridspec(grid[1], grid[0])
        main_canvas_ax = self.fig.add_subplot(gs[main_canvas[1][0]:main_canvas[1][1]+1, main_canvas[0][0]:main_canvas[0][1]+1])
        canvas_ax = self.fig.add_subplot(1, 1, 1)
        width, height, self.main_l, self.main_t = get_size_axes(main_canvas_ax)
        w, h, self.origin_l, self.origin_t = get_size_axes(canvas_ax)
        self.main_w = width / w
        self.main_h = height / h
        self.fig.delaxes(main_canvas_ax)
        self.fig.delaxes(canvas_ax)

        # サブエリアの位置をプロット
        area = np.zeros(grid, dtype="int8").T
        area[main_canvas[1][0]:main_canvas[1][1]+1, main_canvas[0][0]:main_canvas[0][1]+1] = 1
        self.main_area = area
        self.grid = grid

        self.main_axes = {}
        self.sub_axes = {}
        self.last_group = None
        self.initial_setup = True

    def add_subplot(self, rows, cols, idx, group, g_attribute=np.NAN, title_off=True,
                    projection=None):

        ax = self.fig.add_subplot(rows, cols, idx, projection=projection)
        ax = adjust_fig_size(ax, self.main_w, self.main_h, self.main_l, self.main_t, self.origin_l, self.origin_t)

        if not title_off:
            ax.set_title(group)
        self.main_axes[group] = {"ax": ax, "g_attribute": g_attribute, "labels": {}, "projection": projection}

    # 折れ線
    def plot(self, x, y, group=None, label=None, l_attribute=np.NAN):
        if group not in self.main_axes:
            if self.last_group is not None:
                group = self.last_group
            else:
                group = ""
                self.add_subplot(1, 1, 1, "")

        self.last_group = group
        ax = self.main_axes[group]["ax"]
        ax.plot(x, y, label=label)
        ax.set_title(group, loc="left", pad=0.1, size=10)

        self.main_axes[group]["labels"][label] = {
            "axis": {
                "x": x,
                "y": y,
            },
            "main_item": {
                "xlim": ax.get_xlim(),
                "ylim": ax.get_ylim(),
            },
            "l_attribute": l_attribute,
            "type": "plot"
        }

    def show(self, legend=True):
        if self.initial_setup:
            self.set_subarea()
            self.initial_setup = False
        self.update_subarea()
        if legend:
            for k, group_ax in self.main_axes.items():
                group_ax["ax"].legend()
        plt.show()

    def pause_cla(self, interval=0.01):
        if self.initial_setup:
            self.set_subarea()
            self.initial_setup = False
        self.update_subarea()
        for k, group_ax in self.main_axes.items():
            group_ax["ax"].legend(loc='upper right')
        plt.pause(interval)
        for k, group_ax in self.main_axes.items():
            group_ax["ax"].cla()
        for k, module_ax in self.sub_axes.items():
            module_ax["ax"].cla()

    def set_subarea(self):

        # custom_area = np.array([[0, 0, 0, 0, 0, 0],
        #                         [0, 0, 0, 0, 0, 0],
        #                         [0, 0, 0, 1, 0, 0]])
        custom_area = np.array([[0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0]])
        sub_area_list = block_handle(self.main_area, custom_area)

        gs = self.fig.add_gridspec(self.grid[1], self.grid[0])
        modules = construct.construct_sub_area(self.fig, gs,
                                               sub_area_list, self.main_area, custom_area, self.main_axes)
        print("\nfinally sub modules")
        pprint(modules)
        for module in modules:
            self.sub_axes[module[0]] = {
                "property": module[1]["property"],
                "title": module[1]["title"],
                "ax": module[1]["ax"]
            }

    def update_subarea(self):
        for pos, module in self.sub_axes.items():
            prop = module["property"]
            if "func" in prop and "args" in prop:
                kwargs = copy.copy(prop["args"])
                axis = {}
                for k, vs in kwargs["axis"].items():
                    axis[k] = []
                    for v in vs:
                        group_name, label_name, axis_name = v
                        axis[k].append(self.main_axes[group_name]["labels"][label_name]["axis"][axis_name])
                ax = prop["func"](axis=axis, values=kwargs["values"], plt_obj={"ax": module["ax"]})
                module["ax"] = ax
                module["ax"].set_title(module["title"], loc="left", pad=0.5, size=10)


def adjust_fig_size(ax, rate_w, rate_h, offset_rate_l, offset_rate_t, origin_l, origin_t):

    width, height, from_left, from_top = get_size_axes(ax)

    new_w = width * rate_w
    new_h = height * rate_h

    new_l = (from_left - origin_l) * rate_w + offset_rate_l
    new_t = (from_top - origin_t) * rate_h + offset_rate_t
    new_b = 1 - (new_t + new_h)

    ax.set_position([new_l, new_b, new_w, new_h])
    return ax


