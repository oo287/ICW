import numpy as np

class node:

    def __init__(self, pk, m=1, base_list=[], k_list=[]):
        self.pk = pk                    # Primary key (unique identifier) of this node
        self.i = None                   # Position of node in matrix (set by program)
        self.m = m                      # The mass of the node (kg)
        self.base_list = base_list      # List of pks of the nodes beneath this one
        self.k_list = k_list            # List stiffnesses of the springs *beneath* the node, corresponding to nodes in bases list (N/m)




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
        print("Node:", node.pk)
        print("k_list_above:", k_list_above)
        print("k_list_below:", k_list_below)
        K[node.i] = - (k_list_above + k_list_below)   # Add (subtract) this node's contribution to other node positions (m+n)
        K[node.i][node.i] += sum(k_list_above + k_list_below)   # Add summation of all ks as contribution of other nodes to this node's position
        print("final K", node.i,  K[node.i])
    return K


def run():

    # CANNOT IMPART AMPLITUDES ON THE GROUND!!!!!!! MAKE GROUND y0??
    # DOESNT CHECK FOR NONETYPE PKS!!!!!!!!!

    # Simple 2DOF system attached to ground as a test
    node0 = node(0, 0)
    node1 = node(0, 1, [1], [1])
    node2 = node(1, 2, [2], [1])
    nodes = np.array([node0, node1, node2])
    assign_matrix_order(nodes)
    M = generate_M_matrix(nodes)
    K = generate_K_matrix(nodes)
    print("\n")
    print("Mass matrix:")
    print(M)
    print()
    print("Stiffness matrix:")
    print(K)
    print()
    print("Modified Mass matrix:")
    #ground_i = nodes[[node.pk for node in nodes].index(0)]   # i of the node with pk=0
    print(M)
    print()
    print("Modified Stiffness matrix:")
    print(K)
    print()



if __name__ == "__main__":
    run()
