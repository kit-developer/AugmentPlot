from pprint import pprint


def pairing_sub_area_and_data(sub_info, main_axes_info, iterables):
    iterable_frame_is_one = all([iter_num == 1 for iter_num in iterables['iterable_frame']])
    iterable_datas_is_one = all([iter_num == 1 for iter_num in iterables['iterable_datas']])
    cannot_iterate = all([iterable_frame_is_one, iterable_datas_is_one])

    if cannot_iterate:
        check_num_priority = ["attr_num", "labels_num", "attr_tree_r", "same_attr_construction", "include_attr_construction"]
        frame_iterate_num, datas_iterate_num = 1, 1

    else:
        check_num_priority = ["same_attr_construction", "include_attr_construction", "attr_tree_r", "labels_num", "attr_num"]
        frame_iterate_num, datas_iterate_num = _check_iterate_num(
            iterables, (sub_info[1]['height'], sub_info[1]['width']))

    # print("\nmain_map")
    # print(main_axes_info[1])

    # 枠数をメイン、データ数をサブとして最適な個数をチェック
    # matched_items[検索キー][候補][frame][datas]
    matched_items = {}
    iteration = (frame_iterate_num, datas_iterate_num)
    for check_key in check_num_priority:
        check_key, items = _check_num_map(main_axes_info, check_key, iteration)
        matched_items[check_key] = items

    # print("\nmatched_items, ", iteration)
    # pprint(matched_items)

    # 最適なものを選出
    optimal_datasets = _optimal_items(matched_items, check_num_priority, iteration)

    return optimal_datasets, iteration


def _check_iterate_num(iterables, sub_areas_size):
    for i in range(2):
        if sub_areas_size[i] > 1:
            if iterables['iterable_frame'][i] != -1:
                message = "与えられたサブエリア({})に対してモジュールの繰り返し可能回数({})が足りません".format(sub_areas_size,
                                                                              iterables['iterable_frame'])
                raise ValueError(message)

    sub_area_size_h, sub_area_size_w = sub_areas_size
    frame_iterate_num = sub_area_size_h * sub_area_size_w
    datas_iterate_num = 1
    for iter_num in iterables['iterable_datas']:
        datas_iterate_num *= iter_num

    return frame_iterate_num, datas_iterate_num


def _check_num_map(main_axes_info, check_key, iteration):
    main_axes_tree, main_axes_map = main_axes_info
    frame_iterate_num, datas_iterate_num = iteration
    items = []

    if check_key == "attr_num":
        for l_attr, num in main_axes_map[check_key]["labels"].items():
            if num == frame_iterate_num:
                queries = {"l_attr": [l_attr], "g_attr": []}
                items = _search_tree(main_axes_tree["mini_tree"], items, queries)
        items, items_shape = _prefix_list_shape(items)

    elif check_key == "attr_tree_r":
        for l_attr, v in main_axes_map[check_key].items():
            for g_attr, num in v.items():
                if num == frame_iterate_num:
                    queries = {"l_attr": [l_attr], "g_attr": [g_attr]}
                    items = _search_tree(main_axes_tree["mini_tree"], items, queries)
        items, items_shape = _prefix_list_shape(items)

    elif check_key == "labels_num":
        for g_name, num in main_axes_map[check_key].items():
            if num == frame_iterate_num:
                queries = {"g_name": [g_name]}
                items = _search_tree(main_axes_tree["mini_tree"], items, queries)
        items = _reshape(items, order=(0, 2, 1)) if items != [] else []

    elif check_key == "include_attr_construction":
        for g_attr, v in main_axes_map[check_key].items():
            for l_attr_set, num in v.items():
                if num == frame_iterate_num:
                    queries = {"l_attr": list(l_attr_set), "g_attr": [g_attr]}
                    items = _search_tree(main_axes_tree["mini_tree"], items, queries)

    elif check_key == "same_attr_construction":
        for g_attr, v in main_axes_map[check_key].items():
            for l_attr_set, info in v.items():
                if info["num"] == frame_iterate_num:
                    queries = {"l_attr": list(l_attr_set), "g_attr": [g_attr], "g_name": info["group"]}
                    items = _search_tree(main_axes_tree["mini_tree"], items, queries)

    items, items_shape = _fix_list_shape_data_iteration(items, datas_iterate_num)
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
    items_shape = _list_size(items)
    if len(items_shape) > 0:
        _i = items_shape[0]
        _j = items_shape[1]
        new_items = [[[] for j in range(_j)] for i in range(_i)]
        for i, sets in enumerate(items):
            if len(sets) > 0:
                new_sets = []
                for j, groups in enumerate(sets):
                    new_sets.extend(groups)
                for j, path in enumerate(new_sets):
                    new_items[i][j] = [tuple(path)]
        items = new_items
        items_shape = _list_size(items)
    return items, items_shape


def _fix_list_shape_data_iteration(items, datas_iterate_num):
    items_shape = _list_size(items)
    if len(items_shape) > 0 and datas_iterate_num > 1:
        if items_shape[2] != datas_iterate_num and items_shape[0] == datas_iterate_num:
            items = _reshape(items, order=(2, 1, 0))
            items_shape = _list_size(items)
    return items, items_shape


def _reshape(items, order):
    items_shape = _list_size(items)
    new_items = [[[() for k in range(items_shape[order[2]])]
                  for j in range(items_shape[order[1]])]
                 for i in range(items_shape[order[0]])]
    access = [0, 0, 0]
    for i in range(items_shape[0]):
        access[order[0]] = i
        for j in range(items_shape[1]):
            access[order[1]] = j
            for k in range(items_shape[2]):
                access[order[2]] = k
                new_items[access[0]][access[1]][access[2]] = items[i][j][k]
    return new_items


def _list_size(items):
    items_shape = []
    layer = items
    for dim in range(3):
        if len(layer) > 0:
            items_shape.append(len(layer))
            layer = layer[0]
    return items_shape


def _optimal_items(matched_items, check_num_priority, iteration):
    frame_iterate_num, datas_iterate_num = iteration
    selected_key = None
    for check_iter_num in [True, False]:
        for check_key in check_num_priority:

            if len(matched_items[check_key]) != 0 and selected_key is None:
                f_iter_num = len(matched_items[check_key][0])
                d_iter_num = len(matched_items[check_key][0][0])

                if f_iter_num == frame_iterate_num:
                    if (d_iter_num == datas_iterate_num and check_iter_num) \
                            or (d_iter_num != datas_iterate_num and not check_iter_num):
                        selected_key = check_key

    optimal_datasets = matched_items[selected_key][0] if selected_key is not None else None
    return optimal_datasets
