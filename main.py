from utils.harbor import Harbor

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
        simulation_time = int(input("\n\n\n\nEnter simulation time in minutes --->  "))

        docks = input("Enter number of docks (*optional*) --->  ")
        if docks: docks = int(docks)

        number_of_simulations = input("Enter number of simulations (*optional*) --->  ")
        number_of_simulations = int(number_of_simulations) if number_of_simulations else 1

        print('\n\n')

    except: 
        print("\n\n***Please enter valid values.***\n\n") 
        continue
    
    for _ in range(number_of_simulations):
        harbor = Harbor(simulation_time, docks) if docks else Harbor(simulation_time)
        harbor.run_simulation()
    
    if input("Press enter to continue or type command 'exit'.   > ") == 'exit': break