# bucle personalizado entre 2 números dados

numero_inicial = input('Indica el número inicial: ')
numero_inicial_entero = int(numero_inicial)

numero_final = input('Indica el número final: ')
numero_final_entero = int(numero_final)

for i in range(numero_inicial_entero, numero_final_entero+1):
    print(i)