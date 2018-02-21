from view.c_main_frame import MainFrame
import matplotlib.animation as mpl_animation
import numpy
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import threadsafe_tkinter as Tkinter
from view.c_inputs import Inputs
from model.c_population3d import Population3D
from model.c_population2d import Population2D


def animate_2d(data):

    main_frame.mat.set_data(main_frame.population.create_and_return_next_generation())
    main_frame.update_population_status()

    return [main_frame.mat]


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


def __setup_population():

    grid_size = Inputs.user_input_grid_size(population_type)
    mode = Inputs.user_input_mode(population_type)

    if population_type == Population3D.population_type:
        population = Population3D(grid_size, mode)
    else:
        population = Population2D(grid_size, mode)

    return population


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

if __name__ == '__main__':

    population_type = Inputs.user_input_population_type()

    population = __setup_population()

    root = Tkinter.Tk()
    root.wm_title("Game of life")

    main_frame = MainFrame(root, population)

    animation = __setup_animation()

    root.mainloop()
