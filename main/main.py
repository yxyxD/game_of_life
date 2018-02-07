import model.c_population as mdl_population

import matplotlib.pyplot as mpl_pyplot
import matplotlib.animation as mpl_animation


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
# @brief    Starting point of the program.
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

