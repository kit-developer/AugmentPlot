import copy
from pprint import pprint


def get_main_axes_map(main_axes, mini_tree=None):

    if mini_tree is None:
        mini_tree, main_axes = get_mini_tree(main_axes)
    attr_tree_detail, attr_tree = get_attr_tree(mini_tree)

    labels_num = get_labels_num(mini_tree)
    attr_num = get_attr_num(attr_tree)
    attr_tree_r = get_attr_tree_reverse(attr_tree)
    same_l_attr_num, include_l_attr_num = get_same_l_attr(attr_tree, attr_tree_detail)

    main_axes_tree = {
        "main_axes": main_axes,
        "mini_tree": mini_tree,
        "attr_tree_detail": attr_tree_detail,
        "attr_tree": attr_tree,
    }

    main_axes_map = {
        "labels_num": labels_num,
        "attr_num": attr_num,
        "attr_tree_r": attr_tree_r,
        "same_attr_construction": same_l_attr_num,
        "include_attr_construction": include_l_attr_num
    }

    return main_axes_tree, main_axes_map


def get_mini_tree(main_axes):
    axes = {}
    for g_name, g in main_axes.items():
        axes[g_name] = g.pop("ax")

    mini_tree = copy.deepcopy(main_axes)
    for g_name, g in main_axes.items():
        main_axes[g_name]["ax"] = axes[g_name]

    for group_name, group in mini_tree.items():
        group.pop("projection")
        for label_name, label in group["labels"].items():
            label.pop("main_item")
            label.pop("type")
            label["axis"] = list(label["axis"].keys())
    return mini_tree, main_axes


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
        l_attr_set = tuple(sorted([label["l_attribute"] for label in group["labels"].values()]))
        attr_tree[g_attr].append(l_attr_set)
    return attr_tree_detail, attr_tree


def get_labels_num(mini_tree):
    labels_num = {}
    for group_name, group in mini_tree.items():
        labels_num[group_name] = len(group['labels'])
    return labels_num


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


def get_same_l_attr(attr_tree, attr_tree_detail):
    same_l_attr_num = {}
    include_l_attr_num = {}
    for g_attr, g_attr_groups in attr_tree.items():
        same = {x: {"num": g_attr_groups.count(x),
                    "group": [g_name for g_name, l_attrs, in attr_tree_detail[g_attr].items()
                              if sorted(tuple(l_attrs.keys())) == sorted(x)]}
                for x in set(g_attr_groups) if g_attr_groups.count(x) > 1}
        same_l_attr_num[g_attr] = same

        include_l_attr_num[g_attr] = {}
        for l_attrs in g_attr_groups:
            included_by_others = [
                all([l_attrs.count(l_attr) <= _l_attrs.count(l_attr) for l_attr in l_attrs])
            for _l_attrs in g_attr_groups].count(True)
            if included_by_others > 1:
                include_l_attr_num[g_attr][l_attrs] = included_by_others
    return same_l_attr_num, include_l_attr_num


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
                # 'label1-2': {
                #     'axis': ['x', 'y'],
                #     'l_attribute': 'b'},
                'label1-3': {
                    'axis': ['x', 'y'],
                    'l_attribute': 'b'}}},
        'group2': {
            'g_attribute': 'A',
            'labels': {
                'label2-1': {
                    'axis': ['x', 'y'],
                    'l_attribute': 'a'},
                'label2-2': {
                    'axis': ['x', 'y'],
                    'l_attribute': 'b'}}},
        # 'group5': {
        #     'g_attribute': 'A',
        #     'labels': {
        #         'label5-1': {
        #             'axis': ['x', 'y'],
        #             'l_attribute': 'a'},
        #         'label5-2': {
        #             'axis': ['x', 'y'],
        #             'l_attribute': 'a'}}},
        'group3': {
            'g_attribute': 'B',
            'labels': {
                'label3-1': {
                    'axis': ['x', 'y'],
                    'l_attribute': 'a'}}},
        # 'group4': {
        #     'g_attribute': 'B',
        #     'labels': {
        #         'label3-1': {
        #             'axis': ['x', 'y'],
        #             'l_attribute': 'a'}}},
    }
    return mini_tree


def get_mini_tree_sample2():
    mini_tree = {
        'group1': {
            'g_attribute': 'A',
            'labels': {
                'label1-1': {
                    'axis': ['x', 'y'],
                    'l_attribute': 'a'},
                'label1-2': {
                    'axis': ['x', 'y'],
                    'l_attribute': 'b'}}},
        'group2': {
            'g_attribute': 'A',
            'labels': {
                'label2-1': {
                    'axis': ['x', 'y'],
                    'l_attribute': 'a'},
                'label2-2': {
                    'axis': ['x', 'y'],
                    'l_attribute': 'a'}}},
        'group3': {
            'g_attribute': 'B',
            'labels': {
                'label3-1': {
                    'axis': ['x', 'y'],
                    'l_attribute': 'c'}}},
    }
    return mini_tree


def test():
    from pprint import pprint

    # main_axes = get_main_axes_sample()
    # pprint(main_axes)

    # mini_tree = get_mini_tree(main_axes)
    mini_tree = get_mini_tree_sample()

    main_axes_tree, main_axes_map = get_main_axes_map(None, mini_tree=mini_tree)

    for tree_name, tree in main_axes_tree.items():
        print("\n", tree_name)
        pprint(tree)
    print("\n\n map =================")
    for map_name, map in main_axes_map.items():
        print("\n", map_name)
        pprint(map)


if __name__ == '__main__':
    test()
