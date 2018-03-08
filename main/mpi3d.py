import matplotlib.animation as mpl_animation

from c_population3d import Population3D
from c_main_frame import MainFrame

import threadsafe_tkinter as Tkinter
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

import numpy
import time

from mpi4py import MPI


standard_grid_size = 10
animate = True


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
    global world, main_frame, calculation_time

    main_frame.clear_axes()

    main_frame.axis.set_xlim([0, main_frame.population.get_grid_size()])
    main_frame.axis.set_ylim([0, main_frame.population.get_grid_size()])
    main_frame.axis.set_zlim([0, main_frame.population.get_grid_size()])

    main_frame.axis.set_xlabel("x")
    main_frame.axis.set_ylabel("y")
    main_frame.axis.set_zlabel("z")

    world = main_frame.population.get_world()
    __calculate_next_generation()
    main_frame.population.iteration_count_increment()
    main_frame.population.set_calculation_time(calculation_time)

    for x in range(main_frame.population.get_grid_size()):
        for y in range(main_frame.population.get_grid_size()):
            for z in range(main_frame.population.get_grid_size()):

                if world[x][y][z] == 1:
                    points = numpy.array([
                        [x, y, z],              # [0] down lower left
                        [x + 1, y, z],          # [1] down lower right
                        [x, y + 1, z],          # [2] down upper left
                        [x + 1, y + 1, z],      # [3] down upper right
                        [x, y, z + 1],          # [4] up lower left
                        [x + 1, y, z + 1],      # [5] up lower right
                        [x, y + 1, z + 1],      # [6] up upper left
                        [x + 1, y + 1, z + 1]   # [7] up upper right
                    ])

                    sides = [
                        [points[0], points[1], points[3], points[2]],   # bottom
                        [points[0], points[1], points[5], points[4]],   # front
                        [points[0], points[2], points[6], points[4]],   # left
                        [points[1], points[3], points[7], points[5]],   # right
                        [points[2], points[3], points[7], points[6]],   # back
                        [points[4], points[5], points[7], points[6]]    # top
                    ]

                    main_frame.axis.add_collection3d(Poly3DCollection(
                        sides, facecolors='blue', linewidths=1, edgecolors='black'
                    ))

    main_frame.update_population_status()
    __user_output_calculation_speed()

    return


def loop_no_animation():
    __calculate_next_generation()
    __user_output_calculation_speed()
    return


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
    for i in range(min_borders.__len__()):
        mpi_comm.send(world, dest=(i + 1), tag=1)
        mpi_comm.send(min_borders[i], dest=(i + 1), tag=2)
        mpi_comm.send(max_borders[i], dest=(i + 1), tag=3)

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
            for z in range(standard_grid_size):

                neighbor_count = __get_neighbor_count(x, y, z)

                if world[x][y][z] == 1:
                    if (neighbor_count >= 2) and (neighbor_count <= 4):
                        new_world[x][y][z] = 1
                    else:
                        new_world[x][y][z] = 0
                elif world[x][y][z] == 0:
                    if (neighbor_count >= 5) and (neighbor_count <= 6):
                        new_world[x][y][z] = 1

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
def __get_neighbor_count(x, y, z):
    global world

    count = 0

    for i in [x - 1, x, x + 1]:
        for j in [y - 1, y, y + 1]:
            for k in [z - 1, z, z + 1]:

                if (i == x) and (j == y) and (z == k):
                    continue

                if (i == x) and (j == y) and (z == k):
                    continue

                if i == standard_grid_size:
                    continue

                if j == standard_grid_size:
                    continue

                if k == standard_grid_size:
                    continue

                count += world[i][j][k]

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

    global world, calculation_time, iteration_count, main_frame

    calculation_time = 0
    iteration_count = 0

    mpi_comm = MPI.COMM_WORLD
    mpi_size = mpi_comm.size
    mpi_rank = mpi_comm.rank

    if mpi_rank == 0:
        print("using MPI with standard grid size: " + str(standard_grid_size))
        print("MPI size: " + str(mpi_size))

    if mpi_rank == 0:
        world = numpy.random.randint(
            2,
            size=(standard_grid_size, standard_grid_size, standard_grid_size)
        )

        if animate:

            population_type = "3d"
            population = Population3D(standard_grid_size, "seq")

            root = Tkinter.Tk()
            main_frame = MainFrame(root, population)

            animation = mpl_animation.FuncAnimation(
                main_frame.figure,
                update,
                interval=50
            )

            root.mainloop()
        else:
            while True:
                loop_no_animation()

    else:
        while True:
            world = mpi_comm.recv(source=0, tag=1)
            start_x = mpi_comm.recv(source=0, tag=2)
            end_x = mpi_comm.recv(source=0, tag=3)

            __calculate_section_of_world(start_x, end_x)

            mpi_comm.send(world, dest=0, tag=4)

