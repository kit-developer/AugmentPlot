import copy
from pprint import pprint
import numpy as np
np.set_printoptions(threshold=99, edgeitems=1)

from templates.construct_tools import divide_with_main as dwm
from templates.construct_tools import selection as sel
from templates.construct_tools import main_axes_map as mam
from templates.modules_config import module_info, module_priority


def construct_sub_area(fig, gs, sub_area_list, main_area, custom_area, main_axes):

    # メインエリアのグラフ属性などの情報をまとめる
    main_axes_tree, main_axes_map = mam.get_main_axes_map(main_axes)
    main_axes_info = (main_axes_tree, main_axes_map)

    # サブエリアをメインエリアの大きさに合わせて分割
    sub_div_info = dwm.get_sub_div_info(copy.deepcopy(sub_area_list), main_area)
    # pprint(sub_div_info)

    # サブエリアを構成
    modules = _confirming_sub_modules(fig, gs, main_axes_info, sub_div_info, module_info, module_priority)

    # カスタムエリアを構成

    return modules


def _confirming_sub_modules(fig, gs, main_axes_info, sub_div_info, module_info, module_priority):

    selections = []
    for sub_div_unit in sub_div_info:
        selections.extend(sel.sub_area_selections(sub_div_unit, main_axes_info, module_info, module_priority))

    sub_areas = []
    for selection in selections:
        if selection["module_name"] == '':
            continue
        # プロパティを構成
        sliced_areas = sel.set_property(selection, main_axes_info, module_info[selection["module_name"]], fig, gs)
        sub_areas.extend(sliced_areas)

    return sub_areas
