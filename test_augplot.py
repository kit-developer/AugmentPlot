import numpy as np
from aug_plot import AugmentPlot


def dynamic():
    ap = AugmentPlot(grid=(5, 3), main_canvas=((0, 3), (0, 1)),
                     stylesheet="./original.mplstyle")
    ap.add_subplot(1, 1, 1, group="cos-log")
    x = np.array([0])

    length = 10
    for i in range(1, 100):
        x = np.append(x, i)
        if i >= length:
            x = x[-length:]

        ap.plot(x, np.cos(x), group="cos-log", label="cos")
        ap.plot(x, np.log(x), group="cos-log", label="log")

        ap.pause_cla(0.01)

    # ap.show(legend=False)


def static1():
    ap = AugmentPlot(grid=(5, 3), main_canvas=((0, 3), (0, 1)),
                     stylesheet="./original.mplstyle")

    ap.add_subplot(1, 1, 1, group="cos-log")

    x = np.linspace(0, 10, 100) + 1.0

    ap.plot(x, np.cos(x), group="cos-log", label="cos")
    # ap.plot(x, np.log(x), group="cos-log", label="log")

    ap.show()


def static3():
    # ap = AugmentPlot(grid=(6, 3), main_canvas=((0, 3), (0, 1)))
    ap = AugmentPlot(grid=(5, 3), main_canvas=((0, 3), (0, 1)),
                     stylesheet="./original.mplstyle")

    ap.add_subplot(2, 2, 1, group="cos-log", g_attribute="2plot")
    ap.add_subplot(2, 2, 3, group="log-sin", g_attribute="2plot")
    ap.add_subplot(1, 2, 2, group="cos-sin", g_attribute="1plot")

    x = np.linspace(0, 10, 100) + 1.0

    ap.plot(x, np.cos(x), group="cos-log", label="cos", l_attribute="wave")
    ap.plot(x, np.log(x), group="cos-log", label="log", l_attribute="log")

    ap.plot(x, np.log(x), group="log-sin", label="log", l_attribute="log")
    ap.plot(x, np.sin(x), group="log-sin", label="sin", l_attribute="wave")

    ap.plot(x, np.cos(x), group="cos-sin", label="cos", l_attribute="wave")
    ap.plot(x, np.sin(x), group="cos-sin", label="sin", l_attribute="wave")

    ap.show()


def dynamic3():
    ap = AugmentPlot(grid=(5, 3), main_canvas=((0, 3), (0, 1)),
                     stylesheet="./original.mplstyle")

    ap.add_subplot(2, 2, 1, group="cos-log", g_attribute="2plot")
    ap.add_subplot(2, 2, 3, group="log-sin", g_attribute="2plot")
    ap.add_subplot(1, 2, 2, group="cos-sin", g_attribute="1plot")

    x = np.array([0])

    length = 10
    for i in range(1, 100):
        x = np.append(x, i)
        if i >= length:
            x = x[-length:]

        ap.plot(x, np.cos(x), group="cos-log", label="cos", l_attribute="wave")
        ap.plot(x, np.log(x), group="cos-log", label="log", l_attribute="log")

        ap.plot(x, np.log(x), group="log-sin", label="log", l_attribute="log")
        ap.plot(x, np.sin(x), group="log-sin", label="sin", l_attribute="wave")

        ap.plot(x, np.cos(x), group="cos-sin", label="cos", l_attribute="x")
        ap.plot(x, np.sin(x), group="cos-sin", label="sin", l_attribute="y")

        ap.pause_cla(0.01)


def static4():
    # ap = AugmentPlot(grid=(6, 3), main_canvas=((0, 3), (0, 1)))
    ap = AugmentPlot(grid=(5, 3), main_canvas=((0, 3), (0, 1)),
                     stylesheet="./original.mplstyle")

    ap.add_subplot(2, 2, 1, group="group1(A)", g_attribute="A")
    ap.add_subplot(2, 2, 3, group="group2(A)", g_attribute="A")
    ap.add_subplot(1, 2, 2, group="group3(B)", g_attribute="B")
    ap.add_subplot(1, 2, 2, group="group4(B)", g_attribute="B")
    ap.add_subplot(1, 2, 2, group="group5(A)", g_attribute="A")

    x = np.linspace(0, 10, 100) + 1.0

    ap.plot(x, np.cos(x), group="group1(A)", label="1-1(A-a)", l_attribute="a")
    ap.plot(x, np.sin(x), group="group1(A)", label="1-2(A-b)", l_attribute="b")
    ap.plot(x, np.log(x), group="group1(A)", label="1-2(A-c)", l_attribute="c")

    ap.plot(x, np.log(x), group="group2(A)", label="2-1(A-a)", l_attribute="a")
    ap.plot(x, np.sin(x), group="group2(A)", label="2-1(A-b)", l_attribute="b")

    ap.plot(x, np.cos(x), group="group3(B)", label="3-1(B-a)", l_attribute="a")

    ap.plot(x, np.cos(x), group="group4(B)", label="4-1(B-a)", l_attribute="a")

    ap.plot(x, np.log(x), group="group5(A)", label="5-1(A-a)", l_attribute="a")
    ap.plot(x, np.sin(x), group="group5(A)", label="5-1(A-b)", l_attribute="b")

    ap.show()


if __name__ == '__main__':
    static3()
