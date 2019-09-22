# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 14:05:55 2019

@author: Juan Esteban Cepeda
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("acc_data.csv", delimiter = ",")
df.columns = "category Xmax Xmin Xstd Ymax Ymin Ystd Zmax Zmin Zstd Tmax Tmin Tstd".split()

sns.set(rc={'figure.figsize':(8,4)})
ax2 = sns.scatterplot(x="Xmax", y="Tmax",  hue="category", style="category", s=100, data=df)
ax = plt.gca()
ax.set_title("Compare Measures")
ax.plot()
