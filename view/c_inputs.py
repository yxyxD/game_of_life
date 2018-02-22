from old.c_population2d import Population2D
from old.c_population3d import Population3D


class Inputs:

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

    @staticmethod
    def user_input_mode(population_type):

        if population_type == Population3D.population_type:
            standard_mode = Population3D.mode_sequential
        else:
            standard_mode = Population2D.mode_sequential

        user_input = input(
            "Please enter the requested __mode - sequential or parallel ([s] / p): "
        )

        try:
            if (user_input == 's') or (user_input == 'S'):
                mode = Population3D.mode_sequential
            elif (user_input == 'p') or (user_input == 'P'):
                mode = Population3D.mode_parallel
            else:
                mode = standard_mode
        except ValueError:
            mode = standard_mode

        print("Selected __mode: " + mode)

        return mode
