# import copy
# import numpy as np
# from pprint import pprint
#
# import divide_with_main as dwm
#
#
# def _get_main_axes_map(main_axes):
#     group_num = len(main_axes)
#     group_attr_num = 0
#     group_attr_each_num = {}
#     label_map = {}
#
#     group_names = []
#     label_names = []
#     axis_names = []
#
#     # map 作成
#     for g_name, group in main_axes.items():
#
#         # group map 作成
#         g_attr_name = group['g_attribute']
#         group_names.append(g_name)
#         if g_attr_name is not None:
#             if g_attr_name in group_attr_each_num:
#                 group_attr_each_num[g_attr_name] += 1
#             else:
#                 group_attr_num += 1
#                 group_attr_each_num[g_attr_name] = 1
#
#         # label map 作成
#         label_num = len(group['labels'])
#         label_attr_num = 0
#         label_attr_each_num = {}
#
#         for l_name, label in group['labels'].items():
#             l_attr_name = label['l_attribute']
#             label_names.append(l_name)
#             axis_names.extend(list(label['axis'].keys()))
#             if l_attr_name is not None:
#                 if l_attr_name in label_attr_each_num:
#                     label_attr_each_num[l_attr_name] += 1
#                 else:
#                     label_attr_num += 1
#                     label_attr_each_num[l_attr_name] = 1
#             label_map[g_name] = {
#                 "label_num": label_num,
#                 "label_attr_num": label_attr_num,
#                 "label_attr_each_num": label_attr_each_num,
#             }
#
#     axes_map = {
#         "group_num": group_num,
#         "group_attr_num": group_attr_num,
#         "group_attr_each_num": group_attr_each_num,
#         "group_names": group_names,
#         "label_names": list(set(label_names)),
#         "axis_names": list(set(axis_names)),
#         "label": label_map,
#     }
#
#     return axes_map


