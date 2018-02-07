import model.c_population as mdl_population

import matplotlib.pyplot as mpl_pyplot
import matplotlib.animation as mpl_animation


################################################################################
#                           Update Method for Animation                        #
################################################################################
def update(data):

    mat.set_data(population.create_and_return_next_generation())
    return [mat]

################################################################################
#                           Starting Point                                     #
################################################################################
if __name__ == '__main__':

    population = mdl_population.Population(100)

    fig, ax = mpl_pyplot.subplots()
    mat = ax.matshow(population.world)

    animation = mpl_animation.FuncAnimation(
        fig,
        update,
        interval=200,
        save_count=50
    )

    mpl_pyplot.show()

