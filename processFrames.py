# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 21:26:21 2019

@author: Juan Esteban Cepeda
"""

import csv
import pandas as pd

df = pd.read_csv("acc_data_walk2.csv", header = None)
series = df.iloc[1]
lista = series.tolist()

print(lista)


frames = 60
lista_de_listas = list()
lista_de_listas.append(list())


ejemplos = 0 # va hasta 20
contador = 0


for i in range(0, len(lista)):
    lista_de_listas[ejemplos].append(lista[i])
    contador += 1
    
    if(contador >= frames):
        lista_de_listas.append(list())
        contador = 0
        ejemplos += 1
    
print(lista_de_listas)

CATEGORY = 1

for i in lista_de_listas: 
    with open("./acc_data_walk_process.csv", "a") as writeFile:
         writer = csv.writer(writeFile)
         i.insert(0, CATEGORY)
         writer.writerow(i)
    writeFile.close()