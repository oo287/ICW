import numpy as np

class node:

    def __init__(self, pk, m=1, k_list=[1], base_list=[-1]):
        self.pk = pk            # Primary key (unique identifier) of this node (also position in node matrices)
        self.m = m              # The mass of the node (kg)
        self.k_list = k_list         # List of pks of the nodes beneath this one (-1 by default is fixed ground)
        self.base_list = base_list   # List stiffnesses of the springs *beneath* the node, corresponding to nodes in bases list (N/m)


def generate_M_matrix(nodes):
    """ Function to create a diagonal nxn mass matrix using all node masses
    """
    M = np.zeros((len(nodes), len(nodes)))  # Create square nxn matrix
    for i, node in enumerate(nodes):
        M[i][i] = node.m
    return M

def get_k_list_above(nodes, focus):
    """ Generates list of length n containing stiffnesses of springs attached to focus from above. All other stiffnesses are 0.
    """
    k = np.zeros_like(nodes)
    for i, node in enumerate(nodes):
        if focus.pk in node.base_list:
            k[i] = node.k_list[node.base_list.index(focus.pk)]     # Get spring constant from above node that connects to focus
    return k

def generate_K_matrix(nodes):
    """ Function to create nxn stiffness matrix
    """
    K = np.zeros((len(nodes), len(nodes)))  # Create square nxn matrix
    for i, node in enumerate(nodes):
        k_list_above = get_k_list_above(nodes, node)    # Create n-length list of k values that relate to this node (all others are zero), in the same position as their nodes
        k_list_below = np.zeros(len(nodes))
        for j,k in zip(node.base_list, node.k_list):    # Create n-length list of k values that come from this node (all others are zero), in the same position as the node they attach to
            if j != -1:     # If this connection is not to ground
                k_list_below[j] = k
        print("Node:", node.pk)
        print("k_list_above:", k_list_above)
        print("k_list_below:", k_list_below)
        K[i] = - (k_list_above + k_list_below)   # Add (subtract) this node's contribution to other node positions (m+n)
        K[node.pk] += sum(k_list_above + k_list_below)   # Add summation of all ks as contribution of other nodes to this node's position
        print("final K", i,  K[i])

    return K

def run():

    # CANNOT IMPART AMPLITUDES ON THE GROUND!!!!!!! MAKE GROUND y0??
    # DOESNT CHECK FOR NONETYPE PKS!!!!!!!!!

    # Simple 2DOF system attached to ground as a test
    node0 = node(0, 1, [1], [-1])
    node1 = node(1, 2, [2], [0])
    nodes = np.array([node0, node1])
    print("Mass matrix:")
    print(generate_M_matrix(nodes))
    print()
    print("Stiffness matrix:")
    print(generate_K_matrix(nodes))
    print()


if __name__ == "__main__":
    run()
