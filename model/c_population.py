import numpy
import multiprocessing
import time

from multiprocessing import Pool
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import wait


class Population:

    mode_sequential = "sequential"
    mode_parallel = "parallel"
    cpu_count = multiprocessing.cpu_count()

    ############################################################################
    #                           Constructor                                    #
    ############################################################################
    def __init__(self, grid_size, mode):

        self._grid_size = grid_size
        self._mode = mode

        self._world = []
        self._new_world = []

        self._iteration_count = 0
        self._calculation_time = 0

        self._setup_world_with_population()

        return

    ############################################################################
    #                           Child Implementations                          #
    ############################################################################
    def _setup_world_with_population(self):
        raise NotImplementedError

    def _calculate_section_of_world(self, x_min, x_max):
        raise NotImplementedError

    ############################################################################
    #                           Getter Methods                                 #
    ############################################################################
    def get_grid_size(self):
        return self._grid_size

    def get_mode(self):
        return self._mode

    def get_world(self):
        return self._world

    def get_iteration_count(self):
        return self._iteration_count

    def get_calculation_time(self):
        return self._calculation_time

    def get_calculation_speed(self):
        return self._iteration_count / self._calculation_time

    ############################################################################
    #                           Public Methods                                 #
    ############################################################################
    def create_and_return_next_generation(self):

        start_time = time.time()

        self._new_world = self._world.copy()

        if self._mode == self.mode_sequential:
            self._calculate_next_generation_sequential()
        if self._mode == self.mode_parallel:
            self._calculate_next_generation_parallel()

        self._world = self._new_world.copy()

        end_time = time.time()

        self._calculation_time += (end_time - start_time)
        self._iteration_count += 1

        return self._world

    ############################################################################
    #                           Private Methods                                #
    ############################################################################
    def _calculate_next_generation_sequential(self):

        self._calculate_section_of_world(0, self._grid_size)

        return

    def _calculate_next_generation_parallel(self):

        min_borders, max_borders = self._get_border_lists()
        executor = ThreadPoolExecutor(min_borders.__len__())
        future_list = []
        for i in range(min_borders.__len__()):
            future_list.append(executor.submit(
                self._calculate_section_of_world,
                min_borders[i],
                max_borders[i]
            ))

        wait(future_list)

        return

    def _get_border_lists(self):
        min_borders = []
        max_borders = []

        # take one core less than available for better performance
        # todo could be the key to get parallel to be faster than sequential
        cpu_count = multiprocessing.cpu_count() - 1

        div, mod = divmod(self._grid_size, cpu_count)
        if mod == 0:
            border = div
        else:
            border = div + 1

        for i in range(cpu_count):
            min_border = border * i
            max_border = border * (i + 1)
            if max_border > self._grid_size:
                max_border = self._grid_size

            min_borders.append(min_border)
            max_borders.append(max_border)

        return min_borders, max_borders
