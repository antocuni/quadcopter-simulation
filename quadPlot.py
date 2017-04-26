from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import cnames
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import sys

# TODO add functionality for plotting state and desired_state

class QuadPlotter(object):

    def __init__(self):
        self.fig = plt.figure()
        ax = self.fig.add_axes([0, 0, 1, 1], projection='3d')
        ax.plot([], [], [], '-', c='cyan')[0]
        ax.plot([], [], [], '-', c='red')[0]
        ax.plot([], [], [], '-', c='blue', marker='o', markevery=2)[0]
        self.set_limit((-0.5,0.5), (-0.5,0.5), (-0.5,5))

    def set_limit(self, x, y, z):
        ax = plt.gca()
        ax.set_xlim(x)
        ax.set_ylim(y)
        ax.set_zlim(z)

    def plot_animation(self, get_world_frame):
        """
        get_world_frame is a function which return the "next" world frame to be
        drawn
        """
        def anim_callback(i):
            frame = get_world_frame(i)
            self.set_frame(frame)

        an = animation.FuncAnimation(self.fig,
                                     anim_callback,
                                     init_func=None,
                                     frames=400, interval=10, blit=False)
        if len(sys.argv) > 1 and sys.argv[1] == 'save':
            an.save('sim.gif', dpi=80, writer='imagemagick', fps=60)
        else:
            plt.show(block=False)

    def plot_step(self, world_frame):
        self.set_frame(world_frame)
        plt.pause(0.00001)

    def set_frame(self, frame):
        # convert 3x6 world_frame matrix into three line_data objects which is 3x2 (row:point index, column:x,y,z)
        lines_data = [frame[:,[0,2]], frame[:,[1,3]], frame[:,[4,5]]]
        ax = plt.gca()
        lines = ax.get_lines()
        for line, line_data in zip(lines, lines_data):
            x, y, z = line_data
            line.set_data(x, y)
            line.set_3d_properties(z)
