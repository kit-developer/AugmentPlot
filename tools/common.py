from matplotlib import pyplot as plt


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


def deep_process_dict(obj, action):

    status_map = {}
    map_focus = status_map
    p_v = obj
    layer = []

    while True:

        if isinstance(p_v, dict):

            do_continue = False
            for c_k in p_v.keys():
                if c_k not in map_focus:
                    map_focus[c_k] = {"_STATUS": "yet", "_MAP": {}}
                    focus_c_k = c_k
                else:
                    if map_focus[c_k]["_STATUS"] == "yet":
                        focus_c_k = c_k
                    elif map_focus[c_k]["_STATUS"] == "focus":
                        focus_c_k = c_k
                        layer.append(focus_c_k)
                        map_focus = map_focus[focus_c_k]["_MAP"]
                        p_v = p_v[focus_c_k]
                        do_continue = True
            if do_continue:
                continue

            if all([map_focus[c_k]["_STATUS"] == "ok" or map_focus[c_k]["_STATUS"] == "checked"
                    for c_k in p_v.keys()]):
                if len(layer) <= 1:
                    break
                map = status_map[layer[0]]['_MAP']
                for i in range(1, len(layer)):
                    if i == len(layer)-1:
                        map[layer[i]]['_STATUS'] = "checked"
                    map = map[layer[i]]['_MAP']
                map_focus = status_map
                p_v = obj
                layer = []
                continue

            if isinstance(p_v[focus_c_k], dict):
                layer.append(focus_c_k)
                map_focus[focus_c_k]["_STATUS"] = "focus"
                map_focus = map_focus[focus_c_k]["_MAP"]
                p_v = p_v[focus_c_k]
            else:
                map_focus[focus_c_k]["_STATUS"] = "ok"
                path = ""
                path += layer[0]
                for u in layer[1:]:
                    path += "/" + str(u).replace('/', '_')
                path += "/" + str(focus_c_k).replace('/', '_')
                action()

        else:
            break


def deep_process_list(obj, action):

    ret = {"lasts": []}
    status_map = {}
    map_focus = status_map
    p_v = obj
    layer = []

    while True:

        if isinstance(p_v, list):

            do_continue = False
            for c_k in range(len(p_v)):
                if c_k not in map_focus:
                    map_focus[c_k] = {"_STATUS": "yet", "_MAP": {}}
                    focus_c_k = c_k
                else:
                    if map_focus[c_k]["_STATUS"] == "yet":
                        focus_c_k = c_k
                    elif map_focus[c_k]["_STATUS"] == "focus":
                        focus_c_k = c_k
                        layer.append(focus_c_k)
                        map_focus = map_focus[focus_c_k]["_MAP"]
                        p_v = p_v[focus_c_k]
                        do_continue = True
            if do_continue:
                continue

            if all([map_focus[c_k]["_STATUS"] == "ok" or map_focus[c_k]["_STATUS"] == "checked"
                    for c_k in range(len(p_v))]):
                if len(layer) <= 1:
                    break
                map = status_map[layer[0]]['_MAP']
                for i in range(1, len(layer)):
                    if i == len(layer) - 1:
                        map[layer[i]]['_STATUS'] = "checked"
                    map = map[layer[i]]['_MAP']
                map_focus = status_map
                p_v = obj
                layer = []
                continue

            if isinstance(p_v[focus_c_k], list):
                layer.append(focus_c_k)
                map_focus[focus_c_k]["_STATUS"] = "focus"
                map_focus = map_focus[focus_c_k]["_MAP"]
                p_v = p_v[focus_c_k]
            else:
                map_focus[focus_c_k]["_STATUS"] = "ok"

                arg = {
                    "depth": p_v[focus_c_k]
                }
                p_v[focus_c_k] = action(arg=arg)
                ret["lasts"].append(p_v[focus_c_k])
        else:
            break

    return ret
