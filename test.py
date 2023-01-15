from matplotlib import pyplot as plt
import numpy as np

fig = plt.figure()

ax1 = fig.add_subplot(2, 2, 1)
ax2 = fig.add_subplot(2, 2, 3)
ax3 = fig.add_subplot(1, 2, 2)

x = np.linspace(0, 10, 100) + 1.0

ax1.plot(x, np.cos(x), label="cos")
ax1.plot(x, np.log(x), label="log")
ax1.set_title("cos-log")

ax2.plot(x, np.log(x), label="log")
ax2.plot(x, np.sin(x), label="sin")
ax2.set_title("log-sin")

ax3.plot(x, np.cos(x), label="cos")
ax3.plot(x, np.sin(x), label="sin")
ax3.set_title("cos-sin")

plt.show()
