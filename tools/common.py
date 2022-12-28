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
