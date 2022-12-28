
def get_sub_div_info(sub_area_list, main_area):
    main_area_info = get_start_and_end_main(main_area)
    sub_div_info = []
    for sub_area in sub_area_list:
        divided_sub_areas = divide_sub_by_main(sub_area, main_area_info)

        included_feature = []
        for d_sub_area in divided_sub_areas:
            included_feature.extend(d_sub_area[1]['feature'])

        sub_area_info = get_start_and_end_sub(sub_area)
        relative = relative_position(main_area_info, sub_area_info)
        if relative in ["left", "right"]:
            original_feature = ["main_" + relative]
            if sub_area_info[1] == main_area_info[1] and sub_area_info[3] == main_area_info[3]:
                original_feature.append("fit_main_h")
        elif relative in ["upper", "bottom"]:
            original_feature = ["main_" + relative]
            if sub_area_info[0] == main_area_info[0] and sub_area_info[2] == main_area_info[2]:
                original_feature.append("fit_main_w")
        else:
            original_feature = []
        sub_area[1]['feature'] = check_feature(original_feature, sub_area[1]['height'], sub_area[1]['width'])

        info = {
            "original": sub_area,
            "divided": divided_sub_areas,
            "included_feature": list(set(included_feature))
        }
        sub_div_info.append(info)

    return sub_div_info


def divide_sub_by_main(sub_area, main_area_info):

    sub_area_info = get_start_and_end_sub(sub_area)
    relative = relative_position(main_area_info, sub_area_info)

    new_area = []
    if relative in ["left", "right"]:
        new_area = _h_divide_sub_by_main(new_area, main_area_info, sub_area_info, relative)
    elif relative in ["upper", "bottom"]:
        new_area = _v_divide_sub_by_main(new_area, main_area_info, sub_area_info, relative)

    return new_area


def get_start_and_end_main(main_area):

    x_start = 0
    y_start = 0
    x_end = 0
    y_end = 0

    y_tmp = 0
    for i, row in enumerate(main_area):
        c_tmp = 0
        for j, value in enumerate(row):
            if value == 1 and c_tmp == 0:
                x_start = j
            elif value == 0 and c_tmp == 1:
                if x_end < j - 1:
                    x_end = j - 1
            c_tmp = value
        if 1 in row and y_tmp == 0:
            y_start = i
        elif 1 not in row and y_tmp == 1:
            if y_end < i - 1:
                y_end = i - 1
        y_tmp = 1 if 1 in row else 0

    return x_start, y_start, x_end, y_end


def get_start_and_end_sub(sub_area):
    pos = sub_area[0]
    w = sub_area[1]['width']
    h = sub_area[1]['height']
    sub_area_info = (pos[1], pos[0], pos[1] + w - 1, pos[0] + h - 1)
    return sub_area_info


def relative_position(main_area_info, sub_area_info):
    main_left, main_upper, main_right, main_bottom = main_area_info
    sub_left, sub_upper, sub_right, sub_bottom = sub_area_info

    relative = None

    # メインエリアの左側に位置する
    if sub_right < main_left and \
            sub_upper <= main_upper and sub_bottom >= main_bottom:
        relative = "left"

    # メインエリアの右側に位置する
    if sub_left > main_right and \
            sub_upper <= main_upper and sub_bottom >= main_bottom:
        relative = "right"

    # メインエリアの上側に位置する
    if sub_bottom < main_upper and \
            sub_left <= main_left and sub_right >= main_right:
        relative = "upper"

    # メインエリアの下側に位置する
    if sub_upper > main_bottom and \
            sub_left <= main_left and sub_right >= main_right:
        relative = "bottom"

    return relative


# サブエリアを縦に分割
def _v_divide_sub_by_main(new_area, main_area_info, sub_area_info, pos_name):
    main_left, main_upper, main_right, main_bottom = main_area_info
    sub_left, sub_upper, sub_right, sub_bottom = sub_area_info

    tmp_pos = (sub_upper, main_left)
    tmp_h = sub_bottom - sub_upper + 1
    tmp_w = main_right - main_left + 1

    feature = ['main_' + pos_name, 'fit_main_w']
    feature = check_feature(feature, tmp_h, tmp_w)

    new_area.append((tmp_pos, {
        'height': tmp_h,
        'square': tmp_h * tmp_w,
        'width': tmp_w,
        'feature': feature
    }))

    # サブエリアの左に余りがある場合
    if main_left - sub_left > 0:
        tmp_pos = (sub_upper, sub_left)
        tmp_w = main_left - sub_left

        feature = []
        feature = check_feature(feature, tmp_h, tmp_w)

        new_area.append((tmp_pos, {
            'height': tmp_h,
            'square': tmp_h * tmp_w,
            'width': tmp_w,
            'feature': feature
        }))

    # サブエリアの右に余りがある場合
    if sub_right - main_right > 0:
        tmp_pos = (sub_upper, main_right + 1)
        tmp_w = sub_right - main_right

        feature = []
        feature = check_feature(feature, tmp_h, tmp_w)

        new_area.append((tmp_pos, {
            'height': tmp_h,
            'square': tmp_h * tmp_w,
            'width': tmp_w,
            'feature': feature
        }))

    return new_area


# サブエリアを横に分割
def _h_divide_sub_by_main(new_area, main_area_info, sub_area_info, pos_name):
    main_left, main_upper, main_right, main_bottom = main_area_info
    sub_left, sub_upper, sub_right, sub_bottom = sub_area_info

    tmp_pos = (main_upper, sub_left)
    tmp_h = main_bottom - main_upper + 1
    tmp_w = sub_right - sub_left + 1

    feature = ['main_' + pos_name, 'fit_main_h']
    feature = check_feature(feature, tmp_h, tmp_w)

    new_area.append((tmp_pos, {
        'height': tmp_h,
        'square': tmp_h * tmp_w,
        'width': tmp_w,
        'feature': feature
    }))

    # サブエリアの上に余りがある場合
    if main_upper - sub_upper > 0:
        tmp_pos = (sub_upper, sub_left)
        tmp_h = main_upper - sub_upper

        feature = []
        feature = check_feature(feature, tmp_h, tmp_w)

        new_area.append((tmp_pos, {
            'height': tmp_h,
            'square': tmp_h * tmp_w,
            'width': tmp_w,
            'feature': feature
        }))

    # サブエリアの下に余りがある場合
    if sub_bottom - main_bottom > 0:
        tmp_pos = (main_bottom + 1, sub_left)
        tmp_h = sub_bottom - main_bottom

        feature = []
        feature = check_feature(feature, tmp_h, tmp_w)

        new_area.append((tmp_pos, {
            'height': tmp_h,
            'square': tmp_h * tmp_w,
            'width': tmp_w,
            'feature': feature
        }))

    return new_area


def check_feature(feature, h, w):
    if h > w:
        feature.append("vertical")
    elif w > h:
        feature.append("horizontal")
    else:
        feature.append("square")

    if h > 1:
        feature.append("tall")
    if w > 1:
        feature.append("wide")

    return feature
