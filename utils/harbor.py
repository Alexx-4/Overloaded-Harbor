from utils.utils import exponential
from utils.tanker import Tanker

from enum import IntEnum


'''
Enum que guarda las posibles posiciones de un remolcador
'''
class Location(IntEnum):
    PORT = 0
    MOVING = -1
    DOCK = 1


'''
Clase principal donde se desarrolla la simulacion
'''
class Harbor:
    '''
    Inicia con un tiempo de simulacion a partir del cual ya no entrara ningun otro tanquero pero atiende
    a aquellos tanqueros en espera.
    Tambien podemos modificar el numero de muelles en la simulacion (por defecto 3)
    '''
    def __init__(self, simulation_time, docks = 3):
        self.simulation_time = simulation_time * 60
        self.free_docks = docks

        # en la primera lista se guardaran los tanqueros que estan en
        # el tiempo T en el puertos; y en la segunda se guarda el tiempo
        # que cada tanquero que abandona el Puerto estuvo en el
        self.pending_tankers = []
        self.tankers_time = []

        # tiempo T de la simulacion, localizacion del remolcador y
        # cantidad de taqueros q han pasado por el puerto, respectivamente
        self.time = 0
        self.tug = Location.DOCK
        self.count = 0
    

    '''
    Se genera el tiempo de un nuevo arribo si aun no hemos superado
    el tiempo limite
    '''
    def next_arrival(self):
        time = exponential(8) * 60 + self.time
        if time <= self.simulation_time:
            self.count += 1
            tanker = Tanker(self.count, time, self.arrival)

            # order_join garantiza que pending_tankers siempre se mantenga ordenada en forma creciente
            # ya que al annadir un tanquero a la cola este metodo lo inserta sin romper el orden
            tanker.order_join(self.pending_tankers)

        return True
    

    '''
    Se ejecuta un nuevo arribo de un tanquero al puerto
    '''
    def arrival(self, tanker):
        self.time = tanker.arrival_time
        tanker.Event = self.move_to_dock
        self.next_arrival()
        print(f'Tanker {tanker.id} is arriving to the port.     Time: {self.time}')

        return True


    '''
    Si el remolcador esta libre y hay muelles desocupados, este metodo realiza el
    movimiento de un tanquero a un muelle
    '''
    def move_to_dock(self, tanker):
        if self.tug != Location.MOVING and self.free_docks > 0:
            self.move_tug(Location.PORT)
            self.tug = Location.MOVING
            tanker.current_time = self.time + exponential(2) * 60
            tanker.Event = self.load
            tanker.order_join(self.pending_tankers)

            print(f'Moving tanker {tanker.id} to a dock.     Time: {self.time}')
            return True
        return False


    '''
    Metodo encargado de mover el remolcador hacia la localizacion indicada
    '''
    def move_tug(self, location):
        if self.tug != location:
            self.time += exponential(15)
            self.tug = Location(1 - location.value)

            print(f'Moving tug to {location.name}.     Time: {self.time}')
    

    '''
    Metodo que simula el momento que un tanquero llega al muelle y 
    comienza la carga
    '''
    def load(self, tanker):
        self.time = tanker.current_time
        self.free_docks -= 1
        self.tug  = Location.DOCK

        tanker.current_time = tanker.load_time() + self.time
        tanker.Event = self.ready
        tanker.order_join(self.pending_tankers)

        print(f'Tanker {tanker.id} arrived to a dock. Loading...     Time: {self.time}')
        return True
    

    '''
    Se ejecuta cuando un tanquero termino de cargar y esta listo para regresar
    al puerto
    '''
    def ready(self, tanker):
        self.time = tanker.current_time
        tanker.Event = self.move_to_port
        tanker.order_join(self.pending_tankers)

        print(f'Tanker {tanker.id} already finished loading. Its ready to go to the port.     Time: {self.time}')
        return True
    

    '''
    Si el remolcador no esta ocupado se realiza el movimiento del 
    tanquero hacia el puerto
    '''
    def move_to_port(self, tanker):
        if self.tug != Location.MOVING:
            self.move_tug(Location.DOCK)
            self.free_docks += 1
            self.tug = Location.MOVING

            tanker.current_time = self.time + exponential(2) * 60
            tanker.Event = self.departure
            tanker.order_join(self.pending_tankers)

            print(f'Moving tanker {tanker.id} to the port.     Time: {self.time}')
            return True
        return False
    

    '''
    Momento en el tanquero llega al puerto y sale de la simulacion
    '''
    def departure(self, tanker):
        self.time = tanker.departure_time = tanker.current_time
        self.tug = Location.PORT
        self.tankers_time.append(tanker.time_in_harbor() / 60)

        self.pending_tankers.remove(tanker)

        print(f'Tanker {tanker.id} is leaving the harbor.     Time: {self.time}')
        return True
    

    '''
    Metodo que inicia la simulacion
    '''
    def run_simulation(self):
        print('Starting a new simulation....\n')
        self.next_arrival()

        while self.pending_tankers:
           assert any(tanker.Event(tanker) for tanker in self.pending_tankers), "Simulation crashed"
            
        print(f'\n\n\nSimulation finished.   Duration: {self.time / 60} hours.   Tankers served: {len(self.tankers_time)}')

        self.mean()


    '''
    Calcula la media del tiempo de los tanqueros en el puerto
    '''
    def mean(self):
        _mean = sum(self.tankers_time) / len(self.tankers_time)
        print(f'\nMean of tankers time in harbor: {_mean} hours aprox.')
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n\n')