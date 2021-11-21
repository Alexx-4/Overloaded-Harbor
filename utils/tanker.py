from utils.utils import normal

from enum import IntEnum
import random as r


'''
Enum que guarda los posibles tamannos de un tanquero
'''
class Size (IntEnum):
    SMALL = 0
    MEDIUM = 1
    BIG = 2



'''
Clase que describe los tanqueros
'''
class Tanker:
    '''
    Para inicializar un tanquero debemos pasar el id, tiempo de arribo y
    el primer evento que ejecutara en el tiempo current_time
    '''
    def __init__(self, id, arrival_time, event):
        self.id = id
        self.arrival_time = arrival_time
        self.current_time = arrival_time
        self.Event = event

        self.size = self.get_size()
        self.departure_time = -1
        
    
    '''
    Devuelve la estancia de un tanquero en el Puerto
    '''
    def time_in_harbor(self): return self.departure_time - self.arrival_time


    '''
    Devuelve, atendiendo a las probabilidades dadas, el tamanno que tendra el tanquero
    El array de probabilidades puede variar, solo debe ingresarlo en orden creciente
    '''
    def get_size(self):
        P_size = [0.25, 0.25, 0.5]

        u = r.random()
        sum_p, i = 0, len(P_size)

        # recorre el array en reverso, comenzado con la
        # probabilidad mayor
        while i >= 0:
            i -= 1
            sum_p += P_size[i]
            if u <= sum_p:
                return Size(i)
    

    '''
    Atendiendo a los diferentes parametros de la distribucion normal dados segun el 
    tamanno del tanquero, este metodo devuelve el tiempo de carga de este en el muelle
    '''
    def load_time(self):
        params = [(9,1), (12,2), (18,3)]

        miu, o_2 = params[self.size.value]
        return normal(miu, o_2) * 60


    '''
    Inserta la instancia de la clase en list (lista ordenada de forma creciente 
    atendiendo al tiempo que cada tanquero lleva en la simulacion), de forma tal que 
    la lista mantiene el orden despues de la insercion 
    '''
    def order_join(self, list):
        try: list.remove(self)
        except ValueError: pass

        list.append(self)

        i = len(list) - 2

        while i >= 0:
            if list[i] > self:
                list[i+1] = list[i]
                list[i] = self
            i -= 1


    '''
    Define el operador > para comparar una clase tanker con otra atendiendo al tiempo que cada 
    tanquero lleva en la simulacion. Si este tiempo es el mismo es mayor (tiene menos precedencia) 
    aquel tanquero cuyo tiempo de llegada es mayor (lleva menos tiempo en el sistema) 
    '''
    def __gt__(self, other_tanker):
        return self.arrival_time > other_tanker.arrival_time if self.current_time == other_tanker.current_time \
            else self.current_time > other_tanker.current_time