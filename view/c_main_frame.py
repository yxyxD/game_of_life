from model.c_population3d import Population3D

import numpy
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as mpl_animation
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import threadsafe_tkinter as Tkinter
import sys


class MainFrame(Tkinter.Frame):

    ############################################################################
    #                           Constructor                                    #
    ############################################################################
    def __init__(self, root, *args, **kwargs):

        Tkinter.Frame.__init__(self, root, *args, **kwargs)

        self.root = root
        self.population = Population3D(10, "sequential")
        self.is_paused = False

        self.__init_plot3d()
        self.__init_buttons()

        self.__init_layout()

        return

    ############################################################################
    #                           Initialising                                   #
    ############################################################################
    def __init_plot3d(self):

        self.figure = pyplot.figure()

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.show()

        self.axis = Axes3D(self.figure)

        return

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
        self.button_restart = Tkinter.Button(
            self.root,
            text="Restart",
            command=self.__restart
        )
        self.button_quit = Tkinter.Button(
            self.root,
            text="Quit",
            command=self.__quit
        )

        return

    def __init_layout(self):

        self.canvas.get_tk_widget().grid(row=0, column=0, columnspan=3)
        self.button_pause.grid(row=1, column=0)
        self.button_continue.grid(row=1, column=1)
        self.button_restart.grid(row=1, column=2)
        self.button_quit.grid(row=1, column=4)

        return

    ############################################################################
    #                           Public Methods                                 #
    ############################################################################
    def clear_axes(self):

        pyplot.cla()

        return

    ############################################################################
    #                           Private Methods                                #
    ############################################################################
    def __pause(self):

        self.is_paused = True

        return

    def __continue(self):

        self.is_paused = False

        return

    def __restart(self):

        old_grid_size = self.population.get_grid_size()
        old_mode = self.population.get_mode()

        self.population = Population3D(old_grid_size, old_mode)

        self.is_paused = False

        return

    def __quit(self):

        sys.exit()
