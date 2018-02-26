import threadsafe_tkinter as Tkinter
import sys
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.colors import ListedColormap

from model.c_population import Population
from model.c_population3d import Population3D
from model.c_population2d import Population2D

import multiprocessing

import numpy
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.animation import FuncAnimation


class MainFrame(Tkinter.Frame):

    ############################################################################
    #                           Constructor                                    #
    ############################################################################
    # @author   yxyxD
    # @changes
    #       2018-02-21 (yxyxD)  created
    # @brief    Creates a new MainFrame to display a population.
    def __init__(self, root, population, *args, **kwargs):

        Tkinter.Frame.__init__(self, root, *args, **kwargs)

        self.root = root
        self.population = population
        self.is_paused = False

        self.root.wm_title("Game of life")
        self.root.protocol("WM_DELETE_WINDOW", self.__quit)

        self.__init_plot()
        self.__init_buttons()
        self.__init_labels()
        self.__init_layout()

        return

    ############################################################################
    #                           Initialising                                   #
    ############################################################################
    # @author   yxyxD
    # @changes
    #       2018-02-26 (yxyxD)  created
    # @brief    Initialises the plot to display the population.
    def __init_plot(self):

        self.figure = pyplot.figure()

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.show()

        if self.population.__class__.population_type == Population2D.population_type:
            self.__init_plot2d()
        if self.population.__class__.population_type == Population3D.population_type:
            self.__init_plot3d()

        return

    # @author   yxyxD
    # @changes
    #       2018-02-21 (yxyxD)  created
    # @brief    Initialises the plot to display a 3-dimensional population.
    def __init_plot3d(self):

        self.axis = Axes3D(self.figure)

        return

    # @author   yxyxD
    # @changes
    #       2018-02-21 (yxyxD)  created
    # @brief    Initialises the plot to display a 2-dimensional population
    def __init_plot2d(self):

        self.axis = pyplot.subplot()

        color_map = ListedColormap(['white', 'blue'])
        self.mat = self.axis.matshow(self.population.get_world(), cmap=color_map)

        return

    # @author   yxyxD
    # @changes
    #       2018-02-21 (yxyxD)  created
    # @brief    Initialises the buttons.
    def __init_buttons(self):

        self.button_pause = Tkinter.Button(
            self.root,
            text="Pause",
            command=self.__pause
        )
        self.button_continue = Tkinter.Button(
            self.root,
            text="Continue",
            command=self.__continue
        )

        return

    # @author   yxyxD
    # @changes
    #       2018-02-21 (yxyxD)  created
    # @brief    Initialises the labels.
    def __init_labels(self):

        self.label_info_iteration_count = Tkinter.Label(
            self.root,
            text="Number of Iterations: "
        )
        self.label_info_total_time = Tkinter.Label(
            self.root,
            text="Total calculation time (in seconds): "
        )
        self.label_info_iteration_speed = Tkinter.Label(
            self.root,
            text="Iterations per second: "
        )

        self.value_iteration_count = Tkinter.StringVar()
        self.value_iteration_count.set(str(0))
        self.label_value_iteration_count = Tkinter.Label(
            self.root,
            textvariable=self.value_iteration_count,
            width=15
        )
        self.value_total_time = Tkinter.StringVar()
        self.value_total_time.set(str(0))
        self.label_value_total_time = Tkinter.Label(
            self.root,
            textvariable=self.value_total_time,
            width=15
        )
        self.value_iteration_speed = Tkinter.StringVar()
        self.value_iteration_speed.set(str(0))
        self.label_value_iteration_speed = Tkinter.Label(
            self.root,
            textvariable=self.value_iteration_speed,
            width=15
        )

        return

    # @author   yxyxD
    # @changes
    #       2018-02-21 (yxyxD)  created
    # @brief    Initialises the layout by placing every GUI-component on the
    #           MainFrame.
    def __init_layout(self):

        self.canvas.get_tk_widget().grid(row=0, column=0, rowspan=10, columnspan=2)

        self.label_info_iteration_count.grid(row=4, column=3)
        self.label_value_iteration_count.grid(row=4, column=4)
        self.label_info_total_time.grid(row=5, column=3)
        self.label_value_total_time.grid(row=5, column=4)
        self.label_info_iteration_speed.grid(row=6, column=3)
        self.label_value_iteration_speed.grid(row=6, column=4)

        self.button_pause.grid(row=11, column=0)
        self.button_continue.grid(row=11, column=1)

        return

    ############################################################################
    #                           Public Methods                                 #
    ############################################################################
    # @author   yxyxD
    # @changes
    #       2018-02-21 (yxyxD)  created
    # @brief    Clears the content of the grid (only necessary for 3d-plots).
    def clear_axes(self):

        pyplot.cla()

        return

    # @author   yxyxD
    # @changes
    #       2018-02-21 (yxyxD)  created
    # @brief    Updates the status labels for the generation.
    def update_population_status(self):

        self.value_iteration_count.set(str(self.population.get_iteration_count()))
        self.value_total_time.set(str(round(self.population.get_calculation_time(), 2)))
        self.value_iteration_speed.set(str(round(self.population.get_calculation_speed(), 5)))

        return

    ############################################################################
    #                           Private Methods                                #
    ############################################################################
    # @author   yxyxD
    # @changes
    #       2018-02-21 (yxyxD)  created
    # @brief    Pauses the animation of the population development.
    def __pause(self):

        self.is_paused = True

        return

    # @author   yxyxD
    # @changes
    #       2018-02-21 (yxyxD)  created
    # @brief    Continues the animation of a paused population development.
    def __continue(self):

        self.is_paused = False

        return

    # @author   yxyxD
    # @changes
    #       2018-02-21 (yxyxD)  created
    # @brief    Ends the program.
    def __quit(self):

        sys.exit()
