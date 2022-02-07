from random import randint
import numpy as np
from equation_solver import y_amplitudes
import matplotlib.pyplot as plt
from NDOF_solver import *
import argparse

ap = argparse.ArgumentParser('Plot response curves')
ap.add_argument('--f', type=str, default="mesh.csv", help='Filename of mesh to read, e.g. mesh.csv')
args = ap.parse_args()

# Generate node list from file
nodes = read_mesh_from_file(args.f)

# Validate nodelist and update 'node.i's
validate_system(nodes)
assign_matrix_order(nodes)

# Generate matrices
m_matrix = generate_M_matrix(nodes)
k_matrix = generate_K_matrix(nodes)
l_matrix = generate_L_matrix(nodes)

n = len(m_matrix)

f_vector = np.zeros(n)
omega = 0.0

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
        amplitudes[i] = np.array(y_amplitudes(m_matrix, k_matrix, l_matrix, omega, f_vector))
    except:
        amplitudes[i] = amplitudes[i-1]

    for j in range(0,n):

        amplitudes[i][j] = abs(amplitudes[i][j])
        

for i in range(1,n):

    plt.plot(omegas,amplitudes[:,i],label=str(i))

plt.legend()
plt.show()
