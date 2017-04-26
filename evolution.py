import numpy as np
from model.quadcopter import Quadcopter
from quadPlot import QuadPlotter

DT = 1/200.0 # 200 Hz

class Creature(object):
    INPUTS = 4 # roll, pitch, yaw, z
    OUTPUTS = 4 # 4 motors
    VARS = 5

    def __init__(self, id, generation, parent):
        N = self.INPUTS + self.VARS
        M = self.OUTPUTS + self.VARS
        self.id = id
        self.generation = generation
        self.parent = parent
        self.matrix = np.random.random(N*M).reshape(M, N) - 0.5
        self.constant = np.random.random(M) - 0.5
        self.fitness = 0

    def run(self, show=False):
        plotter = None
        if show:
            plotter = QuadPlotter()
        #
        quad = Quadcopter(pos=(0, 0, 0), attitude=(0, 0, 0))
        state = np.zeros(self.VARS)
        self.fitness = 0
        t = 0
        #
        while t < 2:
            x, y, z = quad.position()
            inputs = np.concatenate([quad.attitude(), [z], state])
            outputs = np.dot(self.matrix, inputs) + self.constant
            motors = outputs[:4]
            state = outputs[4:]
            quad.update_propellers(DT, motors)
            t += DT
            self.fitness += self.compute_fitness(quad)
            if show:
                plotter.plot_step(quad.world_frame())

    def compute_fitness(self, quad):
        # for now, the goal is to reach the target position as fast as
        # possible and then to stay there. So a measure of the fitness is the
        # distance to the target at every step (the goal is to *minimize* the
        # total value, of course)
        target = [0, 0, 1]
        distance = np.linalg.norm(target - quad.position())
        return distance

    def evolve(self):
        """
        What do we want?
        We probably want two steps of evolution:

          1. the first does the "fine tuning": so we adjust many/most/all the values
             by a small amount (+/- 1%?)

         2. the second does rare mutations: it might adjust 1 or 2 values by a larger amount
            (+/- 20%?), but it occurs rarely
        """
        # mu = 0
        # sigma = 0.2
        # k = np.random.normal(mu, sigma, len(self.matrix))
        # matrix + (matrix*k)


def main():
    import time
    c = Creature(0, 1, None)
    c.run(show=True)
    ## for i in range(5):
    ##     start = time.time()
    ##     c.run()
    ##     end = time.time()
    ##     print '%.2f' % (end-start)

if __name__ == '__main__':
    main()
