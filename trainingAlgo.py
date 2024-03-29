# -*- coding: utf-8 -*-
"""
Editor de Spyder
Este es un archivo temporal.
"""

import socket
import matplotlib.pyplot as plt
import time
import auxiliar as axfunc
import csv
import numpy as np
import naive_bayes

# Graphing helper function
def setup_graph(title='', x_label='', y_label='', fig_size=None):
    fig = plt.figure()
    if fig_size != None:
        fig.set_size_inches(fig_size[0], fig_size[1])
    ax = fig.add_subplot(111)
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

UDP_IP = "10.203.162.231" #"192.168.43.156" #0.14
UDP_PORT = 5555
CATEGORY = 1
  #-1 => Testing, 0 => Still, 1 => Moving, 2 => Fall
MODE = "TRAINING" #"TRAINING" # "TESTING"
DECIMALS = 3

if(MODE == "TESTING"):
    CATEGORY = -1

# Start socket server.
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
print("Host Listening...")

# Initialize Acelerometro
acelerometro = list()
for i in range(0, 4):
    acelerometro.append(list())
    
contador = 0    
FRAMES = 15

start_time = time.time()
    
while contador < FRAMES:
    
    # Get Data.
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes.
    info = str(data, 'utf-8')
    
    # Process Data.
    info = info.replace(" ", "")
    lista = info.split(",")    
    length = len(lista)
    for i in range(0, length):
        lista[i] = round(float(lista[i]), DECIMALS)        

    # Print values.
    print(lista)  
    
    # Add Values in list.
    acelerometro[0].append(lista[2])
    acelerometro[1].append(lista[3])
    acelerometro[2].append(lista[4])
    acelerometro[3].append(lista[2] + lista[3] + lista[4])
    
    contador += 1
    
# Get features from data.
categoria = CATEGORY
data = axfunc.getFeatures(categoria, acelerometro, decimals = DECIMALS)
print(data)

# Print elapsed time.
elapsed_time = time.time() - start_time
print("Elapsed Time: ", elapsed_time)

# Training Mode.
if MODE == "TRAINING":
          
    # Save in CSV.
    if(input("Include in DataSet? YES/NO: ") == "Y"):
        with open("./acc_data.csv", "a") as writeFile:
             writer = csv.writer(writeFile)
             writer.writerow(data)
        writeFile.close()
        print("Included!")
    else: 
        print("Not included")

# Testing Mode.
elif MODE == "TESTING":
    classifier = naive_bayes.NaiveBayesClassifier("acc_data.csv")
    print("Classification: ", classifier.classifyEntry(data))

    
# Plot X, Y, Z
x = list()
for i in range(0, FRAMES):
    x.append(i+1)
    
    
# 
time_to_plot = 2 # second
sample_rate = 100 # samples per second
num_samples = sample_rate * time_to_plot
    
fft_output = np.fft.rfft(acelerometro[3])
magnitude_only = [np.sqrt(i.real**2 + i.imag**2)/len(fft_output) for i in fft_output]
frequencies = [(i*1.0/num_samples)*sample_rate for i in range(num_samples//2+1)]

setup_graph(x_label='frequency (in Hz)', y_label='amplitude', title='frequency domain')
plt.plot(frequencies, magnitude_only, 'r')

# Plot results.

"""
plot1, = plt.plot(x, acelerometro[0])
plot2, = plt.plot(x, acelerometro[1])
plot3, = plt.plot(x, acelerometro[2])
plt.legend([plot1, plot2, plot3], ["X", "Y", "Z"])
plt.ylabel("Values")
plt.xlabel("Frames")
plt.title("Accelerometer Info")
plt.show()

# Plot total.
plot4, = plt.plot(x, acelerometro[3])
plt.title("Accelerometer Total")
plt.legend([plot4], "Total")
plt.ylabel("Values")
plt.xlabel("Frames")
plt.show()
"""

# Close socket
sock.close()



#category,Xmean,Xmax,Xmin,Xstd,Ymean,Ymax,Ymin,Ystd,Zmean,Zmax,Zmin,Zstd
#category,Xmax,Xstd,Ymax,Ystd,Zmax,Zstd