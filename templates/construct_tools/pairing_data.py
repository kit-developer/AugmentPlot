import sys
from pprint import pprint

from tools.common import list_size, distorted_list_max_size


def pairing_sub_area_and_data(sub_info, main_axes_info, module_config):
    # print("pairing_sub_area_and_data sub_info", sub_info[0])
    # print(module_config)

    iterate_map, check_way_priority = _check_iterate_num(module_config, (sub_info[1]['height'], sub_info[1]['width']))

    # 枠数をメイン、データ数をサブとして最適な個数をチェック
    # matched_items[検索キー][候補][frame][datas]
    matched_items = {}
    for check_key in check_way_priority:
        items = _check_num_map(main_axes_info, check_key, iterate_map)
        matched_items[check_key] = items

    # print("matched_items")
    # pprint(matched_items)

    # 最適なものを選出
    optimal_datasets = _optimal_items(matched_items, check_way_priority, iterate_map)

    return optimal_datasets, iterate_map


def _check_iterate_num(module_config, sub_areas_size):

    conf_iter_f = module_config["iterable"]["frame"]
    conf_iter_d = module_config["iterable"]["datas"]

    iterate_prime = None
    if "priority" in conf_iter_f:
        if conf_iter_f["priority"] is not None:
            iterate_prime = "frame"
    if iterate_prime is None and "priority" in conf_iter_d:
        if conf_iter_d["priority"] is not None:
            iterate_prime = "datas"

    if iterate_prime is not None:
        check_way_priority = module_config["iterable"][iterate_prime]["priority"]
    else:
        check_way_priority = ["same_attr_construction", "include_attr_construction",
                              "attr_tree_r", "labels_num", "labels_num_same_attr", "attr_num"]

    iterable_datas_max_dim = conf_iter_d['max_dim'] if 'max_dim' in conf_iter_d else [-1, -1]
    iterable_datas_min_dim = conf_iter_d['min_dim'] if 'min_dim' in conf_iter_d else [-1, -1]

    frame_iteration = []
    for i in range(2):
        extent = module_config['extent'][i] if 'extent' in module_config else 1
        if extent == -1:
            frame_iteration.append(1)
        else:
            frame_iteration.append(sub_areas_size[i])

    fi_over_one = [(fi, fi) for fi in frame_iteration if fi > 1]
    di_over_one = [(di_min, di_max) for di_min, di_max in zip(iterable_datas_min_dim, iterable_datas_max_dim)
                   if di_max > 1 or di_max == -1]
    if not fi_over_one and di_over_one:
        iterate_prime = "datas"

    if iterate_prime is None:
        iterate_prime = "frame"

    if iterate_prime == "frame":
        prime_second_etc = fi_over_one + di_over_one + [(1, 1)]
        meta = ["frame"] * len(fi_over_one) + ["datas"] * len(di_over_one) + ["default"]
    else:
        prime_second_etc = di_over_one + [(1, 1)]
        meta = ["datas"] * len(di_over_one) + ["default"]

    if len(prime_second_etc) == 1:
        prime_second_etc = [(1, 1), (1, 1)]
        meta = ["default", "default"]

    iterate_map = {
        "check_num_priority": prime_second_etc,
        "f_height-width": frame_iteration,
        "meta": meta,
        "iterate_prime": iterate_prime
    }

    return iterate_map, check_way_priority


def _check_num_map(main_axes_info, check_key, iterate_map):
    main_axes_tree, main_axes_map = main_axes_info
    # condition = "same" if iterate_map["iterate_prime"] == "frame" else "less"
    primary_min, primary_max = iterate_map["check_num_priority"][0]
    items = []

    if check_key == "attr_num":
        for l_attr, num in main_axes_map[check_key]["labels"].items():
            if _check_iter_num(num, primary_min, primary_max):
                queries = {"l_attr": [l_attr], "g_attr": []}
                items = _search_tree(main_axes_tree["mini_tree"], items, queries)
        items, items_shape = _prefix_list_shape(items)

    elif check_key == "attr_tree_r":
        for l_attr, v in main_axes_map[check_key].items():
            for g_attr, num in v.items():
                if _check_iter_num(num, primary_min, primary_max):
                    queries = {"l_attr": [l_attr], "g_attr": [g_attr]}
                    items = _search_tree(main_axes_tree["mini_tree"], items, queries)
        items, items_shape = _prefix_list_shape(items)
        items = _select_with_secondary_num(items, iterate_map["check_num_priority"][1], iterate_map["iterate_prime"])

    elif check_key == "labels_num":
        for g_name, num in main_axes_map[check_key].items():
            if _check_iter_num(num, primary_min, primary_max):
                queries = {"g_name": [g_name]}
                items = _search_tree(main_axes_tree["mini_tree"], items, queries)

        items = _select_with_secondary_num(items, iterate_map["check_num_priority"][1], iterate_map["iterate_prime"])
        print("labels_num", list_size(items), items)
        items = _reshape(items, order=(0, 2, 1)) if items != [] else []

    elif check_key == "include_attr_construction":
        for g_attr, v in main_axes_map[check_key].items():
            for l_attr_set, num in v.items():
                if _check_iter_num(num, primary_min, primary_max):
                    queries = {"l_attr": list(l_attr_set), "g_attr": [g_attr]}
                    items = _search_tree(main_axes_tree["mini_tree"], items, queries)

    elif check_key == "same_attr_construction":
        for g_attr, v in main_axes_map[check_key].items():
            for l_attr_set, info in v.items():
                num = info["num"]
                if _check_iter_num(num, primary_min, primary_max):
                    queries = {"l_attr": list(l_attr_set), "g_attr": [g_attr], "g_name": info["group"]}
                    items = _search_tree(main_axes_tree["mini_tree"], items, queries)

    print(check_key, "__________")
    print(iterate_map["check_num_priority"])
    print("bf", list_size(items), items)
    items = _select_with_secondary_num(items, iterate_map["check_num_priority"][1], iterate_map["iterate_prime"])
    print("mi", list_size(items), items)

    try:
        items, items_shape = _fix_list_shape_data_iteration(items, iterate_map)
    except:
        raise Exception("error occurred with :" + check_key)

    print("af", list_size(items), items)

    return items


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
    items_shape = distorted_list_max_size(items)
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
                new_items[i] = [ni for ni in new_items[i] if ni != []]
        items = new_items
        items_shape = list_size(items)
    return items, items_shape


def _select_with_secondary_num(items, secondary_num, iterate_prime):
    if not items:
        return items
    secondaries = []
    data_nums_len = []

    for candidate in items:
        # items が候補、プライマリ、セカンダリで構成されるうちの、最初のプライマリに含まれるセカンダリの数を取得していく
        data_nums = [len(primaries) for primaries in candidate if len(primaries) != 0]
        data_nums_len.append(len(data_nums))
        if iterate_prime == "frame" and data_nums.count(data_nums[0]) != len(data_nums):
            raise Exception("primary_numと異なる検索結果が混じっている可能性があります。" + str(data_nums))
        secondaries.append(data_nums[0])

    if iterate_prime == "datas":
        idx = data_nums_len.index(max(data_nums_len))
    else:
        if secondary_num in secondaries:
            idx = secondaries.index(secondary_num)
        elif secondary_num == -1:
            idx = secondaries.index(max(secondaries))
        else:
            idx = 0
    items = [items[idx]]
    return items


def _fix_list_shape_data_iteration(items, iterate_map):
    items_shape = list_size(items)
    secondary_min, secondary_max = iterate_map['check_num_priority'][1]

    if len(items_shape) > 0 and secondary_max > 1:
        if not (secondary_min <= items_shape[2] <= secondary_max) \
                and (secondary_min <= items_shape[0] <= secondary_max):
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
                    try:
                        new_items[access[0]][0][access[1]][access[2]] = items[i][j][k]
                    except:
                        print("items")
                        print(i, j, k)
                        print(list_size(items))
                        pprint(items, width=200)
                        print("new_items")
                        print(access)
                        print(list_size(new_items))
                        pprint(new_items, width=200)
                        raise Exception()
    return new_items


# 各matched_itemsから、最適なものを選択する
def _optimal_items(matched_items, check_num_priority, iterate_map):

    check_num_start_dim = ["frame", "datas"].index(iterate_map['iterate_prime']) + 1
    dim_num = len(iterate_map['check_num_priority'])

    print(iterate_map['check_num_priority'])

    selected_key = None
    matched_dim = -1
    for check_key in check_num_priority:

        if len(matched_items[check_key]) != 0:
            print(check_key, matched_items[check_key])
            # shape[候補, frame, datas, datas2, ...]
            shape = list_size(matched_items[check_key])

            for i in range(dim_num):
                iter_min, iter_max = iterate_map['check_num_priority'][i]
                print(shape)
                print(check_num_start_dim, check_num_start_dim + dim_num + 1, i)
                start = check_num_start_dim
                stop = check_num_start_dim + dim_num + 1
                num = shape[start:stop][i]

                if iterate_map['meta'][i] == "frame":
                    if not (iter_min <= num <= iter_max) or i < matched_dim:
                        break
                elif iterate_map['meta'][i] == "datas":
                    if (not (iter_min <= num <= iter_max) or i < matched_dim)\
                            and iter_min != -1 and iter_max != -1:
                        break
                else:
                    if not (iter_min <= num <= iter_max) or i < matched_dim:
                        break

                matched_dim = i
                selected_key = check_key

    optimal_datasets = matched_items[selected_key][0] if selected_key is not None else None
    return optimal_datasets


def _check_iter_num(num, iter_min, iter_max):
    result = False
    if iter_min <= num <= iter_max:
        result = True
    if iter_min == -1 and num <= iter_max:
        result = True
    if iter_min <= num and iter_max == -1:
        result = True
    if iter_min == -1 and iter_max == -1:
        result = True
    return result
