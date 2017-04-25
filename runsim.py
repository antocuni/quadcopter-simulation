"""
author: Peter Huang, Antonio Cuni
email: hbd730@gmail.com, anto.cuni@gmail.com
license: BSD
Please feel free to use and modify this, but keep the above information. Thanks!
"""

from quadPlot import plot_quad_3d
import controller
import trajGen
from model.quadcopter import Quadcopter
import numpy as np

PLAYBACK_SPEED = 4
control_frequency = 200 # Hz for attitude control loop
dt = 1.0 / control_frequency
time = [0.0]

def attitudeControl(quad, time):
    desired_state = trajGen.genLine(time[0])
    F, M = controller.run(quad, desired_state)
    quad.update(dt, F, M)
    time[0] += dt

def main():
    pos = (0,0,0)
    attitude = (0,0,np.pi/2)
    quadcopter = Quadcopter(pos, attitude)

    def control_loop(i):
        for _ in range(PLAYBACK_SPEED):
            attitudeControl(quadcopter, time)
        return quadcopter.world_frame()

    plot_quad_3d(get_world_frame=control_loop)

if __name__ == "__main__":
    main()

