import numpy as np
import matplotlib.pyplot as plt

names = [
        "data_exp1_2dof_0tmd.txt.txt",
        "data_exp1_2dof_ntmd.txt.txt"
        ]

n = 100000

omegas = np.linspace(0.01,100,n)

dofs = 2

amplitudes = np.zeros((2,n,dofs))

for i in range(0,len(names)):

    file = open(names[i],"r").readlines()

    for j in range(0,n):

        line = file[j]

        line = line.split(",")[0:-1]

        #print(line)

        for k in range(0,len(line)):

            line[k] = float(line[k])

        amplitudes[i,j,:] = line[1:dofs+1]

for j in range(0,len(names)):

    for i in range(0,dofs):
        
        plt.plot(omegas,amplitudes[j,:,i])

plt.xlabel("Excitation Frequency / rad s-1")
plt.ylabel("Amplitude / m")
plt.show()
