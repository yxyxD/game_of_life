################################################################################
#                   @TODO obsolete Klasse
################################################################################
from model.c_population3d import Population3D

import numpy
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as mpl_animation
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import threadsafe_tkinter as tk
import sys


################################################################################
#                           User Input Functions                               #
################################################################################
# @author   yxyxD
# @changes
#       2018-02-08 (yxyxD)  created
# @brief    Requests the grid size from the user. If the input is incorrect
#           the standard_grid_size will be used instead.
def __user_input_grid_size():
    standard_grid_size = Population3D.standard_grid_size

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
    standard_mode = Population3D.mode_sequential

    user_input = input(
        "Please enter the requested __mode - sequential or parallel ([s] / p): "
    )

    try:
        if (user_input == 's') or (user_input == 'S'):
            mode = Population3D.mode_sequential
        elif (user_input == 'p') or (user_input == 'P'):
            mode = Population3D.mode_parallel
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
    max_cores = Population3D.cpu_count

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

    pyplot.cla()

    ax.set_xlim([0, grid_size])
    ax.set_ylim([0, grid_size])
    ax.set_zlim([0, grid_size])

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")

    world = population.create_and_return_next_generation()
    # print(world)

    for x in range(population.get_grid_size()):
        for y in range(population.get_grid_size()):
            for z in range(population.get_grid_size()):

                if world[x][y][z] == 1:
                    points = numpy.array([
                        [(x),     (y),     (z)],        # [0] down lower left
                        [(x + 1), (y),     (z)],        # [1] down lower right
                        [(x),     (y + 1), (z)],        # [2] down upper left
                        [(x + 1), (y + 1), (z)],        # [3] down upper right
                        [(x),     (y),     (z + 1)],    # [4] up lower left
                        [(x + 1), (y),     (z + 1)],    # [5] up lower right
                        [(x),     (y + 1), (z + 1)],    # [6] up upper left
                        [(x + 1), (y + 1), (z + 1)]     # [7] up upper right
                    ])

                    sides = [
                        [points[0], points[1], points[3], points[2]],   # bottom
                        [points[0], points[1], points[5], points[4]],   # front
                        [points[0], points[2], points[6], points[4]],   # left
                        [points[1], points[3], points[7], points[5]],   # right
                        [points[2], points[3], points[7], points[6]],   # back
                        [points[4], points[5], points[7], points[6]]    # top
                    ]

                    # ax.scatter3D(points[:, 0], points[:, 1], points[:, 2])
                    ax.add_collection3d(Poly3DCollection(
                        sides, facecolors='blue', linewidths=1, edgecolors='black'
                    ))

    __user_output_calculation_speed()

    return


def quit():
    sys.exit()


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

    population = Population3D(grid_size, mode)

    root = tk.Tk()

    label = tk.Label(root, text="SHM Simulation").grid(column=0, row=0)

    fig = pyplot.figure()
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().grid(column=0, row=1)

    tk.Button(root, text="Quit", command=quit).grid(column=1, row=1)

    ax = Axes3D(fig)

    animation = mpl_animation.FuncAnimation(
        fig,
        update,
        interval=50
    )

    # pyplot.show()

    tk.mainloop()
