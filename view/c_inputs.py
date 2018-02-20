from model.c_population3d import Population3D


class Inputs:

    @staticmethod
    def user_input_grid_size():
        standard_grid_size = Population3D.standard_grid_size

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
    def user_input_mode():
        standard_mode = Population3D.mode_sequential

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
