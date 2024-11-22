'''
Programa para gestionar la lista de la compra

Cargamos la lista de la compra del fichero "mi_lista_compra.py"
'''
lista_compra = []

FICHERO_LISTA_COMPRA = 'lista_compra.txt'

def cargar_lista_compra_v3():
    try:   
        f = open(FICHERO_LISTA_COMPRA, 'rt', encoding='utf8')
        while True:
            cosa = f.readline()
            if cosa and cosa != '':
                lista_compra.append(cosa.rstrip())
            else:
                break
        f.close()
    except Exception as e:
        print('No existe el fichero',e)
        
def mostrar_lista_compra(): #definición de la función
    print('Lista de compra actual\n'+'-'*30)
    for i in lista_compra:
        print(f'\t{i}') 

def guarda_lista_compra_v3():
    f = open(FICHERO_LISTA_COMPRA, 'wt', encoding='utf8') # abrimos el fichero para escritura
    for cosa in lista_compra:
        f.write(f'{cosa}\n')
    f.close() # cerramos el fichero

cargar_lista_compra_v3()
                          
mostrar_lista_compra() # ejecuto la función

while True: # bucle  
    compra = input("¿Quieres comprar algo más? ('no' para terminar) ").strip().lower()
    if compra not in  ('no','No','NO','') : # comparamos lo que hemos escrito
        if compra not in lista_compra:
            lista_compra.append(compra) # añadimos el elemento a la lista
        else:
            print(f'{compra} ya está en la lista')
    else:
        break  # salimos del bucle
mostrar_lista_compra() # ejecuto la función

guarda_lista_compra_v3()
