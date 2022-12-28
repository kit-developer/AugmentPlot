import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

print(mpl.get_configdir())
plt.style.use("C:/Users/revoc/.matplotlib/original.mplstyle")

start = 12
num = 20
np.random.seed(777)

for i in range(start, start+num):
    ofs1 = np.random.uniform(0, np.pi, num)
    ofs2 = np.random.uniform(0, np.pi, num)

    plt.figure(figsize=(13, 7))

    for j in range(0, i):
        x = np.linspace(0, 10, 100) + 1.0
        plt.plot(x, np.cos(x + ofs1[j]) + np.sin(x + ofs2[j]), label="cos+sin")

    plt.legend()
    plt.title("sample title")
    plt.grid()
    plt.show()
