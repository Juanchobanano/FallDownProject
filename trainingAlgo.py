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
import naive_bayes

UDP_IP = "192.168.0.11"
UDP_PORT = 5556
CATEGORY = 1
  #-1 => Testing, 0 => Still, 1 => Moving, 2 => Fall
MODE = "TESTING" #"TRAINING" # "TESTING"
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
    
    # Plot X, Y, Z
    x = list()
    for i in range(0, FRAMES):
        x.append(i+1)
          
    # Save in CSV.
    if(input("Include in DataSet? YES/NO") == "Y"):
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

# Plot results.
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

# Close socket
sock.close()



#category,Xmean,Xmax,Xmin,Xstd,Ymean,Ymax,Ymin,Ystd,Zmean,Zmax,Zmin,Zstd
#category,Xmax,Xstd,Ymax,Ystd,Zmax,Zstd