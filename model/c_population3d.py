from model.c_population import Population

import numpy


class Population3D(Population):

    population_type = "3d"
    standard_grid_size = 10

    def __init__(self, grid_size, mode):

        super().__init__(grid_size, mode)

        return

    def _setup_world_with_population(self):

        self._world = numpy.random.randint(
            2,
            size=(self._grid_size, self._grid_size, self._grid_size)
        )

        return

    def _calculate_section_of_world(self, x_min, x_max):

        for x in range(x_min, x_max):
            for y in range(self._grid_size):
                for z in range(self._grid_size):

                    # @todo search for best rules
                    # working set -> to many living cells
                    #   >= 4; <= 8
                    #   >= 6; <= 8
                    # working set -> dynamic
                    #   >= 4; <= 7
                    #   >= 6; <= 8
                    neighbor_count = self._get_neighbor_count(x, y, z)
                    if self._world[x, y, z] == 1:
                        if (neighbor_count >= 2) and (neighbor_count <= 4):
                            self._new_world[x, y, z] = 1
                        else:
                            self._new_world[x, y, z] = 0
                    elif self._world[x, y, z] == 0:
                        if (neighbor_count >= 5) and (neighbor_count <= 6):
                            self._new_world[x, y, z] = 1

        return

    def _get_neighbor_count(self, x, y, z):
        count = 0

        for i in [x - 1, x, x + 1]:
            for j in [y - 1, y, y + 1]:
                for k in [z - 1, z, z + 1]:

                    if (i == x) and (j == y) and (z == k):
                        continue

                    if i == self._grid_size:
                        continue

                    if j == self._grid_size:
                        continue

                    if k == self._grid_size:
                        continue

                    count += self._world[i][j][k]

        return count