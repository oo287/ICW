from random import randint
import numpy as np
from equation_solver import y_amplitudes
import matplotlib.pyplot as plt

print("\n\nPlease input the name of the txt file to read mass and stiffness matrices and force vector from.\n")

s = False

while not s:

    filename = input("File name: ")

    try:

        txt_file = open(filename,"r").readlines()

        s = True

    except:

        try:
            
            txt_file = open(str(filename) + ".txt","r").readlines()

            s = True

        except:

            print("Failed to open file.")

text = []

for line in txt_file:

    line = line.strip("\n")

    a = line.split(",")

    text.append(a)
    
    #text.append(a[0:-1]+[a[-1][0:-1]]) # Remove the \n s from the last items on each line

n = len(text[0])

for line in text[0:-1]:

    if len(line) != n:

        raise("Dimension Error- Matrices must be square")

if len(text) != 3*n+2:

    raise("Dimension Error- Matrices must be of the same size")

m_matrix = np.zeros((n,n))
k_matrix = np.zeros((n,n))
l_matrix = np.zeros((n,n))
f_vector = np.zeros(n)
omega = 0.0

try:

    for j in range(0,n):

        for i in range(0,n):

            m_matrix[j][i] = float(text[j][i])

    for j in range(n,2*n):

        for i in range(0,n):

            k_matrix[j-n][i] = float(text[j][i])

    for j in range(2*n,3*n):

        for i in range(0,n):

            l_matrix[j-2*n][i] = float(text[j][i])

    for i in range(0,n):

        f_vector[i] = float(text[3*n][i])

    #omega = float(text[2*n+1][0])

except:

    raise("All values must be floats/integers")


min_freq = float(input("Minimum frequency: "))
max_freq = float(input("Maximum frequency: "))
no_samples = int(input("Number of samples: "))

delta = 0.01

amplitudes = np.zeros((no_samples,n))
omegas = np.linspace(min_freq,max_freq,no_samples)

m_e = m_matrix[0][0]

for i in range(0,no_samples):

    omega = omegas[i]
    
    f_vector = np.zeros(n)
    f_vector[0] = m_e*omega*omega*1 # 1m amplitude oscillation of the Earth

    try:
        amplitudes[i] = np.array(y_amplitudes(m_matrix, k_matrix, l_matrix, omega, f_vector),dtype=np.csingle)
    except Exception as e:
        print(amplitudes[i])
        print(m_matrix)
        print(k_matrix)
        print(l_matrix)
        print(omega)
        print(f_vector)
        print(y_amplitudes(m_matrix, k_matrix, l_matrix, omega, f_vector))
        print(e)
        amplitudes[i] = amplitudes[i-1]

    for j in range(0,n):

        amplitudes[i][j] = abs(amplitudes[i][j])
        

for i in range(1,n):

    plt.plot(omegas,amplitudes[:,i],label=str(i))

plt.legend()
plt.show()
