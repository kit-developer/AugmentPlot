import sys
from pprint import pprint

from tools.common import list_size


def pairing_sub_area_and_data(sub_info, main_axes_info, module_config, iterables):

    # print("pairing_sub_area_and_data sub_info", sub_info[0])
    # print(module_config)

    iterate_map, check_way_priority = _check_iterate_num(iterables, module_config,
                                                         (sub_info[1]['height'], sub_info[1]['width']))

    # 枠数をメイン、データ数をサブとして最適な個数をチェック
    # matched_items[検索キー][候補][frame][datas]
    matched_items = {}
    for check_key in check_way_priority:
        check_key, items = _check_num_map(main_axes_info, check_key, iterate_map)
        matched_items[check_key] = items

    # 最適なものを選出
    optimal_datasets = _optimal_items(matched_items, check_way_priority, iterate_map)

    return optimal_datasets, iterate_map


def _check_iterate_num(iterables, module_config, sub_areas_size):

    iterate_prime = None
    if "priority" in module_config["iterable"]["frame"]:
        if module_config["iterable"]["frame"]["priority"] is not None:
            iterate_prime = "frame"
    if iterate_prime is None and "priority" in module_config["iterable"]["datas"]:
        if module_config["iterable"]["datas"]["priority"] is not None:
            iterate_prime = "datas"

    if iterate_prime is not None:
        check_way_priority = module_config["iterable"][iterate_prime]["priority"]
    else:
        check_way_priority = ["same_attr_construction", "include_attr_construction",
                              "attr_tree_r", "labels_num", "labels_num_same_attr", "attr_num"]

    iterable_frame_max_num = module_config['iterable']['frame']['max_num']
    iterable_datas_max_dim = module_config['iterable']['datas']['max_dim']

    frame_iteration = []
    for i in range(2):
        if iterable_frame_max_num[i] == -1:
            frame_iteration.append(sub_areas_size[i])
        elif iterable_frame_max_num[i] == 1:
            frame_iteration.append(1)
        else:
            if sub_areas_size[i] <= iterable_frame_max_num[i]:
                frame_iteration.append(sub_areas_size[i])
            else:
                frame_iteration.append(1)

    fi_over_one = [fi for fi in frame_iteration if fi > 1]
    di_over_one = [di for di in iterable_datas_max_dim if di > 1 or di == -1]
    if not fi_over_one and di_over_one:
        iterate_prime = "datas"
    if iterate_prime is None:
        iterate_prime = "frame"
    if iterate_prime == "frame":
        over_one = fi_over_one + di_over_one + [1]
        meta = ["frame"] * len(fi_over_one) + ["datas"] * len(di_over_one) + ["default"]
    else:
        over_one = di_over_one + [1]
        meta = ["datas"] * len(di_over_one) + ["default"]

    if over_one == [1]:
        over_one = [1, 1]
        meta = ["default", "default"]

    iterate_map = {
        "iteration": over_one,
        "meta": meta,
        "iterate_prime": iterate_prime
    }

    return iterate_map, check_way_priority


def _check_num_map(main_axes_info, check_key, iterate_map):
    main_axes_tree, main_axes_map = main_axes_info
    condition = "same" if iterate_map["iterate_prime"] == "frame" else "less"
    primary_num = iterate_map["iteration"][0]
    items = []

    if check_key == "attr_num":
        for l_attr, num in main_axes_map[check_key]["labels"].items():
            if (num == primary_num and condition == "same")\
                    or (num <= primary_num and condition == "less")\
                    or primary_num == -1:
                queries = {"l_attr": [l_attr], "g_attr": []}
                items = _search_tree(main_axes_tree["mini_tree"], items, queries)
        items, items_shape = _prefix_list_shape(items)

    elif check_key == "attr_tree_r":
        for l_attr, v in main_axes_map[check_key].items():
            for g_attr, num in v.items():
                if (num == primary_num and condition == "same") \
                        or (num <= primary_num and condition == "less") \
                        or primary_num == -1:
                    queries = {"l_attr": [l_attr], "g_attr": [g_attr]}
                    items = _search_tree(main_axes_tree["mini_tree"], items, queries)
        items, items_shape = _prefix_list_shape(items)

    elif check_key == "labels_num":
        for g_name, num in main_axes_map[check_key].items():
            if (num == primary_num and condition == "same")\
                    or (num <= primary_num and condition == "less")\
                    or primary_num == -1:
                queries = {"g_name": [g_name]}
                items = _search_tree(main_axes_tree["mini_tree"], items, queries)
        items = _reshape(items, order=(0, 2, 1)) if items != [] else []

    elif check_key == "include_attr_construction":
        for g_attr, v in main_axes_map[check_key].items():
            for l_attr_set, num in v.items():
                if (num == primary_num and condition == "same") \
                        or (num <= primary_num and condition == "less") \
                        or primary_num == -1:
                    queries = {"l_attr": list(l_attr_set), "g_attr": [g_attr]}
                    items = _search_tree(main_axes_tree["mini_tree"], items, queries)

    elif check_key == "same_attr_construction":
        for g_attr, v in main_axes_map[check_key].items():
            for l_attr_set, info in v.items():
                num = info["num"]
                if (num == primary_num and condition == "same") \
                        or (num <= primary_num and condition == "less") \
                        or primary_num == -1:
                    queries = {"l_attr": list(l_attr_set), "g_attr": [g_attr], "g_name": info["group"]}
                    items = _search_tree(main_axes_tree["mini_tree"], items, queries)

    items, items_shape = _fix_list_shape_data_iteration(items, iterate_map)
    return check_key, items


def _search_tree(mini_tree, items, queries):
    """
    :return: items[queriesによる検索結果単位][group単位][] ?
    """
    sets = []
    for g_name, g in mini_tree.items():
        if "g_attr" in queries and g["g_attribute"] not in queries["g_attr"]:
            continue
        if "g_name" in queries and g_name not in queries["g_name"]:
            continue
        groups = []
        for l_name, l in g["labels"].items():
            if "l_attr" in queries and l["l_attribute"] not in queries["l_attr"]:
                continue
            if "l_name" in queries and l_name not in queries["l_name"]:
                continue
            groups.append((g_name, l_name))
        if groups:
            sets.append(groups)
    if sets:
        items.append(sets)
    return items


def _prefix_list_shape(items):
    items_shape = list_size(items)
    if len(items_shape) > 0:
        _i = items_shape[0]
        _j = items_shape[1]
        _k = items_shape[2]
        new_items = [[[] for j in range(_j * _k)] for i in range(_i)]
        for i, sets in enumerate(items):
            if len(sets) > 0:
                new_sets = []
                for j, groups in enumerate(sets):
                    new_sets.extend(groups)
                for j, path in enumerate(new_sets):
                    new_items[i][j] = [tuple(path)]
        items = new_items
        items_shape = list_size(items)
    return items, items_shape


def _fix_list_shape_data_iteration(items, iterate_map):

    items_shape = list_size(items)
    secondary = iterate_map['iteration'][1]

    if len(items_shape) > 0 and secondary > 1:
        if items_shape[2] != secondary and items_shape[0] == secondary:
            items = _reshape(items, order=(2, 1, 0))
            items_shape = list_size(items)

    if len(items_shape) > 0 and iterate_map['iterate_prime'] == "datas":
        items = _reshape(items, order=(0, 1, 2), prime="datas")
        items_shape = list_size(items)

    return items, items_shape


def _reshape(items, order, prime="frame"):
    items_shape = list_size(items)
    if prime == "frame":
        new_items = [[[() for k in range(items_shape[order[2]])]
                      for j in range(items_shape[order[1]])]
                     for i in range(items_shape[order[0]])]
    else:
        new_items = [[[[() for k in range(items_shape[order[2]])]
                       for j in range(items_shape[order[1]])]
                      for _ in range(1)]
                     for i in range(items_shape[order[0]])]
    access = [0, 0, 0]
    for i in range(items_shape[0]):
        access[order[0]] = i
        for j in range(items_shape[1]):
            access[order[1]] = j
            for k in range(items_shape[2]):
                access[order[2]] = k
                if prime == "frame":
                    new_items[access[0]][access[1]][access[2]] = items[i][j][k]
                else:
                    new_items[access[0]][0][access[1]][access[2]] = items[i][j][k]
    return new_items


# 各matched_itemsから、最適なものを選択する
def _optimal_items(matched_items, check_num_priority, iterate_map):

    ref = ["frame", "datas"].index(iterate_map['iterate_prime']) + 1
    dim_num = len(iterate_map['iteration'])

    print("---")

    selected_key = None
    matched_dim = -1
    for check_key in check_num_priority:

        if len(matched_items[check_key]) != 0:
            shape = list_size(matched_items[check_key])

            print(check_key, matched_dim)
            print(shape)
            print(iterate_map['iteration'])
            print(iterate_map['meta'])

            for i in range(dim_num):
                if iterate_map['meta'][i] == "frame":
                    if shape[ref:ref + dim_num + 1][i] != iterate_map['iteration'][i] or i < matched_dim:
                        break
                elif iterate_map['meta'][i] == "datas":
                    if (shape[ref:ref + dim_num + 1][i] > iterate_map['iteration'][i] or i < matched_dim) and \
                            iterate_map['iteration'][i] != -1:
                        break
                else:
                    if shape[ref:ref + dim_num + 1][i] != iterate_map['iteration'][i] or i < matched_dim:
                        break
                matched_dim = i
                selected_key = check_key

    print(selected_key)
    print("----")

    optimal_datasets = matched_items[selected_key][0] if selected_key is not None else None
    return optimal_datasets
