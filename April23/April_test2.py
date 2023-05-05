import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import sys
import sympy

sys.setrecursionlimit(100000)

n, m = 3, 3
operations = np.zeros(shape=(n * m, n, m))
for i in range(n):
    for j in range(m):
        operations[i * m + j][i, :] = 1
        operations[i * m + j][:, j] = 1


final = np.ones((n, m))
visited = {}
dp = {}
adj = {}

def mask_to_idx(mask):
    # Convert a mask (string of 1 and 0) to it's corresponding index
    idx = 0
    for i in range(len(mask)):
        if mask[i] == "1":
            idx += 2 ** (len(mask) - i - 1)
    return idx


def solve(matrix):
    if np.array_equal(matrix, final):
        return True

    mask = np.array2string(matrix.flatten())
    if mask in dp:
        return dp[mask]
    if mask in visited:
        return False

    visited[mask] = True
    for i in range(n):
        for j in range(m):
            if matrix[i][j] == 0:
                
                next_matrix = (matrix + operations[i * m + j]) % 2
                a = solve(next_matrix)
                
                if a:
                    # idx = str(matrix)
                    # if idx not in adj:
                    #     adj[idx] = []
                    # if str(next_matrix) not in adj[idx]:
                    #     adj[idx].append(str(next_matrix))
                    dp[mask] = True
                    return True
    dp[mask] = False
    return False


# Test, for every possible initial configuration, if it is possible to reach the final configuration
# and save it in a file
file = open("solutions.txt", "w")
for i in range(2 ** (n * m)):
    matrix = np.array(list(np.binary_repr(i, width=n * m)), dtype=int).reshape((n, m))
    file.write(str(matrix) + "\n")
    if solve(matrix):
        file.write("True\n\n")
    else:
        file.write("False\n\n")

exit()
# create a directed graph from the adjacency list
G = nx.DiGraph(adj)
for key in adj:
    print("Key: \n", key)
    for value in adj[key]:
        print("Value: \n", value)

# generate a layout for the nodes and edges of the graph
pos = nx.spring_layout(G, seed=42)

# draw the graph
nx.draw_networkx(G, pos, node_color="lightblue", edge_color="gray")

# save the graph as an image file
plt.show() 