from model.c_population import Population

import matplotlib.pyplot as mpl_pyplot
import matplotlib.animation as mpl_animation

from matplotlib.colors import ListedColormap

from mpi4py import MPI

################################################################################
#                           User Input Functions                               #
################################################################################
# @author   yxyxD
# @changes
#       2018-02-08 (yxyxD)  created
# @brief    Requests the grid size from the user. If the input is incorrect
#           the standard_grid_size will be used instead.
def __user_input_grid_size():
    standard_grid_size = Population.standard_grid_size

    user_input = input(
        "Please enter the grid size [" + str(standard_grid_size) + "]: "
    )

    try:
        value = int(user_input)
        if value > 0:
            grid_size = value
        else:
            grid_size = standard_grid_size
    except ValueError:
        grid_size = standard_grid_size

    print("Selected grid size: " + str(grid_size))

    return grid_size


# @author   yxyxD
# @changes
#       2018-02-08 (yxyxD)  created
# @brief    Requests the calculation __mode from the user. If the input is
#           incorrect the standard_mode will be used instead.
def __user_input_mode():
    standard_mode = Population.mode_sequential

    user_input = input(
        "Please enter the requested __mode - sequential or parallel ([s] / p): "
    )

    try:
        if (user_input == 's') or (user_input == 'S'):
            mode = Population.mode_sequential
        elif (user_input == 'p') or (user_input == 'P'):
            mode = Population.mode_parallel
        else:
            mode = standard_mode
    except ValueError:
        mode = standard_mode

    print("Selected __mode: " + mode)

    return mode

# @author   yxyxD
# @changes
#       2018-02-11 (yxyxD)  created
# @brief    Requests the number of cores (threads) that should be used for the
#           parallel caluclation from the user
def __user_input_cores_for_parallel_calculation():
    min_cores = 2
    max_cores = Population.cpu_count

    user_input = input(
        "Please enter the number of cores that shall be used for the parallel calculation "
        + "(min: " + str(min_cores) + " / [max: " + str(max_cores) + "]): "
    )

    try:
        value = int(user_input)
        if value < min_cores:
            used_cores = min_cores
        elif value > max_cores:
            used_cores = max_cores
        else:
            used_cores = value
    except ValueError:
        used_cores = max_cores

    return used_cores


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

    mat.set_data(population.create_and_return_next_generation())
    __user_output_calculation_speed()
    return [mat]


################################################################################
#                           Test Methods                                       #
################################################################################

def __calculate_section_of_world_mpi(world_calc, x_min_calc, x_max_calc):

    new_world_calc = world_calc.copy()

    for x in range(x_min_calc, x_max_calc):
        for y in range(world_calc.__len__()):
            neighbor_count = __get_neighbor_count_mpi(world_calc, x, y)
            if world_calc[x, y] == 1:
                if neighbor_count < 2:
                    new_world_calc[x, y] = 0
                elif neighbor_count == 2 or neighbor_count == 3:
                    new_world_calc[x, y] = 1
                elif neighbor_count > 3:
                    new_world_calc[x, y] = 0
            elif world_calc[x, y] == 0:
                if neighbor_count == 3:
                    new_world_calc[x, y] = 1

    return new_world_calc


def __get_neighbor_count_mpi(world, x, y):
    size = world.__len__()

    count = 0

    for i in [x - 1, x, x + 1]:
        for j in [y - 1, y, y + 1]:

            if (i == x) and (j == y):
                continue

            if (i != size) and (j != size):
                count += world[i][j]
            elif (i == size) and (j != size):
                count += world[0][j]
            elif (i != size) and (j == size):
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

    mpi_comm = MPI.COMM_WORLD
    mpi_size = mpi_comm.size
    mpi_rank = mpi_comm.rank

    if mpi_size > 1:
        grid_size = Population.standard_grid_size
        mode = Population.mode_mpi
        if mpi_rank == 0:
            print("using MPI with standard grid size: " + str(grid_size))
            print("MPI size: " + str(mpi_size))
    else:
        grid_size = __user_input_grid_size()
        mode = __user_input_mode()
        # @todo implement core number choice for parallel calculation

    if mpi_rank == 0:
        print("")
        print("Program started")
        print("")

        population = Population(grid_size, mode)

        fig, ax = mpl_pyplot.subplots()

        cmap = ListedColormap(['white', 'black'])
        mat = ax.matshow(population.get_world(), cmap=cmap)

        animation = mpl_animation.FuncAnimation(
            fig,
            update,
            interval=50
        )

        mpl_pyplot.show()
    else:
        while True:
            partial_world = mpi_comm.recv(source=0, tag=1)
            x_min = mpi_comm.recv(source=0, tag=2)
            x_max = mpi_comm.recv(source=0, tag=3)

            new_partial_world = __calculate_section_of_world_mpi(partial_world, x_min, x_max)

            mpi_comm.send(new_partial_world, dest=0, tag=4)

