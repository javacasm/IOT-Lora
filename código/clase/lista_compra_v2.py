'''
Programa para gestionar la lista de la compra

Cargamos la lista de la compra del fichero "mi_lista_compra.py"
'''
from mi_lista_compra import lista_compra

def mostrar_lista_compra(): #definición de la función
    for i in lista_compra:
        print(i) 

def guarda_lista_compra():
    f = open('mi_lista_compra.py', 'wt', encoding='utf8') # abrimos el fichero para escritura
    f.write('# programa de lista de la compra v2\n') # escribimos el comentario
    f.write('lista_compra = ') # declaramos la variable
    f.write(str(lista_compra)) # guardamos los valores de la lista
    f.write('\n') # añadimos un final de línea
    f.close() # cerramos el fichero
    
def guarda_lista_compra_v2():
    f = open('mi_lista_compra.py', 'wt', encoding='utf8') # abrimos el fichero para escritura
    f.write('# programa de lista de la compra v2\n') # escribimos el comentario
    f.write(f'lista_compra = {lista_compra}\n') # añadimos un final de línea
    f.close() # cerramos el fichero 

                          
mostrar_lista_compra() # ejecuto la función

while True: # bucle  
    compra = input("¿Quieres comprar algo más? ('no' para terminar) ")
    if compra != 'no': # comparamos lo que hemos escrito 
        lista_compra.append(compra) # añadimos el elemento a la lista
    else:
        break  # salimos del bucle
mostrar_lista_compra() # ejecuto la función

guarda_lista_compra_v2()
