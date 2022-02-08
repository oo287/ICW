import numpy as np
import matplotlib.pyplot as plt

names = [
        "data_exp1_2dof_0tmd.txt.txt"
        ]

n = 100000

dofs = 2

amplitudes = np.zeros((2,n,dofs))

for i in range(0,len(names)):

    file = open(names[i],"r").readlines()

    for j in range(0,len(file)):

        line = file[j]

        line = np.array(line.strip("\n"))

        line = float(line)

        amplitudes[i,j,:] = line[0:dofs]

        
