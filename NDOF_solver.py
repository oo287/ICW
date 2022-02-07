import numpy as np
import argparse

class node:

    def __init__(self, pk, m=1, base_list=[], k_list=[], l_list=[]):
        self.pk = pk                    # Primary key (unique identifier) of this node
        self.i = None                   # Position of node in matrix (set by program)
        self.m = m                      # The mass of the node (kg)
        self.base_list = base_list      # List of pks of the nodes beneath this one
        self.k_list = k_list            # List stiffnesses of the springs *beneath* the node, corresponding to nodes in bases list (N/m)
        self.l_list = l_list            # List of damping factors of the dashpots *beneath* the node, corresponding to nodes in bases list (N/ms-1)



def validate_system(nodes):
    present_pks = [0]
    for node in nodes[1:]:
        if node.pk in present_pks:
            error_str = "More than one node with pk = " + str(node.pk) + ". Primary keys must be unique."
            if node.pk == 0:
                error_str = "Node pk = 0 is reserved, and cannot be used for inputted nodes."
            raise ValueError(error_str)
        else:
            present_pks.append(node.pk)

def assign_matrix_order(nodes):
    for i, node in enumerate(nodes):
        node.i = i

def generate_M_matrix(nodes):
    """ Function to create a diagonal nxn mass matrix using all node masses
    """
    M = np.zeros((len(nodes), len(nodes)))  # Create square nxn matrix
    for node in (nodes):
        M[node.i][node.i] = node.m
    return M

def get_k_list_above(nodes, focus):
    """ Generates list of length n containing stiffnesses of springs attached to focus from above. All other stiffnesses are 0.
        STIFFNESSES ARE IN POSITION CORRESPONDING TO I OF RELEVENT MASS
    """
    k = np.zeros_like(nodes)
    for node in nodes:
        if focus.pk in node.base_list:
            k[node.i] = node.k_list[node.base_list.index(focus.pk)]     # Get spring constant from above node that connects to focus
    return k

def get_k_list_below(nodes, focus):
    """ Generates list of length n containing stiffnesses of springs attached to focus from above. All other stiffnesses are 0.
        STIFFNESSES ARE IN POSITION CORRESPONDING TO I OF RELEVENT MASS
    """
    k = np.zeros_like(nodes)
    for node in nodes:
        if node.pk in focus.base_list:
            k[node.i] = focus.k_list[focus.base_list.index(node.pk)]    # Get spring constant from k_list corresponding to "below-mass" pk
    return k

def generate_K_matrix(nodes):
    """ Function to create nxn stiffness matrix
    """
    K = np.zeros((len(nodes), len(nodes)))  # Create square nxn matrix
    for node in nodes:
        k_list_above = get_k_list_above(nodes, node)    # Create n-length list of k values that relate to this node (all others are zero), in the same position as their nodes
        k_list_below = get_k_list_below(nodes, node)
        K[node.i] = - (k_list_above + k_list_below)   # Add (subtract) this node's contribution to other node positions (m+n)
        K[node.i][node.i] += sum(k_list_above + k_list_below)   # Add summation of all ks as contribution of other nodes to this node's position
    return K

def get_l_list_above(nodes, focus):
    """ Generates list of length n containing damping factors of dashpots attached to focus from above. All other damping factors are 0.
        DAMPING FACTORS ARE IN POSITION CORRESPONDING TO I OF RELEVENT MASS
    """
    l = np.zeros_like(nodes)
    for node in nodes:
        if focus.pk in node.base_list:
            l[node.i] = node.l_list[node.base_list.index(focus.pk)]     # Get spring constant from above node that connects to focus
    return l

def get_l_list_below(nodes, focus):
    """ Generates list of length n containing damping factors of dashpots attached to focus from from below. All other damping factors are 0.
        DAMPING FACTORS ARE IN POSITION CORRESPONDING TO I OF RELEVENT MASS
    """
    l = np.zeros_like(nodes)
    for node in nodes:
        if node.pk in focus.base_list:
            l[node.i] = focus.l_list[focus.base_list.index(node.pk)]    # Get spring constant from k_list corresponding to "below-mass" pk
    return l

def generate_L_matrix(nodes):
    """ Function to create nxn stiffness matrix
    """
    L = np.zeros((len(nodes), len(nodes)))  # Create square nxn matrix
    for node in nodes:
        l_list_above = get_l_list_above(nodes, node)    # Create n-length list of l values that relate to this node (all others are zero), in the same position as their nodes
        l_list_below = get_l_list_below(nodes, node)
        L[node.i] = - (l_list_above + l_list_below)   # Add (subtract) this node's contribution to other node positions (m+n)
        L[node.i][node.i] += sum(l_list_above + l_list_below)   # Add summation of all ks as contribution of other nodes to this node's position
    return L

def remove_ith_elements(A, i):
    """Removes ith row and ith column of matrix A."""
    A = np.delete(A, i, 0)
    A = np.delete(A, i, 1)
    return A

def read_mesh_from_file(filename):
    nodes = [node(0,6e24)]
    with open(filename) as file:
        file.readline()
        for line in file:
            if line.strip("\n") == "":
                break
            data = line.split(",")
            for i in range(len(data)):
                data[i] = data[i].strip(" []\n")
            try:
                list_length = int((len(data) - 2)/3)            # Length of base_list, k_list, l_list
                nodes.append(node(float(data[0]),                                     # Create node with specified pk
                                    float(data[1]),                                   # specified mass
                                    list([float(x) for x in data[2:2+list_length]]),                    # specified base_list
                                    list([float(x) for x in data[2+list_length:2+2*list_length]]),      # specified k_list
                                    list([float(x) for x in data[2+2*list_length:2+3*list_length]])     # specified l_list
                                )
                            )
            except ValueError as e:
                print("Invalid (non-numeric) input detected in file", filename)
                raise e
        f_line = file.readline().strip("\n")
        F = np.array(np.array(f_line.split(",")).astype(float))
        o_line = file.readline().strip("\n")
        omega = np.array(float(o_line))

    return np.array(nodes), F, omega

def run():

    # Read filename argument
    ap = argparse.ArgumentParser('Plot response curves')
    ap.add_argument('--f', type=str, default="mesh.txt", help='Filename of mesh to read, e.g. mesh.csv')
    args = ap.parse_args()

    # Generate node list from file
    nodes, F, omega = read_mesh_from_file(args.f)
    
    # Validate nodelist and update 'node.i's
    validate_system(nodes)
    assign_matrix_order(nodes)

    # Generate matrices
    M = generate_M_matrix(nodes)
    K = generate_K_matrix(nodes)
    L = generate_L_matrix(nodes)

    print("Mass matrix:")
    print(M)
    print()
    print("Stiffness matrix:")
    print(K)
    print()
    print("Damping matrix:")
    print(L)
    print()
    print("Modified Mass matrix:")
    ground_i = nodes[[node.pk for node in nodes].index(0)].i   # i of the node with pk=0
    M = remove_ith_elements(M, ground_i)
    print(M)
    print()
    print("Modified Stiffness matrix:")
    K = remove_ith_elements(K, ground_i)
    print(K)
    print()
    print("Modified Damping matrix:")
    L = remove_ith_elements(L, ground_i)
    print(L)
    print()
    




if __name__ == "__main__":
    run()
