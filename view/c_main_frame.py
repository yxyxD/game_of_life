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

        if self.population.__class__.population_type == Population2D.population_type:
            self.__init_plot2d()
        if self.population.__class__.population_type == Population3D.population_type:
            self.__init_plot3d()

        self.__init_inputs()
        self.__init_buttons()
        self.__init_labels()
        self.__init_layout()

        return

    ############################################################################
    #                           Initialising                                   #
    ############################################################################
    def __init_inputs(self):

        self.__type_select = Tkinter.Listbox(
            self.root,
            selectmode='single',
            exportselection=0,
            width=Population3D.population_type.__len__(),
            height=2
        )
        self.__type_select.insert('end', Population2D.population_type)
        self.__type_select.insert('end', Population3D.population_type)
        self.__type_select.select_set(0)

        vcmd = (self.root.register(self.__validate_grid_size), '%d', '%P', '%S')
        self.__value_grid_size_select = Tkinter.StringVar()
        self.__grid_size_select = Tkinter.Entry(
            self.root,
            width=6,
            textvariable=self.__value_grid_size_select,
            validate='key',
            validatecommand=vcmd
        )
        self.__value_grid_size_select.set(str(Population2D.standard_grid_size))

        self.__mode_select = Tkinter.Listbox(
            self.root,
            selectmode='single',
            exportselection=0,
            width=Population.mode_sequential.__len__(),
            height=2
        )
        self.__mode_select.insert('end', Population.mode_sequential)
        self.__mode_select.insert('end', Population.mode_parallel)
        self.__mode_select.select_set(0)

        div, mod = divmod(multiprocessing.cpu_count(), 10)
        self.__core_select = Tkinter.Listbox(
            self.root,
            selectmode='single',
            exportselection=0,
            width=div + 1,
            height=multiprocessing.cpu_count() - 1
        )
        for i in range(2, multiprocessing.cpu_count() + 1):
            self.__core_select.insert('end', str(i))
        self.__core_select.select_set(self.__core_select.size() - 1)

        return

    # @author   yxyxD
    # @changes
    #       2018-02-21 (yxyxD)  created
    # @brief    Initialises the plot to display a 3-dimensional population.
    def __init_plot3d(self):

        self.figure = pyplot.figure()

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.show()

        self.axis = Axes3D(self.figure)

        return

    # @author   yxyxD
    # @changes
    #       2018-02-21 (yxyxD)  created
    # @brief    Initialises the plot to display a 2-dimensional population
    def __init_plot2d(self):

        self.figure = pyplot.figure()

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.show()

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
        self.button_start = Tkinter.Button(
            self.root,
            text="Start",
            command=self.__start
        )

        return

    # @author   yxyxD
    # @changes
    #       2018-02-21 (yxyxD)  created
    # @brief    Initialises the labels.
    def __init_labels(self):

        self.label_type = Tkinter.Label(
            self.root,
            text="Population type: "
        )
        self.label_grid_size = Tkinter.Label(
            self.root,
            text="Grid size: "
        )
        self.label_mode = Tkinter.Label(
            self.root,
            text="Calculation mode: "
        )
        self.label_core_count = Tkinter.Label(
            self.root,
            text="Core count: "
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

    # @author   yxyxD
    # @changes
    #       2018-02-21 (yxyxD)  created
    # @brief    Initialises the layout by placing every GUI-component on the
    #           MainFrame.
    def __init_layout(self):

        self.canvas.get_tk_widget().grid(row=1, column=0, rowspan=10, columnspan=2)

        self.label_type.grid(row=2, column=3)
        self.__type_select.grid(row=2, column=4)
        self.label_grid_size.grid(row=3, column=3)
        self.__grid_size_select.grid(row=3, column=4)
        self.label_mode.grid(row=4, column=3)
        self.__mode_select.grid(row=4, column=4)
        self.label_core_count.grid(row=5, column=3)
        self.__core_select.grid(row=5, column=4)

        self.button_start.grid(row=6, column=3, columnspan=2)

        self.label_info_iteration_count.grid(row=8, column=3)
        self.label_value_iteration_count.grid(row=8, column=4)
        self.label_info_total_time.grid(row=9, column=3)
        self.label_value_total_time.grid(row=9, column=4)
        self.label_info_iteration_speed.grid(row=10, column=3)
        self.label_value_iteration_speed.grid(row=10, column=4)

        self.button_pause.grid(row=11, column=0)
        self.button_continue.grid(row=11, column=1)

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
    # @brief    Restarts the population development by setting up a new randomly
    #           created generation.
    def __start(self):

        type = self.__type_select.get(self.__type_select.curselection()[0])
        str_grid_size = self.__grid_size_select.get()
        mode = self.__mode_select.get(self.__mode_select.curselection()[0])

        try:
            grid_size = int(str_grid_size)
        except ValueError:
            if type == Population2D:
                grid_size = Population2D.standard_grid_size
            else:
                grid_size = Population3D.standard_grid_size
            self.__value_grid_size_select.set(str(grid_size))

        if type == Population2D.population_type:
            self.population = Population2D(grid_size, mode)
            print('yea 2d')
            self.__init_plot2d()

        if type == Population3D.population_type:
            self.population = Population3D(grid_size, mode)
            print('yea 3d')
            self.__init_plot3d()

        self.__continue()

        return

    def __validate_grid_size(self, action, value_if_allowed, text):

        is_valid = False

        if action == '1':
            if text in '0123456789':
                try:
                    int(value_if_allowed)
                    is_valid = True
                except ValueError:
                    is_valid = False
        else:
            is_valid = True

        return is_valid

    # @author   yxyxD
    # @changes
    #       2018-02-21 (yxyxD)  created
    # @brief    Ends the program.
    def __quit(self):

        sys.exit()
