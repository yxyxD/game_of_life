import numpy

from model.c_population import Population


class Population2D(Population):

    population_type = "2d"
    standard_grid_size = 100

    ############################################################################
    #                           Constructor                                    #
    ############################################################################
    # @author   yxyxD
    # @changes
    #       2018-02-21 (yxyxD)  created
    # @brief    Creates a new 2D population with randomly placed bacteria.
    def __init__(self, grid_size, mode):

        super().__init__(grid_size, mode)

        return

    ############################################################################
    #                           Required Implementations                       #
    ############################################################################
    # @author   yxyxD
    # @changes
    #       2018-02-21 (yxyxD)  created
    # @brief    Randomly generates the first generation of the world.
    def _setup_first_generation(self):

        self._world = numpy.random.randint(
            2,
            size=(self._grid_size, self._grid_size)
        )

        return

    # @author   yxyxD
    # @changes
    #       2018-02-21 (yxyxD)  created
    # @brief    Calculates a part of the new world (the rows between x_min and
    #           x_max).
    def _calculate_section_of_new_world(self, x_min, x_max):

        for x in range(x_min, x_max):
            for y in range(self._grid_size):
                neighbor_count = self._get_neighbor_count(x, y)
                if self._world[x, y] == 1:
                    if neighbor_count < 2:
                        self._new_world[x, y] = 0
                    elif neighbor_count == 2 or neighbor_count == 3:
                        self._new_world[x, y] = 1
                    elif neighbor_count > 3:
                        self._new_world[x, y] = 0
                elif self._world[x, y] == 0:
                    if neighbor_count == 3:
                        self._new_world[x, y] = 1

        return

    ############################################################################
    #                           Private Methods                                #
    ############################################################################
    # @author   yxyxD
    # @changes
    #       2018-02-07 (yxyxD)  created
    # @brief    Counts and returns the total amount of living neighbors of a
    #           cell. If the cell is on the edge of grid, cells on the beginning
    #           of the grid count as neighbors too.
    def _get_neighbor_count(self, x, y):
        count = 0

        for i in [x - 1, x, x + 1]:
            for j in [y - 1, y, y + 1]:

                if (i == x) and (j == y):
                    continue

                if (i != self._grid_size) and (j != self._grid_size):
                    count += self._world[i][j]
                elif (i == self._grid_size) and (j != self._grid_size):
                    count += self._world[0][j]
                elif (i != self._grid_size) and (j == self._grid_size):
                    count += self._world[i][0]
                else:
                    count += self._world[0][0]

        return count

