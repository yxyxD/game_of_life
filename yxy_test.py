from view.c_main_frame import MainFrame
import matplotlib.animation as mpl_animation
import numpy
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import threadsafe_tkinter as Tkinter
import threading


def animate_thread(data):

    threading.Thread(target=animate, args=(data,)).start()

    return


def animate(data):

    if plot3d.is_paused:
        return

    plot3d.clear_axes()

    plot3d.axis.set_xlim([0, plot3d.population.get_grid_size()])
    plot3d.axis.set_ylim([0, plot3d.population.get_grid_size()])
    plot3d.axis.set_zlim([0, plot3d.population.get_grid_size()])

    plot3d.axis.set_xlabel("x")
    plot3d.axis.set_ylabel("y")
    plot3d.axis.set_zlabel("z")

    world = plot3d.population.create_and_return_next_generation()

    for x in range(plot3d.population.get_grid_size()):
        for y in range(plot3d.population.get_grid_size()):
            for z in range(plot3d.population.get_grid_size()):

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

                    plot3d.axis.add_collection3d(Poly3DCollection(
                        sides, facecolors='blue', linewidths=1, edgecolors='black'
                    ))

    return


if __name__ == '__main__':

    root = Tkinter.Tk()
    root.wm_title("Game of life")

    plot3d = MainFrame(root)

    animation = mpl_animation.FuncAnimation(
        plot3d.figure,
        animate,
        interval=50
    )

    root.mainloop()
