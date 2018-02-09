import numpy as numpy

from multiprocessing import Pool
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from concurrent.futures import wait

import multiprocessing
import time


class Population:

    standard_grid_size = 100
    mode_sequential = "sequential"
    mode_parallel = "parallel"


    ############################################################################
    #                           Constructor                                    #
    ############################################################################
    # @author   yxyxD
    # @changes
    #       2018-02-07 (yxyxD)  created
    # @brief    Creates a new population with randomly placed bacteria.
    def __init__(self, grid_size, mode):
        self.grid_size = grid_size
        self.mode = mode
        self.calculation_time = 0
        self.iteration_count = 0
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

        start_time = time.time()

        if (self.mode == self.mode_sequential):
            new_world = self.__calculate_next_generation_sequential()
        if (self.mode == self.mode_parallel):
            new_world = self.__calculate_next_generation_parallel()

        self.world = new_world

        end_time = time.time()
        self.calculation_time += (end_time - start_time)

        self.iteration_count += 1
        if (self.iteration_count % 20 == 0):
            calculation_speed = self.iteration_count / self.calculation_time
            print("Calculation speed = " + str(calculation_speed) + " iterations per second")

        return new_world

    ############################################################################
    #                           Private Methods                                #
    ############################################################################
    # @author   yxyxD
    # @changes
    #       2018-02-08 (yxyxD)  created
    # @brief    Calculates the next generation by calculating each row
    #           sequential.
    def __calculate_next_generation_sequential(self):
        new_world = self.world.copy()

        for x in range(self.grid_size):
            x_ret, row = self.__get_next_row(x)
            new_world[x] = row

        self.world = new_world

        return new_world

    # @author   yxyxD
    # @changes
    #       2018-02-08 (yxyxD)  created
    # @brief    Calculates the next generation by calculating each row
    #           parallel.
    def __calculate_next_generation_parallel(self):
        new_world = self.world.copy()

        executor = ThreadPoolExecutor()
        future_list = []
        for x in range(self.grid_size):
            future = executor.submit(self.__get_next_row, x)
            future_list.append(future)

        wait(future_list)

        for future in future_list:
            x, row = future.result()
            new_world[x] = row

        return new_world

    # @author   yxyxD
    # @changes
    #       2018-02-08 (yxyxD)  created
    # @brief    Calculates one row of the next generation of the population.
    def __get_next_row(self, x):
        row = numpy.zeros(self.grid_size)

        for y in range(self.grid_size):
            neighbor_count = self.__get_neighbor_count(x, y)
            if self.world[x, y] == 1:
                if neighbor_count < 2:
                    row[y] = 0
                elif neighbor_count == 2 or neighbor_count == 3:
                    row[y] = 1
                elif neighbor_count > 3:
                    row[y] = 0
            elif self.world[x, y] == 0:
                if neighbor_count == 3:
                    row[y] = 1

        return x, row

    def __test(self, x_min, x_max):
        new_world_part = numpy.zeros(self.grid_size, self.grid_size)

        #for x in range(self.grid_size):


        return new_world_part

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

                if (i != self.grid_size) and (j != self.grid_size):
                    count += self.world[i][j]
                elif (i == self.grid_size) and (j != self.grid_size):
                    count += self.world[0][j]
                elif (i != self.grid_size) and (j == self.grid_size):
                    count += self.world[i][0]
                else:
                    count += self.world[0][0]

        return count


    def __get_border_list(self):
        borders = []
        cpu_count = multiprocessing.cpu_count()

        div, mod = divmod(self.grid_size, cpu_count)
        if mod == 0:
            iterator = div
        else:
            iterator = div + 1

        for i in range(cpu_count + 1):
            border = iterator * i
            if border <= self.grid_size:
                borders.append(border)
            else:
                borders.append(self.grid_size)

        return borders
