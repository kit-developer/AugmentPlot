import copy

from templates.construct_tools import divide_with_main as dwm


def get_sliced_pair(sub_info):

    o_s_info = sub_info[1]
    o_h = o_s_info['height']
    o_w = o_s_info['width']

    if o_w > o_h:
        l_axis, s_axis = 'width', 'height'
    else:
        l_axis, s_axis = 'height', 'width'

    sliced_pairs = []

    # 長い方からみていく
    for l_i in range(o_s_info[l_axis]):
        if l_i == 0:
            sliced = _slice_area(sub_info, l_i, l_axis)
        else:
            sliced = _slice_area(sub_info, o_s_info[l_axis] - l_i, l_axis)
        sliced_pairs.append(sliced)
        s_sliced_pairs = []
        for s_i in range(1, o_s_info[s_axis]):
            for s in sliced:
                s_sliced = _slice_area(s, s_i, s_axis)
                s_sliced_pairs.append(s_sliced)
        if s_sliced_pairs:
            sliced_pairs.append(s_sliced_pairs)

    return sliced_pairs


def set_focus_or_others(sliced_pairs):
    sliced_sets = []
    for i, l_pairs in enumerate(sliced_pairs):
        sliced_set = {"focus": None, "others": []}
        if type(l_pairs[0]) != list:
            for j, l_pair in enumerate(l_pairs):
                if j == 0:
                    sliced_set["focus"] = l_pairs[j]
                else:
                    sliced_set["others"].append(l_pairs[j])
        else:
            for j, l_pair in enumerate(l_pairs):
                for k, s_pair in enumerate(l_pair):
                    if (j, k) == (0, 0):
                        sliced_set["focus"] = l_pairs[j][k]
                    else:
                        sliced_set["others"].append(l_pairs[j][k])
        sliced_sets.append(sliced_set)
    return sliced_sets


def restore_relation_main(sliced_sets, include_main=None):

    include_main_div_idx = []
    if include_main is not None:
        if len(include_main) > 0:
            main_divs = []
            for div in include_main:
                if 'fit_main_h' in div[1]['feature'] or 'fit_main_w' in div[1]['feature']:
                    main_divs.append(div)

            for i, sliced_set in enumerate(sliced_sets):
                sliced_set_list = [sliced_set['focus']]
                sliced_set_list.extend(sliced_set['others'])
                for sliced in sliced_set_list:
                    for main_div in main_divs:

                        # mainに合わせた領域がある場合
                        if main_div[0] == sliced[0] \
                        and main_div[1]['height'] == sliced[1]['height'] \
                        and main_div[1]['width'] == sliced[1]['width']:

                            sliced[1]['feature'] = main_div[1]['feature']
                            include_main_div_idx.append(i)

    sliced_combination = []
    for i in include_main_div_idx:
        sliced_combination.append(sliced_sets.pop(i))

    sliced_combination.extend(sliced_sets)

    return sliced_combination


def _slice_area(sub_info, div_pos, div_axis):

    if sub_info[1][div_axis] <= div_pos:
        raise ValueError("div_posは"+div_axis+"よりも小さい必要があります")
    if div_pos == 0:
        sub_info[1]['feature'].clear()
        sub_info[1]['feature'] = dwm.check_feature(sub_info[1]['feature'],
                                                   sub_info[1]['height'], sub_info[1]['width'])
        return [sub_info]

    new_sub_info = copy.deepcopy(sub_info)
    new_sub_info[1][div_axis] = div_pos
    new_sub_info[1]['square'] = new_sub_info[1]['height'] * new_sub_info[1]['width']
    new_sub_info[1]['feature'].clear()
    new_sub_info[1]['feature'] = dwm.check_feature(new_sub_info[1]['feature'],
                                                   new_sub_info[1]['height'], new_sub_info[1]['width'])

    div_axis_idx = ['height', 'width'].index(div_axis)
    another_sub_info = [None, {}]
    another_sub_info[1] = copy.deepcopy(sub_info[1])
    another_sub_position = list(new_sub_info[0])
    another_sub_position[div_axis_idx] = new_sub_info[0][div_axis_idx] + div_pos
    another_sub_info[0] = tuple(another_sub_position)
    another_sub_info[1][div_axis] = sub_info[1][div_axis] - new_sub_info[1][div_axis]
    another_sub_info[1]['square'] = another_sub_info[1]['height'] * another_sub_info[1]['width']
    another_sub_info[1]['feature'].clear()
    another_sub_info[1]['feature'] = dwm.check_feature(another_sub_info[1]['feature'],
                                                       another_sub_info[1]['height'], another_sub_info[1]['width'])

    sliced = [new_sub_info, tuple(another_sub_info)]
    return sliced


# 縦に長い（横に切る）場合はarea_type="vertical"
def slice_to_unit(sub_area, area_type):
    if area_type == "vertical":
        l, s, h, w = "height", "width", 1, 0
    elif area_type == "horizontal":
        l, s, h, w = "width", "height", 0, 1
    else:
        raise ValueError("area_type is not either vertical and horizontal : " + str(area_type))

    new_areas = []
    for i in range(sub_area[1][l]):
        pos = (sub_area[0][0] + h * i, sub_area[0][1] + w * i)
        cfg = copy.deepcopy(sub_area[1])
        cfg[l] = 1
        cfg["square"] = 1 * sub_area[1][s]
        new_areas.append((pos, cfg))

    return new_areas
