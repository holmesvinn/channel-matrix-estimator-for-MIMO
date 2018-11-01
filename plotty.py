from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np


real_vals = []
img_vals = []


f = open("channels.txt","r")
data = f.read()
data = data.replace("(","")
data = data.replace(")","")
lines = data.split("\n")
print(lines)

xs = []
ys = []
for line in lines:
    if len(line) > 1:
        x, y = line.split(',')
        print(x,y)
        xs.append(x)
        ys.append(y)

ax = plt.subplot(111, projection='polar')
ax.plot(ys, xs)
ax.set_rmax(2)
ax.set_rticks([0.5, 1, 1.5, 2])  # less radial ticks
ax.set_rlabel_position(-22.5)  # get radial labels away from plotted line
ax.grid(True)

ax.set_title("channel matrix polar plot", va='bottom')
plt.show()