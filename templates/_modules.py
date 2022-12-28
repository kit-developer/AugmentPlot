from tools.analyse_preset.plot import common as pl_common
from templates.construct_tools import _module_common as mc


def v_meter(sub_area, main_axes_info, self_info):

    # 複数データある場合の、優先順位。
    # まず、サブエリアのエリア数に対応させるものを上からチェック
    # 続いて、サブエリアの１つのグラフ内に複数表示させるものを上からチェック
    # priority = ["groups", "labels", "values/dims"]
    # module_config["values"] = {"dims": [1, 2]}

    # 枠を区切る
    sliced_areas = mc.slice_area(sub_area, area_type="vertical")

    # print("v_meter")
    # print(module_config)

    # プロパティを構成
    new_areas = mc.set_property(sliced_areas, self_info, main_axes_info,
                                func=pl_common.last_differential_meter)
                                # adjusting_element="values/dims")

    return new_areas


# これを作りながらslice_area, set_propertyの抽象化を進めていく
def x_color_bar(sub_area, main_axes_info, self_info):

    # priority = ["groups", "labels", "values/dims"]
    # module_config["iterates"] = ["xlim"]
    # module_config["values"] = {"dims": [2]}
    #
    # print("x_color_bar")
    # print(module_config)

    new_areas = mc.set_property([sub_area], self_info, main_axes_info,
                                 func=pl_common.color_differential)

    return new_areas
