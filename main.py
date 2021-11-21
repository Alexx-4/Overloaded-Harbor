from utils.harbor import Harbor
from plot.plot import plot, order_insert

def main():
    
    print('''
                PROYECTO DE SIMULACIóN. EVENTOS DISCRETOS
            

                          Alejandro Campos
                               C-411


                    Problema: Overloaded Harbor


                    Facultad de Matemática y Computación 
                         Universidad de La Habana
                                  2021
             
             ''')

    while True:
        try:
            simulation_time = int(input("\n\n\n\nEnter limit time in hours --->  "))

            docks = input("Enter number of docks (*optional*) --->  ")
            if docks: docks = int(docks)

            number_of_simulations = input("Enter number of simulations (*optional*) --->  ")
            number_of_simulations = int(number_of_simulations) if number_of_simulations else 1

            print('\n\n')

        except:
            print("\n\n***Please enter valid values.***\n\n") 
            continue
        

        mean_list = []
        tankers_list = []
        time_list = []

        for _ in range(number_of_simulations):
            harbor = Harbor(simulation_time, docks) if docks else Harbor(simulation_time)

            mean, tankers, time = harbor.run_simulation()
            order_insert(tankers, mean, time, tankers_list, mean_list, time_list)

        #### crea graficas para analizar los datos obtenidos en las simulaciones ####
        plot(tankers_list, time_list, mean_list)

        _input = ''
        while _input != 'exit':
            _input = input("Press enter to continue or type command 'exit'.   > ")
            if _input == '': break
        else: break


if __name__== '__main__': main()