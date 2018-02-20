from model.c_population3d import Population3D

import numpy
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as mpl_animation
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import threadsafe_tkinter as Tkinter
import sys

from view.c_inputs import Inputs


class MainFrame(Tkinter.Tk):

    def __init__(self, *args, **kwargs):

        Tkinter.Tk.__init__(self, *args, **kwargs)
        Tkinter.Tk.wm_title(self, "Game of Life")

        self.grid_size = Population3D.standard_grid_size
        self.mode = Population3D.mode_sequential
        self.population = Population3D(self.grid_size, self.mode)

        self.fig = pyplot.figure()
        self.ax = Axes3D(self.fig)

        self.__setup_main_frame()

        return

    def __setup_main_frame(self):

        plot = FigureCanvasTkAgg(self.fig, master=self).get_tk_widget()
        plot.grid(column=0, row=0)

        Tkinter.Button(self, text="Quit", command=self.__quit).grid(column=0, row=1)

        return

    def __quit(self):
        sys.exit()

    def clearAxes(self):
        pyplot.cla()
