from pprint import pprint
from matplotlib import pyplot as plt


def ax_title(ax, title, color, h_offset=0):
    width, height, from_left, from_top = get_size_axes(ax)
    h_ofs = (h_offset + 0.01) / height
    ax.text(0, 1 + h_ofs, title, color=color, ha='left', transform=ax.transAxes, fontsize=10)


def ax_subtitle(ax, title, color, h_offset=0):
    width, height, from_left, from_top = get_size_axes(ax)
    h_ofs = (h_offset - 0.01) / height
    ax.text(0, 1 + h_ofs, title, color=color, ha='left', transform=ax.transAxes, fontsize=8)


def get_size_axes(ax):
    width = abs(ax.get_position().x1 - ax.get_position().x0)
    height = abs(ax.get_position().y1 - ax.get_position().y0)
    from_left = ax.get_position().x0
    from_top = 1 - ax.get_position().y1

    return width, height, from_left, from_top


def get_center_axes(ax):
    width = abs(ax.get_position().x1 - ax.get_position().x0)
    height = abs(ax.get_position().y1 - ax.get_position().y0)

    x = ax.get_position().x0 + width / 2
    y = ax.get_position().y0 + height / 2

    return x, y


def get_value(values, key, default="NULL DEFAULT"):
    if key in values:
        value = values[key]
    elif default == "NULL DEFAULT":
        raise ValueError("Need to input value :" + str(key))
    else:
        value = default

    return value


def get_axes_obj(plt_obj, polar=False):
    projection = None
    if polar:
        projection = "polar"

    if "ax" in plt_obj:
        ax = plt_obj["ax"]
    else:
        if "fig" in plt_obj and "gs" in plt_obj:
            ax = plt_obj["fig"].add_subplot(plt_obj["gs"], projection=projection)
        elif "fig" in plt_obj:
            ax = plt_obj["fig"].add_subplot(1, 1, 1, projection=projection)
        else:
            ax = plt.subplot(1, 1, 1, polar=polar)

    return ax


class PltObjManager:

    def __init__(self):
        self.labels = {}

    def set_label(self, ax, label=None):
        ax_id = id(ax)
        if ax_id not in self.labels:
            self.labels[ax_id] = [label]
        else:
            if label not in self.labels[ax_id] or label is None:
                self.labels[ax_id].append(label)
        label_last_id = [i for i, x in enumerate(self.labels[ax_id]) if x == label][-1]
        return label_last_id


def list_size(items):
    items_shape = []
    layer = items
    while isinstance(layer, list):
        if len(layer) > 0:
            items_shape.append(len(layer))
        else:
            break
        layer = layer[0]
    return items_shape


def distorted_list_max_size(items):
    if items:
        ret = deep_process_list(items, layer_action=lambda **kwargs: max(len(kwargs["element"]), kwargs["layer"])
                                if kwargs["layer"] is not None else len(kwargs["element"]))["layer"]
    else:
        ret = []
    return ret


def deep_process_list(obj, leaf_action=None, branch_action=None, layer_action=None):

    ret = {
        "depth": 0,
        "leaves": [],
        "branch": {},
        "layer": []
    }
    ret_map = ret["branch"]

    status_map = {}
    map_focus = status_map
    p_v = obj
    layer = []

    while True:
        if isinstance(p_v, list):

            # pprint(status_map)
            # print(layer)
            # print("--")
            # pprint(ret)
            # print("----------------")
            # print(map_focus)

            # ????????????yet???????????????focus_c_k????????????????????????
            do_continue = False
            focus_c_k = None
            for c_k in range(len(p_v)):

                # ????????????????????????????????????????????????branch????????????leaf?????????????????????yet????????????
                if c_k not in map_focus:
                    map_focus[c_k] = {"_STATUS": "yet", "_BRANCH": {}}
                    focus_c_k = c_k

                # ???????????????????????????????????????????????????????????????focus?????????????????????????????????????????????????????????yet???focus_c_k???????????????
                else:
                    if map_focus[c_k]["_STATUS"] == "yet":
                        focus_c_k = c_k
                    elif map_focus[c_k]["_STATUS"] == "focus":
                        # focus??????????????????????????????????????????
                        focus_c_k = c_k
                        layer.append(focus_c_k)
                        map_focus = map_focus[focus_c_k]["_BRANCH"]
                        p_v = p_v[focus_c_k]
                        if branch_action is not None:
                            ret_map = ret_map[focus_c_k]["branch"]
                        do_continue = True
                        break

            if do_continue:
                continue

            # if focus_c_k is not None:
            #     print(map_focus[focus_c_k]["_STATUS"])
            # else:
            #     print("under focused are ok or checked")

            # ??????????????????????????????????????????branch???checked??????????????????????????????????????????
            if all([map_focus[c_k]["_STATUS"] == "ok" or map_focus[c_k]["_STATUS"] == "checked"
                    for c_k in range(len(p_v))]):

                _map = status_map
                for i in range(len(layer)):
                    if i == len(layer) - 1:
                        _map[layer[i]]['_STATUS'] = "checked"
                        if layer_action is not None:
                            while len(ret["layer"]) - 1 < i+1:
                                ret["layer"].append(None)
                            ret["layer"][i+1] = layer_action(element=p_v, layer=ret["layer"][i+1])
                    _map = _map[layer[i]]['_BRANCH']

                # ??????????????????????????????????????????????????????
                if len(layer) < 1:
                    if layer_action is not None:
                        while len(ret["layer"]) <= 1:
                            ret["layer"].append(None)
                        ret["layer"][0] = layer_action(element=p_v, layer=ret["layer"][0])
                    break

                if branch_action is not None:
                    ret_map = ret["branch"]

                map_focus = status_map
                p_v = obj
                layer = []
                # print("now checked")
                continue

            # ????????????????????????????????????????????????????????????????????????????????????branch???focus????????????
            if isinstance(p_v[focus_c_k], list):

                if branch_action is not None:
                    ret_map[focus_c_k] = {"value": branch_action(element=p_v[focus_c_k]),
                                          "branch": {}}
                    ret_map = ret_map[focus_c_k]["branch"]

                layer.append(focus_c_k)
                map_focus[focus_c_k]["_STATUS"] = "focus"
                map_focus = map_focus[focus_c_k]["_BRANCH"]
                p_v = p_v[focus_c_k]
                # print("now focused")

            # ??????????????????????????????????????????????????????????????????leaf???ok????????????
            else:
                map_focus[focus_c_k]["_STATUS"] = "ok"

                if leaf_action is not None:
                    p_v[focus_c_k] = leaf_action(element=p_v[focus_c_k])
                ret["leaves"].append(p_v[focus_c_k])
                ret["depth"] = max(len(layer) + 1, ret["depth"])
                # print("now ok_ed")

    # print(status_map)
    return ret
