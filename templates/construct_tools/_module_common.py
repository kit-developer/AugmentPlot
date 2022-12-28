from pprint import pprint
import copy
import sys
import numpy as np


# 縦に長い（横に切る）場合はarea_type="vertical"
def slice_area(sub_area, area_type):
    if area_type == "vertical":
        l, s, h, w = "height", "width", 1, 0
    elif area_type == "horizontal":
        l, s, h, w = "width", "height", 0, 1
    else:
        raise ValueError("area_type is not either vertical and horizontal : " + str(area_type))

    new_area = []
    for i in range(sub_area[1][l]):
        pos = (sub_area[0][0] + h * i, sub_area[0][1] + w * i)
        cfg = copy.deepcopy(sub_area[1])
        cfg[l] = 1
        cfg["square"] = 1 * sub_area[1][s]
        new_area.append((pos, cfg))

    return new_area


def set_property(sliced_areas, module_info, main_axes_info, func):

    main_axes_tree, main_axes_map = main_axes_info
    # elements, module_config = _create_module_config(main_axes_tree["main_axes"])

    # print("\n", "main_axes_tree")
    # pprint(main_axes_tree)
    # print("\n", "main_axes_map")
    # pprint(main_axes_map)

    print("\n", "sliced_areas")
    pprint(sliced_areas)

    shape_map = _get_shape_sliced_areas(sliced_areas)
    _confirm_use_data(module_info, main_axes_info, shape_map)


    sys.exit(0)

    for i, sliced_area in enumerate(sliced_areas):
        sliced_area[1]["property"] = {"func": func, "args": args}


def _get_shape_sliced_areas(sliced_areas):
    places = [sliced_area[0] for sliced_area in sliced_areas]
    origin = np.array((min([place[0] for place in places]), min([place[1] for place in places])))
    size = tuple(np.array((max([place[0] for place in places]), max([place[1] for place in places]))) - origin)
    shape_map = [[None for x in range(size[1] + 1)] for y in range(size[0] + 1)]
    for y, row in enumerate(shape_map):
        for x, value in enumerate(row):
            shape_map[y][x] = tuple(origin + np.array((y, x)))
    return shape_map


def _confirm_use_data(module_info, main_axes_info, shape_map):

    main_axes_tree, main_axes_map = main_axes_info

    # print("\n\n", "module_info")
    # pprint(module_info)

    # コンフィグのframe_max_numの値チェック（datas_max_dimのチェックは未実装）
    iterable_frame = _check_frame_num(module_info, shape_map)
    iterable_datas = module_info["iterable"]["datas_max_dim"]
    # iterable_frame = module_info["iterable"]["frame_max_num"]

    print("\n\n", "shape")
    print(shape_map)
    print("iterable_datas: ", iterable_datas, "iterable_frame: ", iterable_frame)

    print("\n", "main_axes_map")
    pprint(main_axes_map)



def _check_frame_num(module_info, sub_areas_shape_map):

    sub_areas_h = len(sub_areas_shape_map)
    sub_areas_w = len(sub_areas_shape_map[0])
    sub_areas_size = (sub_areas_h, sub_areas_w)
    module_iterable_size = module_info["iterable"]["frame_max_num"]

    for i in range(2):
        if sub_areas_size[i] > 1:
            if module_iterable_size[i] != -1:
                raise ValueError("与えられたサブエリアに対してモジュールの繰り返し可能回数が足りません")
        # if sub_areas_size[i] == 1:
        #     if module_iterable_size[i] != 1:
        #         raise ValueError("与えられたサブエリアに対してモジュールの繰り返し可能回数が多すぎます")

    return sub_areas_size










# 以下、過去のもの

def _set_property(sliced_area, module_info, main_axes_info, func, adjusting_element):

    new_areas = sliced_area

    elements, module_config = _create_module_config(main_axes)

    # 枠とデータ数を使って、つじつま合わせ
    iterate, l_elements = _grouping_element(elements, area_num, adjusting_element)

    # 要素の優先度を構成
    elements_priority = {e["name"]: i for i, e in enumerate(elements)}
    id_g = elements_priority["groups"]
    groups = elements[id_g]["layer"]
    id_l = elements_priority["labels"]
    labels = elements[id_l]["layer"]

    for i, na in enumerate(new_areas):
        args = {"axis": {}, "values": {}}
        multi_data = False
        for l_i, l in enumerate(l_elements):

            # グループやラベルに複数（枠数と同数でない）データがある場合
            if l > 1:
                multi_data = True
                for j in range(l):
                    for axis in module_config["axis"]:
                        key = axis+"-"+str(j)
                        if elements[l_i]["name"] == "groups":
                            args["axis"][key] = [groups[j], labels[iterate[id_l] * i], axis]
                        elif elements[l_i]["name"] == "labels":
                            args["axis"][key] = [groups[iterate[id_g] * i], labels[j], axis]

                    if "iterates" in module_config:
                        for ite in module_config["iterates"]:
                            key = ite + "-" + str(j)
                            if elements[l_i]["name"] == "groups":
                                args["values"][key] = [groups[j], labels[iterate[id_l] * i], ite]
                            elif elements[l_i]["name"] == "labels":
                                args["values"][key] = [groups[iterate[id_g] * i], labels[j], ite]
                break

        # グループやラベルに複数（枠数と同数でない）データがない場合
        if not multi_data:
            for axis in module_config["axis"]:
                args["axis"][axis] = [groups[iterate[id_g] * i], labels[iterate[id_l] * i], axis]
            if "iterates" in module_config:
                for ite in module_config["iterates"]:
                    args["values"][ite] = [groups[iterate[id_g] * i], labels[iterate[id_l] * i], ite]

        # グループやラベル以外の要素を引数に構成
        # id_val = elements_priority["dim"]
        # args["values"]["dim"] = elements[id_val]["layer"][iterate[id_val] * i]
        id_vals = [(elements_priority[k], k) for k in priority if k != "groups" and k != "labels"]
        for id_val, key in id_vals:
            args["values"][key] = elements[id_val]["layer"][iterate[id_val] * i]

        na[1]["property"] = {"func": func, "args": args}

    return new_areas


def _create_module_config(main_axes):

    axes_map = _get_main_axes_map(main_axes)

    print("\n\nmain_axes_map")
    pprint(axes_map)

    # sys.exit(0)
    # module_configs = line_chart_configs
    module_priority = ["v_meter", "x_color_bar"]

    module_configs = []
    for module_name in module_priority:
        module_config = (module_name, {})
        module_config[1]["groups"] = axes_map["group_names"]
        module_config[1]["labels"] = axes_map["label_names"]
        module_config[1]["axis"] = axes_map["axis_names"]
        module_config[1]["iterates"] = []
        module_config[1]["values"] = {}
        module_configs.append(module_config)

    elements = []
    for p in priority:
        m = copy.deepcopy(module_config)
        for k in p.split('/'):
            m = m[k]
        elements.append({"name": p, "layer": m})

    return elements, module_configs


def _grouping_element(elements, area_num, adjusting_element=None):

    iterate = np.zeros(len(elements), dtype=np.int32)

    # 与えられているそれぞれの要素数
    l_elements = [len(element["layer"]) for element in elements]
    adj_element_id = [i for i, e in enumerate(elements) if e["name"] == adjusting_element]

    if len(adj_element_id) != 1 and not (area_num == 1 and adjusting_element is None):
        raise ValueError("adjusting_element is invalid : " + str(adjusting_element))
    else:
        adj_element_id = adj_element_id[0]

    # メーターの数と、グラフの数やグラフエリアの数を比較する。
    # 一致しているものがなければ、adjusting_elementで数を揃える。
    if area_num in l_elements:
        ite_element_id = l_elements.index(area_num)
        iterate[ite_element_id] = 1
        l_elements[ite_element_id] = -1
        l_elements[adj_element_id] = -1
    elif adjusting_element is not None:
        iterate[adj_element_id] = 1
        l_elements[adj_element_id] = -1
    else:
        raise ValueError("adjusting_element is needed")

    return iterate, l_elements

