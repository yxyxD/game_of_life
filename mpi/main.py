from mpi.c_population import Population

import matplotlib.pyplot as mpl_pyplot
import matplotlib.animation as mpl_animation

from matplotlib.colors import ListedColormap

import numpy

from mpi4py import MPI


standard_grid_size = 100

################################################################################
#                           User Output Functions                              #
################################################################################
# @author   yxyxD
# @changes
#       2018-02-11 (yxyxD)  created
# @brief    Prints the required calculation speed per generation.
def __user_output_calculation_speed():

    if population.get_iteration_count() % 5 == 0:
        print(
            "Calculation speed = "
              + str(round(population.get_calculation_speed(), 5))
              + " iteration(s) per second"
        )

    return


################################################################################
#                           Update Method for Animation                        #
################################################################################
# @author   yxyxD
# @changes
#       2018-02-07 (yxyxD)  created
# @brief    !!! IMPORTANT !!!
#           Updates the data grid for the animation. Do not change location or
#           parameter, unless you know what you are doing.
def update(data):

    #mat.set_data(population.create_and_return_next_generation())
    # hier muss weiter gearbeitet werden
    mat.set_data(world)
    __user_output_calculation_speed()
    return [mat]


################################################################################
#                           Test Methods                                       #
################################################################################

def __calculate_section_of_world():
    global grid_size
    global world
    global new_world
    global start_x
    global end_x

    new_world = world.copy()

    for x in range(start_x, end_x):
        for y in range(grid_size):
            neighbor_count = __get_neighbor_count()
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

    return


def __get_neighbor_count():
    global grid_size
    global world
    global new_world
    global start_x
    global end_x

    count = 0

    for i in [x - 1, x, x + 1]:
        for j in [y - 1, y, y + 1]:

            if (i == x) and (j == y):
                continue

            if (i != grid_size) and (j != grid_size):
                count += world[i][j]
            elif (i == grid_size) and (j != grid_size):
                count += world[0][j]
            elif (i != grid_size) and (j == grid_size):
                count += world[i][0]
            else:
                count += world[0][0]

    return count

################################################################################
#                           Starting Point                                     #
################################################################################
# @author   yxyxD
# @changes
#       2018-02-06 (yxyxD)  created
#       2018-02-08 (yxyxD)  implemented user inputs for console
# @brief    Starting point of the program.
if __name__ == '__main__':

    global grid_size
    global world
    global new_world
    global start_x
    global end_x

    mpi_comm = MPI.COMM_WORLD
    mpi_size = mpi_comm.size
    mpi_rank = mpi_comm.rank

    grid_size = standard_grid_size

    if mpi_rank == 0:
        print("using MPI with standard grid size: " + str(grid_size))
        print("MPI size: " + str(mpi_size))

    if mpi_rank == 0:
        print("")
        print("Program started")
        print("")

        world = numpy.random.randint(
            2,
            size=(grid_size, grid_size)
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
        while True:
            world = mpi_comm.recv(source=0, tag=1)
            start_x = mpi_comm.recv(source=0, tag=2)
            end_x = mpi_comm.recv(source=0, tag=3)

            __calculate_section_of_world()

            mpi_comm.send(new_world, dest=0, tag=4)

