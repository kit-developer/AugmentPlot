import numpy as np
from matplotlib.colors import LinearSegmentedColormap


def color_bar_horizontal(x, y, xlim=(), resolution=100, colormap=None, alpha=0.6):

    if len(x) != len(y):
        raise ValueError("not same length x and y!")

    if colormap is None:
        colors = ['#191970', '#ff1493']
        colormap = LinearSegmentedColormap.from_list('custom', colors)

    max_y = max(y)
    min_y = min(y)
    frame = np.zeros((resolution, 4))

    if len(xlim) == 2:
        max_x = xlim[1]
        min_x = xlim[0]
    else:
        max_x = np.max(x)
        min_x = np.min(x)

    x_rates = []
    for i in range(len(x)):
        x_rate = (x[i] - min_x) / (max_x - min_x) * resolution
        x_rates.append(x_rate)

    x_rates = np.array(x_rates)
    for i in range(resolution):
        if np.min(np.abs(x_rates - i)) < 0.5:
            near_x = np.argmin(np.abs(x_rates - i))
            value = (y[near_x] - min_y) / (max_y - min_y)
            color = colormap(int(value * colormap.N))
            frame[i] = (color[0], color[1], color[2], alpha)

    frame = np.array(frame).reshape((1, -1, 4))

    return frame
