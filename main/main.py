from model.c_population import Population

import matplotlib.pyplot as mpl_pyplot
import matplotlib.animation as mpl_animation

from matplotlib.colors import ListedColormap


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
#                           Starting Point                                     #
################################################################################
# @author   yxyxD
# @changes
#       2018-02-06 (yxyxD)  created
#       2018-02-08 (yxyxD)  implemented user inputs for console
# @brief    Starting point of the program.
if __name__ == '__main__':
    grid_size = __user_input_grid_size()
    mode = __user_input_mode()
    # @todo implement core number choice for parallel calculation

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


