class Outputs:

    # @author   yxyxD
    # @changes
    #       2018-02-21 (yxyxD)  created
    # @brief    Prints the amount of iterations calculated per second on
    #           console. There will be one output after 5 iterations.
    @staticmethod
    def __user_output_calculation_speed(population):
        if population.get_iteration_count() % 5 == 0:
            print(
                "Calculation speed = "
                + str(round(population.get_calculation_speed(), 5))
                + " iteration(s) per second"
            )

        return
