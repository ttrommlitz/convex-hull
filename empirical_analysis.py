import matplotlib.pyplot as plt
import numpy as np

vals = [10, 100, 1000, 10000, 100000, 500000, 1000000]

# million: 2.981 + 3.054 + 2.993 + 2.980 + 2.954

times = [0.000, 0.001, 0.003, .027, .270, 1.581, 3.177]

x = np.linspace(1, 1000000, 1000)

y = (.0000035) * x

fig, (ax1, ax2) = plt.subplots(1, 2)
fig.suptitle('Empirical Analysis of Convex Hull Algorithm')
ax1.scatter(vals, times)
ax1.set_title('Logarithmic X-Axis Scale')
ax1.set_xscale('log')
# ax1.scale('log')
ax2.scatter(vals, times)
ax2.set_title('Linear X-Axis Scale')
ax2.plot(x, y)

for ax in [ax1, ax2]:
    ax.set_xlabel('Number of Points (n)')
    ax.set_ylabel('Average Time to Find Convex Hull (sec)')

plt.show()

# plt.scatter(vals, times)
# plt.xscale('log')
# # plt.plot(x, y)
# plt.xlabel('Number of Points (n)')
# plt.ylabel('Time to find convex hull (sec)')
# plt.title('Empirical Analysis of Convex Hull Algorithm')
# plt.subplo
# plt.show()