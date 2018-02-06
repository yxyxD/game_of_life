import numpy as numpy

class Generation:

    const = 123

    # Constructor
    def __init__(self, gridSize):
        self.world = numpy.random.randint(
            2,
            size=(gridSize, gridSize)
        )
        return

    def print_generation(self):
        print(self.world)
        return

    def get_neighbor_count(self):
        return

    def get_next_generation(self):
        return