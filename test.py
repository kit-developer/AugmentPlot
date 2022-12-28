from pprint import pprint
import copy


def get_main_axes_sample():
    main_axes = {
        'cos': {
            'ax': None,
            'g_attribute': '1plot',
            'labels': {
                'cos': {
                    'axis': {
                        'x': None,
                        'y': None},
                    'l_attribute': None,
                    'lims': {
                        'xlim': (0.5, 11.5),
                        'ylim': (-1.0997584412126835, 1.0994961344169343)},
                    'type': 'plot'}},
            'projection': None},
        'cos-log': {
            'ax': None,
            'g_attribute': '2plot',
            'labels': {
                'cos': {
                    'axis': {
                        'x': None,
                        'y': None},
                    'l_attribute': 'wave',
                    'lims': {
                        'xlim': (0.5, 11.5),
                        'ylim': (-1.0997584412126835, 1.0994961344169343)},
                    'type': 'plot'},
                'log': {
                    'axis': {
                        'x': None,
                        'y': None},
                    'l_attribute': 'log',
                    'lims': {
                        'xlim': (0.5, 11.5),
                        'ylim': (-1.169676703985459, 2.56777965264522)},
                    'type': 'plot'}},
            'projection': None},
        'cos-sin': {
            'ax': None,
            'g_attribute': '2plot',
            'labels': {
                'cos': {
                    'axis': {
                        'x': None,
                        'y': None},
                    'l_attribute': 'wave',
                    'lims': {
                        'xlim': (0.5, 11.5),
                        'ylim': (-1.0997584412126835, 1.0994961344169343)},
                    'type': 'plot'},
                'sin': {
                    'axis': {
                        'x': None,
                        'y': None},
                    'l_attribute': 'wave',
                    'lims': {
                        'xlim': (0.5, 11.5),
                        'ylim': (-1.099984310877459, 1.0998859843111615)},
                    'type': 'plot'}},
            'projection': None}}
    return main_axes


def get_mini_tree_sample():
    mini_tree = {
        'group1': {
            'g_attribute': 'A',
            'labels': {
                'label1-1': {
                    'axis': ['x', 'y'],
                    'l_attribute': 'a'},
                'label1-2': {
                    'axis': ['x', 'y'],
                    'l_attribute': 'b'},
                'label1-3': {
                    'axis': ['x', 'y'],
                    'l_attribute': 'c'}}},
        'group2': {
            'g_attribute': 'A',
            'labels': {
                'label2-1': {
                    'axis': ['x', 'y'],
                    'l_attribute': 'a'},
                'label2-2': {
                    'axis': ['x', 'y'],
                    'l_attribute': 'b'}}},
        'group5': {
            'g_attribute': 'A',
            'labels': {
                'label5-1': {
                    'axis': ['x', 'y'],
                    'l_attribute': 'a'}}},
        'group3': {
            'g_attribute': 'B',
            'labels': {
                'label3-1': {
                    'axis': ['x', 'y'],
                    'l_attribute': 'a'}}},
        'group4': {
            'g_attribute': 'B',
            'labels': {
                'label3-1': {
                    'axis': ['x', 'y'],
                    'l_attribute': 'a'}}},
    }
    return mini_tree


def get_mini_tree(ma):
    main_axes = copy.deepcopy(ma)
    for group_name, group in main_axes.items():
        group.pop("ax")
        group.pop("projection")
        for label_name, label in group["labels"].items():
            label.pop("lims")
            label.pop("type")
            label["axis"] = list(label["axis"].keys())
    return main_axes


def get_attr_tree(mini_tree):
    attr_tree_detail = {}
    attr_tree = {}
    for group_name, group in mini_tree.items():
        g_attr = group["g_attribute"]
        if g_attr not in attr_tree_detail.keys():
            attr_tree_detail[g_attr] = {group_name: {}}
            attr_tree[g_attr] = []
        else:
            attr_tree_detail[g_attr].update({group_name: {}})
        for label_name, label in group["labels"].items():
            l_attr = label["l_attribute"]
            if l_attr not in attr_tree_detail[g_attr][group_name].keys():
                attr_tree_detail[g_attr][group_name][l_attr] = {label_name: label["axis"]}
            else:
                attr_tree_detail[g_attr][group_name][l_attr].update({label_name: label["axis"]})
        attr_tree[g_attr].append(tuple([label["l_attribute"] for label in group["labels"].values()]))
    return attr_tree_detail, attr_tree


def get_attr_num(attr_tree):
    attr_num = {"groups": {}, "labels": {}}
    for g_attr, g_attr_groups in attr_tree.items():
        attr_num["groups"][g_attr] = len(g_attr_groups)
        for l_attrs in g_attr_groups:
            for l_attr in l_attrs:
                if l_attr not in attr_num["labels"]:
                    attr_num["labels"][l_attr] = 1
                else:
                    attr_num["labels"][l_attr] += 1
    return attr_num


def get_attr_tree_reverse(attr_tree):
    attr_tree_reverse = {}
    for g_attr, g_attr_groups in attr_tree.items():
        for l_attrs in g_attr_groups:
            for l_attr in l_attrs:
                if l_attr not in attr_tree_reverse:
                    attr_tree_reverse[l_attr] = {g_attr: 1}
                else:
                    if g_attr not in attr_tree_reverse[l_attr]:
                        attr_tree_reverse[l_attr].update({g_attr: 1})
                    else:
                        attr_tree_reverse[l_attr][g_attr] += 1
    return attr_tree_reverse


def get_same_l_attr(attr_tree):
    same_l_attr_num = {}
    include_l_attr_num = {}
    for g_attr, g_attr_groups in attr_tree.items():
        same = {x: g_attr_groups.count(x) for x in set(g_attr_groups) if g_attr_groups.count(x) > 1}
        same_l_attr_num[g_attr] = same

        include_l_attr_num[g_attr] = {}
        for l_attrs in g_attr_groups:
            included_by_others = [
                all([l_attr in _l_attrs for l_attr in l_attrs]) for _l_attrs in g_attr_groups
            ].count(True)
            if included_by_others > 1:
                include_l_attr_num[g_attr][l_attrs] = included_by_others
    return same_l_attr_num, include_l_attr_num


# for g_attr, g_attr_groups in attr_tree.items():
#     for l_attr_tree in g_attr_groups.values():
#         for l_attr, l_attr_labels in l_attr_tree.items():


def main():
    # main_axes = get_main_axes_sample()
    # pprint(main_axes)

    # mini_tree = get_mini_tree(main_axes)
    mini_tree = get_mini_tree_sample()
    print("\nmini_tree")
    pprint(mini_tree)

    attr_tree_detail, attr_tree = get_attr_tree(mini_tree)
    print("\nattr_tree_detail")
    pprint(attr_tree_detail)
    print("attr_tree")
    pprint(attr_tree)

    print("\n\nmapping =========================")

    attr_num = get_attr_num(attr_tree)
    print("\nattr_num")
    pprint(attr_num)

    attr_tree_r = get_attr_tree_reverse(attr_tree)
    print("\nattr_tree_reverse")
    pprint(attr_tree_r)

    same_l_attr_num, include_l_attr_num = get_same_l_attr(attr_tree)
    print("\nsame_l_attr_num")
    pprint(same_l_attr_num)
    print("include_l_attr_num")
    pprint(include_l_attr_num)


if __name__ == '__main__':
    main()
