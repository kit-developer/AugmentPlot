import numpy as np
import cv2
from matplotlib.patches import Polygon
from matplotlib.artist import _XYPair


def gradation(width, height, color1, color2, direction=0):

    diagonal = int(np.sqrt(width**2 + height**2)) + 2
    tmp = np.zeros((diagonal, diagonal, len(color1)))

    for i, (start, stop) in enumerate(zip(color1, color2)):
        tmp[:, :, i] = np.tile(np.linspace(start, stop, diagonal), (diagonal, 1)).T

    rotate_matrix = cv2.getRotationMatrix2D(center=(diagonal/2, diagonal/2), angle=-direction, scale=1)
    img = cv2.warpAffine(tmp, rotate_matrix, (diagonal, diagonal))
    ofs_w = (diagonal - width)//2
    ofs_h = (diagonal - height)//2
    return np.uint8(img[ofs_h:ofs_h+height, ofs_w:ofs_w+width, :])


def set_imaged_polygon(ax, x, y, image, aspect=None):

    np_x = np.array(x)
    np_y = np.array(y)
    min_x, max_x = np.min(np_x), np.max(np_x)
    min_y, max_y = np.min(np_y), np.max(np_y)

    np_v = np.array([np_x, np_y])
    path = np_v.T

    img = ax.imshow(image, extent=[min_x, max_x, min_y, max_y], aspect=aspect)
    img._sticky_edges = _XYPair([], [])

    polygon = Polygon(path, closed=True, facecolor='none', edgecolor='none')
    ax.add_patch(polygon)
    img.set_clip_path(polygon)
