import matplotlib.pyplot as mpl_pyplot
import matplotlib.animation as mpl_animation

from matplotlib.colors import ListedColormap

import numpy
import time

from mpi4py import MPI


standard_grid_size = 100


################################################################################
#                           User Output Functions                              #
################################################################################
# @author   yxyxD
# @changes
#       2018-02-11 (yxyxD)  created
#       2018-02-15 (marxmanEUW)  modified for mpi
# @brief    Prints the required calculation speed per generation.
def __user_output_calculation_speed():
    global iteration_count, calculation_time

    if iteration_count % 5 == 0:
        print(
            "Calculation speed = "
              + str(round((iteration_count / calculation_time), 5))
              + " iteration(s) per second"
        )

    return


################################################################################
#                           Update Method for Animation                        #
################################################################################
# @author   yxyxD
# @changes
#       2018-02-07 (yxyxD)  created
#       2018-02-15 (marxmanEUW)  modified for mpi
# @brief    !!! IMPORTANT !!!
#           Updates the data grid for the animation. Do not change location or
#           parameter, unless you know what you are doing.
def update(data):

    __calculate_next_generation()
    mat.set_data(world)
    __user_output_calculation_speed()
    return [mat]


################################################################################
#                           Public Methods                                     #
################################################################################
# @author   yxyxD
# @changes
#       2018-02-07 (yxyxD)  created
#       2018-02-15 (marxmanEUW)  modified for mpi
# @brief    Creates and returns the grid of the next population. The
#           population status of the object will be updated as well.
def __calculate_next_generation():
    global world, new_world, iteration_count, calculation_time

    mpi_comm = MPI.COMM_WORLD

    start_time = time.time()

    new_world = world.copy()

    min_borders, max_borders = __get_border_lists_for()
    # for i in range(min_borders.__len__()):
        # mpi_comm.send(world, dest=(i + 1), tag=1)
        # mpi_comm.send(min_borders[i], dest=(i + 1), tag=2)
        # mpi_comm.send(max_borders[i], dest=(i + 1), tag=3)

    for i in range(min_borders.__len__()):
        new_partial_world = mpi_comm.recv(source=(i + 1), tag=4)

        for x in range(min_borders[i], max_borders[i]):
            for y in range(standard_grid_size):
                new_world[x, y] = new_partial_world[x, y]

    world = new_world.copy()

    end_time = time.time()

    calculation_time += (end_time - start_time)
    iteration_count += 1

    return


# @author   yxyxD
# @changes
#       2018-02-09 (yxyxD)  created
#       2018-02-15 (marxmanEUW)  modified for mpi
# @brief    Calculates a part of the new world (the rows between start_x and
#           end_x).
def __calculate_section_of_world(start_x, end_x):
    global world, new_world

    new_world = world.copy()

    for x in range(start_x, end_x):
        for y in range(standard_grid_size):
            neighbor_count = __get_neighbor_count(x, y)
            if world[x, y] == 1:
                if neighbor_count < 2:
                    new_world[x, y] = 0
                elif neighbor_count == 2 or neighbor_count == 3:
                    new_world[x, y] = 1
                elif neighbor_count > 3:
                    new_world[x, y] = 0
            elif world[x, y] == 0:
                if neighbor_count == 3:
                    new_world[x, y] = 1

    world = new_world.copy()

    return


# @author   yxyxD
# @changes
#       2018-02-07 (yxyxD)  created
#       2018-02-15 (marxmanEUW)  modified for mpi
# @brief    Counts and returns the total amount of living neighbors of a
#           cell. If the cell is on the edge of grid, cells on the other
#           end of the grid count as neighbors too.
# @todo     the counting logic for cells at the edge is most likely wrong
def __get_neighbor_count(x, y):
    global world, new_world

    count = 0

    for i in [x - 1, x, x + 1]:
        for j in [y - 1, y, y + 1]:

            if (i == x) and (j == y):
                continue

            if (i != standard_grid_size) and (j != standard_grid_size):
                count += world[i][j]
            elif (i == standard_grid_size) and (j != standard_grid_size):
                count += world[0][j]
            elif (i != standard_grid_size) and (j == standard_grid_size):
                count += world[i][0]
            else:
                count += world[0][0]

    return count


# @author   yxyxD
# @changes
#       2018-02-09 (yxyxD)  created
#       2018-02-15 (marxmanEUW)  modified for mpi
# @brief    Creates and returns two lists with borders for parallel
#           calculations. The first list contains the lower borders for
#           each Thread. The second list contains the upper borders for
#           each Thread
def __get_border_lists_for():

    mpi_size = MPI.COMM_WORLD.size - 1

    min_borders = []
    max_borders = []

    div, mod = divmod(standard_grid_size, mpi_size)
    if mod == 0:
        border = div
    else:
        border = div + 1

    for i in range(mpi_size):
        min_border = border * i
        max_border = border * (i + 1)
        if max_border > standard_grid_size:
            max_border = standard_grid_size

        min_borders.append(min_border)
        max_borders.append(max_border)

    return min_borders, max_borders


################################################################################
#                           Starting Point                                     #
################################################################################
# @author   yxyxD
# @changes
#       2018-02-06 (yxyxD)  created
#       2018-02-08 (yxyxD)  implemented user inputs for console
#       2018-02-15 (marxmanEUW)  modified for mpi
# @brief    Starting point of the program.
if __name__ == '__main__':

    global world, calculation_time, iteration_count

    calculation_time = 0
    iteration_count = 0

    mpi_comm = MPI.COMM_WORLD
    mpi_size = mpi_comm.size
    mpi_rank = mpi_comm.rank

    if mpi_rank == 0:
        print("using MPI with standard grid size: " + str(standard_grid_size))
        print("MPI size: " + str(mpi_size))

    if mpi_rank == 0:
        print("")
        print("Program started")
        print("")

        world = numpy.random.randint(
            2,
            size=(standard_grid_size, standard_grid_size)
        )

        fig, ax = mpl_pyplot.subplots()

        cmap = ListedColormap(['white', 'black'])
        mat = ax.matshow(world, cmap=cmap)

        animation = mpl_animation.FuncAnimation(
            fig,
            update,
            interval=50
        )

        mpl_pyplot.show()
    else:

        world = mpi_comm.recv(source=0, tag=1)
        start_x = mpi_comm.recv(source=0, tag=2)
        end_x = mpi_comm.recv(source=0, tag=3)

        while True:
            __calculate_section_of_world(start_x, end_x)

            mpi_comm.send(world, dest=0, tag=4)

            mpi_comm.send(world[start_x], dest=(mpi_rank - 1))

