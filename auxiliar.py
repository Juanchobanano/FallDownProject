# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 11:30:33 2019

@author: Juan Esteban Cepeda
"""

def mean(lista):
    suma = 0
    for value in lista:
        suma += value
    return suma / len(lista)

def std(lista):
    mean_val = mean(lista)
    suma = 0
    
    for value in lista:
        suma += (value - mean_val) ** 2
    return suma / len(lista)
    
# Get Features function.
def getFeatures(categoria, acelerometro, decimals):
    
    # Ini features.
    features = list()

    # Set category.
    features.append(categoria)
    
    # Get mean, max, min, std of values.
    for i in range(0, len(acelerometro)):
        #features.append(round(mean(acelerometro[i]), decimals))
        features.append(round(max(acelerometro[i]), decimals))
        features.append(round(min(acelerometro[i]), decimals))
        features.append(round(std(acelerometro[i]), decimals))    

    # Return
    return features