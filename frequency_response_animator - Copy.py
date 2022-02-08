import numpy as np
import matplotlib.pyplot as plt

names = [
        "data_3dof_building_tmd5.txt.txt"
        ]

n = 5

amplitudes = np.zeros((2,n,3))

for i in range(0,len(names)):

    file = open(names[i],"r").readlines()

    for j in range(0,len(file)):

        line = file[j]

        line = np.array(line.strip("\n"))

        line = float(line)

        amplitudes[i,j,:] = line[0:3]

        
