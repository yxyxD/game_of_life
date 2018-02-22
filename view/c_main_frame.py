from old.c_population3d import Population3D
from old.c_population2d import Population2D

from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threadsafe_tkinter as Tkinter
import sys
from matplotlib.colors import ListedColormap


class MainFrame(Tkinter.Frame):

    ############################################################################
    #                           Constructor                                    #
    ############################################################################
    def __init__(self, root, population, *args, **kwargs):

        Tkinter.Frame.__init__(self, root, *args, **kwargs)

        self.root = root
        self.population = population
        self.is_paused = False

        if self.population.__class__.population_type == Population3D.population_type:
            self.__init_plot3d()
        if self.population.__class__.population_type == Population2D.population_type:
            self.__init_plot2d()

        self.__init_buttons()
        self.__init_labels()

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

    def __init_plot2d(self):

        self.figure = pyplot.figure()

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.show()

        self.axis = pyplot.subplot()

        color_map = ListedColormap(['white', 'blue'])
        self.mat = self.axis.matshow(self.population.get_world(), cmap=color_map)

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

    def __init_labels(self):

        self.label_info_grid_size = Tkinter.Label(
            self.root,
            text="Grid size: " + str(self.population.get_grid_size())
        )
        self.label_info_mode = Tkinter.Label(
            self.root,
            text="Calculation mode: " + str(self.population.get_mode())
        )
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

    def __init_layout(self):

        self.button_quit.grid(row=0, column=10)

        self.canvas.get_tk_widget().grid(row=1, column=0, rowspan=10, columnspan=3)

        self.label_info_grid_size.grid(row=1, column=3)
        self.label_info_mode.grid(row=2, column=3)

        self.label_info_iteration_count.grid(row=4, column=3)
        self.label_value_iteration_count.grid(row=4, column=4)
        self.label_info_total_time.grid(row=5, column=3)
        self.label_value_total_time.grid(row=5, column=4)
        self.label_info_iteration_speed.grid(row=6, column=3)
        self.label_value_iteration_speed.grid(row=6, column=4)

        self.button_pause.grid(row=11, column=0)
        self.button_continue.grid(row=11, column=1)
        self.button_restart.grid(row=11, column=2)

        return

    ############################################################################
    #                           Public Methods                                 #
    ############################################################################
    def clear_axes(self):

        pyplot.cla()

        return

    def update_population_status(self):

        self.value_iteration_count.set(str(self.population.get_iteration_count()))
        self.value_total_time.set(str(round(self.population.get_calculation_time(), 2)))
        self.value_iteration_speed.set(str(round(self.population.get_calculation_speed(), 5)))

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
