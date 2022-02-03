import numpy as np

def y_amplitudes(m_mat, k_mat, omega, f_vector):

    m_mat = np.array(m_mat)
    k_mat = np.array(k_mat)
    f_vector = np.array(f_vector)

    y_vector = np.zeros(len(f_vector))
    
    # y_vector = [k_mat - omega^2 * m_mat]^-1 * f_vector

    dyn_mat = k_mat - omega*omega*m_mat

    inv_dyn_mat = np.linalg.inv(dyn_mat)

    y_vector = inv_dyn_mat @ f_vector
    
    return y_vector

#y_amplitudes([[100, 0],[0, 1]],[[-1, 1],[1, -1]],1,[0,1])

