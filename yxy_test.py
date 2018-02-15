import pprint
import numpy
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection

if __name__ == '__main__':

    fig = pyplot.figure()
    ax = Axes3D(fig)

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")

    grid_size = 3
    data = numpy.random.randint(2, size=(grid_size, grid_size, grid_size))
    # print(data)
    # x, y, z = data.nonzero()
    # ax.scatter(x, y, z, zdir='z', c='red')

    ax.set_xlim([0, grid_size])
    ax.set_ylim([0, grid_size])
    ax.set_zlim([0, grid_size])

    d = 0.5
    for x in range(grid_size):
        for y in range(grid_size):
            for z in range(grid_size):

                if data[x][y][z] == 1:
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

                    pprint.PrettyPrinter().pprint(points)

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

    pyplot.show()
