import numpy as numpy


class Population:

    ############################################################################
    #                           Constructor                                    #
    ############################################################################
    # @author   yxyxD
    # @changes
    #       2018-02-07 (yxyxD)  created
    # @brief    Creates a new population with randomly placed bacteria.
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.world = numpy.random.randint(
            2,
            size=(grid_size, grid_size)
        )
        return

    ############################################################################
    #                           Public Methods                                 #
    ############################################################################
    # @author   yxyxD
    # @changes
    #       2018-02-07 (yxyxD)  created
    # @brief    Creates and returns the grid of the next population. The
    #           population status of the object will be updated as well.
    def create_and_return_next_generation(self):
        new_world = self.world.copy()

        for x in range(self.grid_size):
            for y in range(self.grid_size):
                neighbor_count = self.__get_neighbor_count(x, y)
                if self.world[x, y] == 1:
                    if neighbor_count < 2:
                        new_world[x, y] = 0
                    elif neighbor_count == 2 or neighbor_count == 3:
                        new_world[x, y] = 1
                    elif neighbor_count > 3:
                        new_world[x, y] = 0
                elif self.world[x, y] == 0:
                    # todo == 3 oder > 3? => Regeln nachgucken
                    if neighbor_count == 3:
                        new_world[x, y] = 1

        self.world = new_world

        return new_world

    ############################################################################
    #                           Private Methods                                #
    ############################################################################
    # @author   yxyxD
    # @changes
    #       2018-02-07 (yxyxD)  created
    # @brief    Counts and returns the total amount of living neighbors of a
    #           cell. If the cell is on the edge of grid, cells on the other
    #           end of the grid count as neighbors too.
    # @todo     the counting logic for cells at the edge is most likely wrong
    def __get_neighbor_count(self, x, y):
        count = 0

        for i in [x - 1, x, x + 1]:
            for j in [y - 1, y, y + 1]:

                if (i == x and j == y):
                    continue

                if (i != self.grid_size and j != self.grid_size):
                    count += self.world[i][j]
                elif (i == self.grid_size and j != self.grid_size):
                    count += self.world[0][j]
                elif (i != self.grid_size and j == self.grid_size):
                    count += self.world[i][0]
                else:
                    count += self.world[0][0]

        return count
