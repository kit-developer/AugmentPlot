from tools.common import get_axes_obj


def blank(*args, plt_obj=()):
    ax = get_axes_obj(plt_obj)
    return ax
