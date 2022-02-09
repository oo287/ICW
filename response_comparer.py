import numpy as np
import matplotlib.pyplot as plt

names = [
        "data_exp2_3dof_0tmd.txt.txt",
        "data_exp2_3dof_ntmd.txt.txt",
        "data_exp2_3dof_3tmdd.txt.txt",
        "data_exp2_3dof_3tmds.txt.txt"
        ]

n = 100000

omegas = np.linspace(0.01,100,n)

dofs = 3

amplitudes = np.zeros((len(names),n,dofs))

for i in range(0,len(names)):

    file = open(names[i],"r").readlines()

    for j in range(0,n):

        line = file[j]

        line = line.split(",")[0:-1]

        #print(line)

        for k in range(0,len(line)):

            line[k] = float(line[k])
            
        amplitudes[i,j,:] = line[1:dofs+1]
        

    print("Done " + str(names[i]))

for j in range(0,len(names)):

    for i in range(0,dofs):
        
        plt.plot(omegas,amplitudes[j,:,i],label=str(names[j]))

plt.xlabel("Excitation Frequency / rad s-1")
plt.ylabel("Amplitude / m")
plt.legend()
plt.show()
