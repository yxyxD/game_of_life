from model.c_population import Population
from model.c_population2d import Population2D
from model.c_population3d import Population3D


class Inputs:

    # @author   yxyxD
    # @changes
    #       2018-02-21 (yxyxD)  created
    # @brief    Requests the population type (2d or 3d) from the user.
    @staticmethod
    def user_input_population_type():

        standard_population_type = Population3D.population_type

        user_input = input(
            "Please enter the population type (["
            + standard_population_type + "] / "
            + Population2D.population_type + " ): "
        )

        try:
            if user_input == Population3D.population_type:
                population_type = Population3D.population_type
            elif user_input == Population2D.population_type:
                population_type = Population2D.population_type
            else:
                population_type = standard_population_type
        except ValueError:
            population_type = standard_population_type

        print("Selected population type: " + population_type)

        return population_type

    # @author   yxyxD
    # @changes
    #       2018-02-21 (yxyxD)  created
    # @brief    Requests the grid size from the user.
    @staticmethod
    def user_input_grid_size(population_type):

        if population_type == Population3D.population_type:
            standard_grid_size = Population3D.standard_grid_size
        else:
            standard_grid_size = Population2D.standard_grid_size

        user_input = input(
            "Please enter the grid size [" + str(standard_grid_size) + "]: "
        )

        try:
            value = int(user_input)
            if value > 0:
                grid_size = value
            else:
                grid_size = standard_grid_size
        except ValueError:
            grid_size = standard_grid_size

        print("Selected grid size: " + str(grid_size))

        return grid_size

    # @author   yxyxD
    # @changes
    #       2018-02-21 (yxyxD)  created
    # @brief    Requests the calculation mode (parallel, sequential) form the
    #           user.
    @staticmethod
    def user_input_mode():

        standard_mode = Population.mode_sequential

        user_input = input(
            "Please enter the requested mode - sequential or parallel ([s] / p): "
        )

        try:
            if (user_input == 's') or (user_input == 'S'):
                mode = Population.mode_sequential
            elif (user_input == 'p') or (user_input == 'P'):
                mode = Population.mode_parallel
            else:
                mode = standard_mode
        except ValueError:
            mode = standard_mode

        print("Selected mode: " + mode)

        return mode

    # @author   marxmanEUW
    # @changes
    #       2018-03-09 (marxmanEUW)  created
    # @brief    Requests the animation mode.
    @staticmethod
    def user_input_animation():

        standard_animation = True

        user_input = input(
            "Please enter animation type - UI or console ([u] / c): "
        )

        try:
            if user_input == 'u':
                animation = True
            elif user_input == 'c':
                animation = False
            else:
                animation = standard_animation
        except ValueError:
            animation = standard_animation

        return animation
