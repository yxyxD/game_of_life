class Outputs:

    @staticmethod
    def __user_output_calculation_speed(population):
        if population.get_iteration_count() % 5 == 0:
            print(
                "Calculation speed = "
                + str(round(population.get_calculation_speed(), 5))
                + " iteration(s) per second"
            )

        return
