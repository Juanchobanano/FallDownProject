# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 11:52:12 2019

@author: Juan Esteban Cepeda
"""

import pandas as pd
import math
import warnings

warnings.filterwarnings("ignore")

"""
 0 => Still
 1 => Movement
 2 => Fall
"""

class NaiveBayesClassifier():
    
    def __init__(self, filePath):
        # Get Data from csv.
        global data
        global radius 
        
        data = pd.read_csv(filePath)
        data.columns = "category Xmax Xmin Xstd Ymax Ymin Ystd Zmax Zmin Zstd Tmax Tmin Tstd".split()
        radius = 100
                
    # Category Probability.
    def priorProbability(self, category):
        num_category = data[data.category == category]["category"].count()
        total = data["category"].count()
        return num_category / total
    
    # Probability of being 
    def marginalLikelihood(self, new_obs):
        contador = 0
        df_len = data["category"].count()
        for i in range(0, df_len):
            point_features = data.iloc[i].values
            distance = self.distancePoints(new_obs, point_features)
            #print("distance: ", distance)
            if distance < radius:
                contador += 1
        return contador / df_len
    
    # Likelihood.
    def likeliHood(self, category, new_obs):
        contador = 0
        df_len = data["category"].count()
        for i in range(0, df_len):
            point_features = data.iloc[i].values
            distance = self.distancePoints(new_obs, point_features)
            if distance < radius and data.iloc[0].category == category:
                contador += 1
        num_category = data[data.category == category]["category"].count()
        return (contador / num_category)
    
    # Posterior Probability
    def posteriorProbability(self, category, new_obs):
        priorProb = self.priorProbability(category)
        marginalLike = self.marginalLikelihood(new_obs)
        likelihood = self.likeliHood(category, new_obs)
        res = (likelihood * priorProb) / marginalLike
        
        print(category, priorProb, marginalLike, likelihood, res)
        
        return res
    
    def classifyEntry(self, new_obs):
        categories = list()
        for i in [0, 1, 2]:
            categories.append(self.posteriorProbability(i, new_obs))
        return categories.index(max(categories))
    
    # Auxiliar functions.
    def distancePoints(self, p1, p2):
        distance = 0
        for i in range(1, len(p1)):
            distance += (p1[i] - p2[i]) ** 2
        return math.sqrt(distance)
    
    def getData(self):
        return data
        
        
    
#obj = NaiveBayesClassifier("acc_data.csv")

#print(obj.priorProbability(0))

#x = [-1, -6.04326, -5.558, -6.895, 0.029854792400000007, -0.47850000000000015, -0.248, -0.694, 0.0027383900000000007, 7.5284799999999965, 8.765, 6.226, 0.15353362960000003]
#print(obj.marginalLikelihood(x))
#x = [1, 0.638, 3.524, -2.386, 1.605, 9.519, 11.147, 7.816, 0.341, 1.459, 5.363, -1.012, 1.796] 
#print("Classification: ", obj.classifyEntry(x))

#print(obj.likeliHood(0, x))


