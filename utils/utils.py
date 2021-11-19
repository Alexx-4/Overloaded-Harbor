import random as r
import math

'''
 Generacion de variables aleatorias 
'''


'''
Recibe el parametro _lambda de la distribucion exponencial
'''
def exponential(_lambda):
    U = r.random()
    return - ( 1/_lambda ) * math.log(U)



'''
Recibe los parametros miu y sigma cuadrado de la distribucion normal
'''
def normal(miu, o_2):
    while True:
        Y = exponential(1)
        U = r.random()
        if U <= math.exp((-1/2) * (Y - 1)**2): break
    
    U = r.random()
    Z = Y if U < 0.5 else -Y

    # Z = (X - miu)/o ~ N(0,1) => X = Zo + miu ~ N(miu,o^2)
    return Z * math.sqrt(o_2) + miu