import numpy
import multiprocessing
import time

from multiprocessing import Pool
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import wait


class Population3D:

    population_type = "3d"
    standard_grid_size = 10
    mode_sequential = "sequential"
    mode_parallel = "parallel"
    cpu_count = multiprocessing.cpu_count()

    ############################################################################
    #                           Constructor                                    #
    ############################################################################
    # @author   yxyxD
    # @changes
    #       2018-02-07 (yxyxD)  created
    #       2018-02-09 (yxyxD)  changed the access of all variables to private
    # @brief    Creates a new population with randomly placed bacteria.
    def __init__(self, grid_size, mode):
        self.__grid_size = grid_size
        self.__mode = mode

        self.__calculation_time = 0
        self.__iteration_count = 0
        self.__world = numpy.random.randint(
            2,
            size=(grid_size, grid_size, grid_size)
        )
        self.__new_world = []

        return

    ############################################################################
    #                           Getter Methods                                 #
    ############################################################################
    # @author   yxyxD
    # @changes
    #       2018-02-09 (yxyxD) created
    # @brief    Returns the grid size of the world.
    def get_grid_size(self):
        return self.__grid_size

    # @author   yxyxD
    # @changes
    #       2018-02-09 (yxyxD) created
    # @brief    Returns the calculation mode in which the next generations are
    #           calculated (either sequential or parallel).
    def get_mode(self):
        return self.__mode

    # @author   yxyxD
    # @changes
    #       2018-02-09 (yxyxD) created
    # @brief    Returns the total amount of time taken for all operations
    #           regarding the calculation of the next generation.
    def get_calculation_time(self):
        return self.__calculation_time

    # @author   yxyxD
    # @changes
    #       2018-02-09 (yxyxD) created
    # @brief    Returns the total amount of generations calculated.
    def get_iteration_count(self):
        return self.__iteration_count

    # @author   yxyxD
    # @changes
    #       2018-02-11 (yxyxD) created
    # @brief    Returns the amount of generations calculated per second.
    def get_calculation_speed(self):
        return  self.__iteration_count / self.__calculation_time

    # @author   yxyxD
    # @changes
    #       2018-02-09 (yxyxD) created
    # @brief    Returns the world of the current generation.
    def get_world(self):
        return self.__world

    ############################################################################
    #                           Public Methods                                 #
    ############################################################################
    # @author   yxyxD
    # @changes
    #       2018-02-07 (yxyxD)  created
    # @brief    Creates and returns the grid of the next population. The
    #           population status of the object will be updated as well.
    def create_and_return_next_generation(self):

        start_time = time.time()

        self.__new_world = self.__world.copy()

        if self.__mode == self.mode_sequential:
            self.__calculate_next_generation_sequential()
        if self.__mode == self.mode_parallel:
            self.__calculate_next_generation_parallel()

        self.__world = self.__new_world.copy()

        end_time = time.time()

        self.__calculation_time += (end_time - start_time)
        self.__iteration_count += 1

        return self.__world

    ############################################################################
    #                           Private Methods                                #
    ############################################################################
    # @author   yxyxD
    # @changes
    #       2018-02-08 (yxyxD)  created
    #       2018-02-09 (yxyxD)  refactored, so that parallel and sequential
    #                           calculations can be done by the same method
    # @brief    Calculates the next generation by calculating each row
    #           sequential.
    def __calculate_next_generation_sequential(self):

        self.__calculate_section_of_world(0, self.__grid_size)

        return

    # @author   yxyxD
    # @changes
    #       2018-02-08 (yxyxD)  created
    #       2018-02-09 (yxyxD)  refactored, so that parallel and sequential
    #                           calculations can be done by the same method
    # @brief    Calculates the next generation by calculating each row
    #           parallel.
    def __calculate_next_generation_parallel(self):

        min_borders, max_borders = self.__get_border_lists()
        executor = ThreadPoolExecutor(min_borders.__len__())
        future_list = []
        for i in range(min_borders.__len__()):
            future_list.append(executor.submit(
                self.__calculate_section_of_world,
                min_borders[i],
                max_borders[i]
            ))

        wait(future_list)

        return

    # @author   yxyxD
    # @changes
    #       2018-02-09 (yxyxD)  created
    # @brief    Calculates a part of the new world (the rows between x_min and
    #           x_max).
    def __calculate_section_of_world(self, x_min, x_max):

        for x in range(x_min, x_max):
            for y in range(self.__grid_size):
                for z in range(self.__grid_size):

                    # @todo search for best rules
                    # working set -> to many living cells
                    #   >= 4; <= 8
                    #   >= 6; <= 8
                    # working set -> dynamic
                    #   >= 4; <= 7
                    #   >= 6; <= 8
                    neighbor_count = self.__get_neighbor_count(x, y, z)
                    if self.__world[x, y, z] == 1:
                        if (neighbor_count >= 2) and (neighbor_count <= 4):
                            self.__new_world[x, y, z] = 1
                        else:
                            self.__new_world[x, y, z] = 0
                    elif self.__world[x, y, z] == 0:
                        if (neighbor_count >= 5) and (neighbor_count <= 6):
                            self.__new_world[x, y, z] = 1

        return

    # @author   yxyxD
    # @changes
    #       2018-02-07 (yxyxD)  created
    # @brief    Counts and returns the total amount of living neighbors of a
    #           cell. If the cell is on the edge of grid, cells on the other
    #           end of the grid count as neighbors too.
    def __get_neighbor_count(self, x, y, z):
        count = 0

        for i in [x - 1, x, x + 1]:
            for j in [y - 1, y, y + 1]:
                for k in [z - 1, z, z + 1]:

                    if (i == x) and (j == y) and (z == k):
                        continue

                    if i == self.__grid_size:
                        continue

                    if j == self.__grid_size:
                        continue

                    if k == self.__grid_size:
                        continue

                    count += self.__world[i][j][k]

        return count

    # @author   yxyxD
    # @changes
    #       2018-02-09 (yxyxD)  created
    # @brief    Creates and returns two lists with borders for parallel
    #           calculations. The first list contains the lower borders for
    #           each Thread. The second list contains the upper borders for
    #           each Thread
    def __get_border_lists(self):
        min_borders = []
        max_borders = []

        # take one core less than available for better performance
        # todo could be the key to get parallel to be faster than sequential
        cpu_count = multiprocessing.cpu_count() - 1

        div, mod = divmod(self.__grid_size, cpu_count)
        if mod == 0:
            border = div
        else:
            border = div + 1

        for i in range(cpu_count):
            min_border = border * i
            max_border = border * (i + 1)
            if max_border > self.__grid_size:
                max_border = self.__grid_size

            min_borders.append(min_border)
            max_borders.append(max_border)

        return min_borders, max_borders
