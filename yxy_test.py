from view.c_main_frame import MainFrame
import matplotlib.animation as mpl_animation
import numpy
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


def animate(data):

    mainframe.clearAxes()

    mainframe.ax.set_xlim([0, mainframe.grid_size])
    mainframe.ax.set_ylim([0, mainframe.grid_size])
    mainframe.ax.set_zlim([0, mainframe.grid_size])

    mainframe.ax.set_xlabel("x")
    mainframe.ax.set_ylabel("y")
    mainframe.ax.set_zlabel("z")

    world = mainframe.population.create_and_return_next_generation()

    for x in range(mainframe.population.get_grid_size()):
        for y in range(mainframe.population.get_grid_size()):
            for z in range(mainframe.population.get_grid_size()):

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

                    mainframe.ax.add_collection3d(Poly3DCollection(
                        sides, facecolors='blue', linewidths=1, edgecolors='black'
                    ))


if __name__ == '__main__':

    mainframe = MainFrame()

    animation = mpl_animation.FuncAnimation(
        mainframe.fig,
        animate,
        interval=50
    )

    mainframe.mainloop()
