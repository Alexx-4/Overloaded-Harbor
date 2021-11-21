import matplotlib.pyplot as plt

'''
Grafica los datos que se le pasan como parametros, como 
tankers_list vs time_list y tankers_list vs mean_list
si estos son mayores de 10
'''
def plot(tankers_list, time_list, mean_list):
    if len(tankers_list) < 10: return
    
    _, ax = plt.subplots()

    ax.plot(tankers_list, time_list, marker = 'o')
    ax.set_title("Comportamiento del tiempo atendiendo a los tanqueros atendidos", color = 'tab:blue')
    ax.set_xlabel("Tanqueros atendidos")
    ax.set_ylabel("Tiempo de simulación")
    plt.show()

    _, ax = plt.subplots()
    ax.plot(tankers_list, mean_list, marker = 'o')
    ax.set_title("Comportamiento de la media de estancia atendiendo a los tanqueros atendidos", color = 'tab:blue')
    ax.set_xlabel("Tanqueros atendidos")
    ax.set_ylabel("Media de estancia")
    plt.show()




'''
Para graficar se ordena list1 (eje x) y se organizan las demas listas (eje y) de acuerdo al orden de esta
'''
def order_insert(item1, item2, item3, list1, list2, list3):
    list1.append(item1)
    list2.append(item2)
    list3.append(item3)

    i = len(list1) - 2

    while i >= 0:
        if list1[i] > item1:
            list1[i+1] = list1[i]
            list1[i] = item1

            list2[i+1] = list2[i]
            list2[i] = item2

            list3[i+1] = list3[i]
            list3[i] = item3

        i -= 1