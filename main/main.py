import numpy
import matplotlib.animation as mpl_animation
import threadsafe_tkinter as Tkinter
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from model.c_population2d import Population2D
from model.c_population3d import Population3D
from view.c_inputs import Inputs
from view.c_main_frame import MainFrame


################################################################################
#                           Update functions                                   #
################################################################################
# @author   yxyxD
# @changes
#       2018-02-21 (yxyxD)  created
# @brief    Update function for 2-dimensional populations.
def animate_2d(data):

    if main_frame.is_paused:
        return

    main_frame.mat.set_data(main_frame.population.create_and_return_next_generation())
    main_frame.update_population_status()

    return


# @author   yxyxD
# @changes
#       2018-02-21 (yxyxD)  created
# @brief    Update function for 3-dimensional populations.
def animate_3d(data):

    if main_frame.is_paused:
        return

    main_frame.clear_axes()

    main_frame.axis.set_xlim([0, main_frame.population.get_grid_size()])
    main_frame.axis.set_ylim([0, main_frame.population.get_grid_size()])
    main_frame.axis.set_zlim([0, main_frame.population.get_grid_size()])

    main_frame.axis.set_xlabel("x")
    main_frame.axis.set_ylabel("y")
    main_frame.axis.set_zlabel("z")

    world = main_frame.population.create_and_return_next_generation()

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

    return


################################################################################
#                           Private Functions                                  #
################################################################################
# @author   yxyxD
# @changes
#       2018-02-21 (yxyxD)  created
# @brief    Creates the population based on user inputs.
def __setup_population():

    grid_size = Inputs.user_input_grid_size(population_type)
    mode = Inputs.user_input_mode()

    if population_type == Population3D.population_type:
        population = Population3D(grid_size, mode)
    else:
        population = Population2D(grid_size, mode)

    return population


# @author   yxyxD
# @changes
#       2018-02-21 (yxyxD)  created
# @brief    Creates the animation based on the type of the population.
def __setup_animation():

    if population_type == Population3D.population_type:
        animation = mpl_animation.FuncAnimation(
            main_frame.figure,
            animate_3d,
            interval=50
        )
    else:
        animation = mpl_animation.FuncAnimation(
            main_frame.figure,
            animate_2d,
            interval=50
        )

    return animation


################################################################################
#                           Main                                               #
################################################################################
# @author   yxyxD
# @changes
#       2018-02-21 (yxyxD)  created
# @brief    Main method.
if __name__ == '__main__':

    population_type = Inputs.user_input_population_type()
    population = __setup_population()

    animate = Inputs.user_input_animation()

    if animate:

        root = Tkinter.Tk()
        main_frame = MainFrame(root, population)
        animation = __setup_animation()

        root.mainloop()
    else:
        while True:
            population.create_and_return_next_generation()
            if population.get_iteration_count() % 5 == 0:
                print("Calculation speed = "
                      + str(round(population.get_calculation_speed(), 5))
                      + " iteration(s) per second"
                )
