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
        "Please enter the grid size (" + str(standard_grid_size) + "): ")

    try:
        value = int(user_input)
        if (value > 0):
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
# @brief    Requests the calculation mode from the user. If the input is
#           incorrect the standard_mode will be used instead.
def __user_input_mode():
    standard_mode = Population.mode_sequential

    user_input = input(
        "Please enter the requested mode - sequential or parallel (S / p): "
    )

    try:
        if (user_input == 's' or user_input == 'S'):
            mode = Population.mode_sequential
        elif (user_input == 'p' or user_input == 'P'):
            mode = Population.mode_parallel
        else:
            mode = standard_mode
    except ValueError:
        mode = standard_mode

    print("Selected mode: " + mode)

    return mode


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

    population = Population(grid_size, mode)

    fig, ax = mpl_pyplot.subplots()

    cmap = ListedColormap(['white', 'black'])
    mat = ax.matshow(population.world, cmap=cmap)

    animation = mpl_animation.FuncAnimation(
        fig,
        update,
        interval=100
    )

    mpl_pyplot.show()

