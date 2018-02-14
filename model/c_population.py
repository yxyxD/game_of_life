import numpy
import multiprocessing
import time

from multiprocessing import Pool
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import wait

from mpi4py import MPI


class Population:

    standard_grid_size = 100
    mode_sequential = "sequential"
    mode_parallel = "parallel"
    mode_mpi = "mpi"
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
            size=(grid_size, grid_size)
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
        if self.__mode == self.mode_mpi:
            self.__calculate_next_generation_mpi()

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

    # @author   marxmanEUW
    # @changes
    #       2018-02-13 (marxmanEUW)  created
    # @brief    Calculates the next generation by calculating each row
    #           parallel using mpi.
    def __calculate_next_generation_mpi(self):

        mpi_comm = MPI.COMM_WORLD

        min_borders, max_borders = self.__get_border_lists_for_mpi()
        for i in range(min_borders.__len__()):
            mpi_comm.send(self.__world, dest=(i + 1), tag=1)
            mpi_comm.send(min_borders[i], dest=(i + 1), tag=2)
            mpi_comm.send(max_borders[i], dest=(i + 1), tag=3)

        for i in range(min_borders.__len__()):
            new_partial_world = mpi_comm.recv(source=(i + 1), tag=4)

            for x in range(min_borders[i], max_borders[i]):
                for y in range(self.__grid_size):
                    self.__new_world[x, y] = new_partial_world[x, y]

        return

    # @author   yxyxD
    # @changes
    #       2018-02-09 (yxyxD)  created
    # @brief    Calculates a part of the new world (the rows between x_min and
    #           x_max).
    def __calculate_section_of_world(self, x_min, x_max):

        for x in range(x_min, x_max):
            for y in range(self.__grid_size):
                neighbor_count = self.__get_neighbor_count(x, y)
                if self.__world[x, y] == 1:
                    if neighbor_count < 2:
                        self.__new_world[x, y] = 0
                    elif neighbor_count == 2 or neighbor_count == 3:
                        self.__new_world[x, y] = 1
                    elif neighbor_count > 3:
                        self.__new_world[x, y] = 0
                elif self.__world[x, y] == 0:
                    if neighbor_count == 3:
                        self.__new_world[x, y] = 1

        return

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

                if (i == x) and (j == y):
                    continue

                if (i != self.__grid_size) and (j != self.__grid_size):
                    count += self.__world[i][j]
                elif (i == self.__grid_size) and (j != self.__grid_size):
                    count += self.__world[0][j]
                elif (i != self.__grid_size) and (j == self.__grid_size):
                    count += self.__world[i][0]
                else:
                    count += self.__world[0][0]

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

    # @author   marxmanEUW
    # @changes
    #       2018-02-13 (marxmanEUW)  created
    # @brief    Creates and returns two lists with borders for parallel
    #           calculations. The first list contains the lower borders for
    #           each MPI Process. The second list contains the upper borders for
    #           each MPI Process
    def __get_border_lists_for_mpi(self):

        mpi_size = MPI.COMM_WORLD.size - 1

        min_borders = []
        max_borders = []

        div, mod = divmod(self.__grid_size, mpi_size)
        if mod == 0:
            border = div
        else:
            border = div + 1

        for i in range(mpi_size):
            min_border = border * i
            max_border = border * (i + 1)
            if max_border > self.__grid_size:
                max_border = self.__grid_size

            min_borders.append(min_border)
            max_borders.append(max_border)

        return min_borders, max_borders