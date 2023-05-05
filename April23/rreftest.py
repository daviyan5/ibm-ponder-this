import numpy as np
import sympy as sp

def op(n, m):
    # Create a (n * m) x (n * m) matrix of zeros
    operations = np.zeros(shape=(n * m, n * m))
    
    # Create arrays of row and column indices
    rows, cols = np.indices((n, m))
    
    # Create (n * m) x (n * m) matrix of rows
    rows_matrix = np.tile(rows.flatten(), (n * m, 1))
    
    # Create (n * m) x (n * m) matrix of cols
    cols_matrix = np.tile(cols.flatten(), (n * m, 1))
    
    # Set the values of operations using the row and column indices
    operations = np.logical_or(rows_matrix == rows_matrix.T, cols_matrix == cols_matrix.T).astype(int)
   
    return operations

def create_A(operations, initial, reach):
    operations = np.concatenate((operations,  ((reach_state.flatten() - initial_state.flatten()) % 2).reshape(-1, 1)), axis=1)
    return operations

n, m = 3, 3
initial_state =  np.random.randint(0, 1, size=(n, m))
reach_state = np.ones(shape = (n, m))
#reach_state = np.array([[1, 0], [0, 0]])
initial_state = np.array([[1, 1, 1], [1, 1, 0], [0, 1, 1]])
print(initial_state)

operations = op(n, m)
operations = create_A(operations, initial_state, reach_state)

print(operations)
print("\n")
def gauss_jordan_mod2(A):
    # Do Gauss-Jordan elimination on A
    # A is a (n * m) x (n * m) matrix
    
    n, m = A.shape

    # Forward elimination
    for i in range(n):
        # Find pivot row and swap
        max_row = i
        for j in range(i+1, n):
            if abs(A[j,i]) > abs(A[max_row,i]):
                max_row = j
        A[[i,max_row]] = A[[max_row,i]]

        # Eliminate rows below
        for j in range(i+1, n):
            factor = A[j,i] % 2
            A[j] = (A[j] + factor*A[i]) % 2

    # Backward substitution
    for i in range(n-1, -1, -1):
        # Normalize pivot row
        pivot = A[i,i]
        if pivot == 0:
            continue
        A[i] = A[i] / pivot
        # Eliminate rows above
        for j in range(i):
            factor = A[j,i] % 2
            A[j] = (A[j] + factor*A[i]) % 2

    solvable = True
    for i in range(n):
        if np.array_equal(A[i][:-1], np.zeros(m - 1)) and A[i][-1] != 0:
            solvable = False
            break
    return A, solvable

operations_solved, solvable = gauss_jordan_mod2(operations)
alternative_operations = sp.Matrix(operations).rref()
print(operations_solved)
print("Not solvable" if not solvable else "Solvable")
print(alternative_operations)


