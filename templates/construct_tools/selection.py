import copy
import sys
from pprint import pprint

from templates.construct_tools import divide_with_main as dwm
from templates.construct_tools import slice_area
from templates.construct_tools import pairing_data as pd
from tools.common import list_size, deep_process_list


def sub_area_selections(sub_div_unit, main_axes_info, module_info, module_priority=None):

    selections = []

    # 複数の大きさにスライスしたペアを作成
    sliced_pairs = slice_area.get_sliced_pair(sub_div_unit['original'])

    # focusとothersに割り振り
    sliced_sets = slice_area.set_focus_or_others(sliced_pairs)

    # メインとの情報を復帰する
    sliced_combinations = slice_area.restore_relation_main(sliced_sets, include_main=sub_div_unit['divided'])

    check_id = 0
    others_infos = []
    while True:
        # 各サブエリアが適用可能なモジュールのリストを作成する（ここではconfigのrequireを確認するのみ）
        focus_combination, check_id = _module_request(sliced_combinations, check_id, module_info, module_priority)
        next_action, selection_info = "", None

        # 当てはまるモジュールが存在する場合
        if focus_combination is not None:
            approved_info = focus_combination["combination"]["focus"]
            others_infos.extend(focus_combination["combination"]["others"])

            # satisfied_modulesを見ていく
            for selected_module_name, iterables in focus_combination["satisfied_modules"].items():

                # どのデータを使うか、サブエリアを分割する必要があるか、main_axes_infoを使って決定
                optimal_datasets, iteration = pd.pairing_sub_area_and_data(approved_info, main_axes_info,
                                                                           module_info[selected_module_name], iterables)

                same_construction = any([selected_module_name == s["module_name"]
                                         and optimal_datasets == s["datasets"]
                                         for s in selections])

                selection_info, next_action = _selection_info(True, sliced_combinations,
                                                              same_construction, selected_module_name,
                                                              approved_info, optimal_datasets, iteration)

                print("\nframe combination checked_____________in selection")
                print("result |", selection_info['debug_message'])
                print("detail |", selection_info['sub_info'][0],
                      "height :", selection_info['sub_info'][1]['height'],
                      "width :", selection_info['sub_info'][1]['width'])

                if next_action != "more_select_module":
                    break
        else:
            selection_info, next_action = _selection_info(False, sliced_combinations)

        if next_action == "more_module_request" or next_action == "more_select_module":
            continue
        else:
            check_id = 0

        print("\nselection_info")
        pprint(selection_info)
        print("\n-------------------------\n")

        selections.append(selection_info)

        if len(others_infos) > 0:
            # 残りのエリアを検討準備
            new_unit = others_infos.pop(0)

            sliced_pairs = slice_area.get_sliced_pair(new_unit)
            sliced_sets = slice_area.set_focus_or_others(sliced_pairs)
            sliced_combinations = slice_area.restore_relation_main(sliced_sets)
        else:
            break

    return selections


def _module_request(sliced_combinations, check_id, module_info, module_priority=None):
    for sc_i in range(check_id, len(sliced_combinations)):
        request_satisfied_modules = _check_module_request(sliced_combinations[sc_i]["focus"], module_info, module_priority)

        # sliced_sub_infoのfocusに要件を満たすモジュールがまったくない場合は次へ進む
        if len(request_satisfied_modules) > 0:
            focus_combination = {
                "combination": sliced_combinations[sc_i],
                "satisfied_modules": request_satisfied_modules
            }
            check_id = sc_i + 1
            return focus_combination, check_id
    return None, 0


def _check_module_request(sub_info, module_info, module_priority=None):

    request_satisfied_modules = {}

    if module_priority is None:
        module_priority = list(module_info.keys())

    # 適用できそうなモジュールを順番にチェックしていく
    for module_name in module_priority:

        info = module_info[module_name]

        iterable_frame = info['iterable']['frame']['max_num']
        iterable_datas = info['iterable']['datas']['max_dim']
        sub_areas_size = (sub_info[1]['height'], sub_info[1]['width'])

        feature_satisfied = all([required_feat in sub_info[1]['feature'] for required_feat in info["require"]])
        frame_size_satisfied = all([(sub_areas_size[i] > 1 and
                                     (iterable_frame[i] == -1 or iterable_frame[i] == sub_areas_size[i]))
                                    or (info['extent'][i] == -1 or sub_areas_size[i] == 1)
                                    for i in range(2)])

        if feature_satisfied and frame_size_satisfied:
            request_satisfied_modules[module_name] = {
                "iterable_frame": iterable_frame,
                "iterable_datas": iterable_datas,
            }

    return request_satisfied_modules


def _select_module(sub_info, module_info, satisfied_module):
    selected_module_info = module_info[satisfied_module]
    return satisfied_module, selected_module_info


def _selection_info(request_satisfy, sliced_combinations,
                    same_construction=None, selected_module_name=None,
                    approved_info=None, optimal_datasets=None, iteration=None):

    selection_info = {
        "sub_info": (),
        "module_name": "",
        "datasets": [],
        "iteration": (),
        "debug_message": ""
    }

    if request_satisfy:
        if not same_construction:
            if optimal_datasets is not None:
                selection_info["sub_info"] = approved_info
                selection_info["module_name"] = selected_module_name
                selection_info["datasets"] = optimal_datasets
                selection_info["iteration"] = iteration
                next_action = "check_others_sub_area"
            else:
                selection_info["debug_message"] = "no_fit_data"
                selection_info["sub_info"] = approved_info
                next_action = "more_select_module"
        else:
            # same_construction
            next_action = "more_module_request"
    else:
        selection_info["debug_message"] = "no_request_satisfied_modules"
        selection_info["sub_info"] = sliced_combinations[0]["focus"]
        next_action = "check_others_sub_area"   # 条件を満たすモジュールがないので、あきらめて次へ行く

    return selection_info, next_action


def set_property(selection, main_axes_info, module_info, fig, gs):

    sub_area = [selection['sub_info']]
    sub_area[0][1]["property"] = {
        "module": selection['module_name'],
        "func": module_info["func"],
        "args": {"axis": {}, "values": {}}
    }

    # sub_areaのスライス
    sliced_areas = _disassemble(sub_area, selection['iteration']['f_height-width'])

    main_item = module_info["arg_values"]["main_item"]
    values = module_info["arg_values"]["values"]

    # 組み合わせ候補の中を順にみていく
    for f, frame_v in enumerate(selection["datasets"]):
        sa_f_args = sliced_areas[f][1]["property"]["args"]
        layer_name_map = {}
        # 枠セットの中を順にみていく
        for data_v in frame_v:
            data_v_shape = list_size(data_v)
            if data_v_shape:
                ret = deep_process_list(data_v, leaf_action=lambda **kwargs: list(kwargs["element"]))["leaves"]
            else:
                ret = [list(data_v)]

            for d_v in ret:
                g_name, l_name = d_v[0], d_v[1]
                if g_name not in layer_name_map:
                    layer_name_map[g_name] = [l_name]
                else:
                    layer_name_map[g_name].append(l_name)

                axis = main_axes_info[0]["mini_tree"][g_name]["labels"][l_name]["axis"]     # x, y
                m_axes_item = main_axes_info[0]["main_axes"][g_name]["labels"][l_name]["main_item"]  # xlim等
                for key in axis:
                    d = list(d_v)
                    d.append(key)
                    if key not in sa_f_args["axis"]:
                        sa_f_args["axis"][key] = [d]
                        for mi in main_item:
                            sa_f_args["values"][mi] = [m_axes_item[mi]]
                        for k, v in values.items():
                            sa_f_args["values"][k] = [v]
                    else:
                        sa_f_args["axis"][key].append(d)
                        for mi in main_item:
                            sa_f_args["values"][mi].append(m_axes_item[mi])
                        for k, v in values.items():
                            sa_f_args["values"][k].append(v)

        # サブエリアの位置調整
        x1, y1, x2, y2 = dwm.get_start_and_end_sub(sliced_areas[f])
        sliced_areas[f][1]["ax"] = fig.add_subplot(gs[y1:y2 + 1, x1:x2 + 1], projection=module_info["projection"])

        title_concat = ""
        for g_name, l_names in layer_name_map.items():
            title_concat += "  " + g_name + "/ " + ", ".join(l_names)
        sliced_areas[f][1]["title"] = title_concat[1:]

    return sliced_areas


def _disassemble(sub_area, iteration):
    slice_areas = sub_area
    for i, frame_iteration in enumerate(iteration):
        if frame_iteration > 1:
            tmp = []
            for s in sub_area:
                slice_areas = slice_area.slice_to_unit(s, ["vertical", "horizontal"][i])
                tmp.extend(slice_areas)
            sub_area = tmp
    return slice_areas
