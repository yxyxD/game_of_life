import multiprocessing
import time
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import wait


class Population:

    mode_sequential = "seq"
    mode_parallel = "par"
    cpu_count = multiprocessing.cpu_count()

    ############################################################################
    #                           Constructor                                    #
    ############################################################################
    # @author   yxyxD
    # @changes
    #       2018-02-07 (yxyxD)  created
    # @brief    Creates a new population with randomly placed bacteria.
    def __init__(self, grid_size, mode):

        self._grid_size = grid_size
        self._mode = mode

        self._world = []
        self._new_world = []

        self._iteration_count = 0
        self._calculation_time = 0

        self._setup_first_generation()

        return

    ############################################################################
    #                           Child Implementations                          #
    ############################################################################
    # @author   yxyxD
    # @changes
    #       2018-02-21 (yxyxD)  created
    # @brief    Child classes need to implement this method to set up the first
    #           generation of the world.
    def _setup_first_generation(self):
        raise NotImplementedError

    # @author   yxyxD
    # @changes
    #       2018-02-21 (yxyxD)  created
    # @brief    Child classes need to implement this method to calculate a
    #           section of the next generation
    def _calculate_section_of_new_world(self, x_min, x_max):
        raise NotImplementedError

    ############################################################################
    #                           Getter Methods                                 #
    ############################################################################
    # @author   yxyxD
    # @changes
    #       2018-02-21 (yxyxD) created
    # @brief    Returns the grid size of the world.
    def get_grid_size(self):
        return self._grid_size

    # @author   yxyxD
    # @changes
    #       2018-02-21 (yxyxD) created
    # @brief    Returns the calculation mode in which the next generations are
    #           calculated (either sequential or parallel).
    def get_mode(self):
        return self._mode

    # @author   yxyxD
    # @changes
    #       2018-02-21 (yxyxD) created
    # @brief    Returns the world of the current generation.
    def get_world(self):
        return self._world

    # @author   yxyxD
    # @changes
    #       2018-02-21 (yxyxD) created
    # @brief    Returns the total amount of generations calculated.
    def get_iteration_count(self):
        return self._iteration_count

    # @author   yxyxD
    # @changes
    #       2018-02-21 (yxyxD) created
    # @brief    Returns the total amount of time taken for all operations
    #           regarding the calculation of the next generation.
    def get_calculation_time(self):
        return self._calculation_time

    # @author   yxyxD
    # @changes
    #       2018-02-21 (yxyxD) created
    # @brief    Returns the amount of generations calculated per second.
    def get_calculation_speed(self):
        return self._iteration_count / self._calculation_time

    ############################################################################
    #                           Setter Methods                                 #
    ############################################################################
    # @author   marxmanEUW
    # @changes
    #       2018-02-21 (yxyxD) created
    # @brief    Sets the calculation time of the population.
    def set_calculation_time(self, calculation_time):
        self._calculation_time = calculation_time

    # @author   marxmanEUW
    # @changes
    #       2018-02-21 (yxyxD) created
    # @brief    Sets the calculation time of the population.
    def set_world(self, world):
        self._world = world.copy()


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

    # @author   marxmanEUW
    # @changes
    #       2018-03-08 (marxmanEUW) created
    # @brief    Increments the iteration count of the population.
    def iteration_count_increment(self):
        self._iteration_count += 1

    ############################################################################
    #                           Private Methods                                #
    ############################################################################
    # @author   yxyxD
    # @changes
    #       2018-02-21 (yxyxD)  created
    # @brief    Calculates the next generation by calculating each row
    #           sequential.
    def _calculate_next_generation_sequential(self):

        self._calculate_section_of_new_world(0, self._grid_size)

        return

    # @author   yxyxD
    # @changes
    #       2018-02-21 (yxyxD)  created
    # @brief    Calculates the next generation by calculating each row
    #           parallel.
    def _calculate_next_generation_parallel(self):

        min_borders, max_borders = self._get_border_lists()
        executor = ThreadPoolExecutor(min_borders.__len__())
        future_list = []
        for i in range(min_borders.__len__()):
            future_list.append(executor.submit(
                self._calculate_section_of_new_world,
                min_borders[i],
                max_borders[i]
            ))

        wait(future_list)

        return

    # @author   yxyxD
    # @changes
    #       2018-02-21 (yxyxD)  created
    # @brief    Creates and returns two lists with borders for parallel
    #           calculations. The first list contains the lower borders for
    #           each Thread. The second list contains the upper borders for
    #           each Thread
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
