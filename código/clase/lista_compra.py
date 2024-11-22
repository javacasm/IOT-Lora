'''
Programa para gestionar la lista de la compra
'''

lista_compra = ['cafe','patata','cerveza','papel higienico']

def mostrar_lista_compra(): #definición de la función
    for i in lista_compra:
        print(i) 
                                 
mostrar_lista_compra() # ejecuto la función

while True: # bucle  
    compra = input("¿Quieres comprar algo más? ('no' para terminar) ")
    if compra != 'no': # comparamos lo que hemos escrito 
        lista_compra.append(compra) # añadimos el elemento a la lista
    else:
        break  # salimos del bucle
mostrar_lista_compra() # ejecuto la función
