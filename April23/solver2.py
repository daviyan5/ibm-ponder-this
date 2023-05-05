import numpy as np
import numba as nb
from memory_profiler import profile
dp = nb.typed.Dict.empty(key_type=nb.types.unicode_type, value_type=nb.types.ListType(nb.types.int64))
vis = nb.typed.Dict.empty(key_type=nb.types.unicode_type, value_type=nb.types.int64)
min_len_not_allowed = 430

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

@nb.njit(cache=True)
def create_A(operations, initial, reach):
    operations = np.concatenate((operations,  ((reach - initial) % 2).reshape(-1, 1)), axis=1)
    return operations

@nb.njit(cache=True)
def gauss_jordan_mod2(A):
    # Do Gauss-Jordan elimination on A
    # A is a (n * m) x (n * m) matrix
    
    n, m = A.shape

    # Forward elimination
    for i in range(n):
        # Find pivot row and swap
        max_row = np.argmax(A[i:, i]) + i
        temp_row = A[max_row].copy()
        A[max_row] = A[i]
        A[i] = temp_row
        
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

@nb.njit(cache=True)
def array2string(arr):
    ans = ""
    for i in range(arr.shape[0]):
        ans += str(arr[i])
    return ans
#@profile
@nb.njit(cache=True)
def solve(initial_state, reach_state, operations, n, m, skips = 0):
    # Solve the system of equations
    # A is a (n * m) x (n * m) matrix
    # b is a (n * m) x 1 matrix

    #mask = array2string(initial_state)
    #if mask in dp:
        #return dp[mask]
    #if mask in vis:
        #return None
    #vis[mask] = 1
    # Tries to solve it using general method
    A = create_A(operations, initial_state, reach_state)
    A, solvable = gauss_jordan_mod2(A)

    initial_aux = initial_state.copy()

    #adj = [mask]
    # If solvable by general method
    is_zero = np.where(initial_aux == 0)[0]

    if solvable:
        ops = []
        # Tries to solve it respecting the first condition
        found = True
        while is_zero.size != 0 and found:
            if not skips:
                np.random.shuffle(is_zero)
            # sort is_zero by the number of zeros affected by the operation


            found = False
            for i in is_zero:
                if A[i][-1] == 1:
                    initial_aux += operations[i]
                    initial_aux = initial_aux % 2
                    ops.append(i)
                    # adj.append(np.array2string(initial_aux))
                    # vis[np.array2string(initial_aux)] = 1
                    found = True
                    A[i][-1] = 0
                    break
            is_zero = np.where(initial_aux == 0)[0]

        # If it is solvable by the first condition
        if np.array_equal(initial_aux, reach_state) and len(ops) < min_len_not_allowed:
            #dp[mask] = ops
            # for i, mask2 in enumerate(adj):
            #     dp[mask2] = ops[i:]
            return ops
        else:
            if len(ops) >= min_len_not_allowed:
                #dp[mask] = None
                return None
            # We vary the matrix by every possible operation
            actual_ans = None
            actual_i = None
            counter = 0
            lim = skips + 1
            if not skips:
                per_op = np.sum((initial_aux + operations[is_zero]) % 2, axis=1)
                #print(per_op)
                is_zero = is_zero[np.argsort(per_op)]
            for i in is_zero:
                next_state = initial_aux.copy()
                next_state += operations[i]
                next_state = next_state % 2
                ans = solve(next_state, reach_state, operations, n, m, skips)
                if ans is not None and (actual_ans is None or len(ans) < len(actual_ans)):
                    actual_ans = ans
                    actual_i = i
                if ans is not None:
                    counter += 1
                if counter == lim:
                    break
            if actual_ans is not None and len(ops) + len(ans) < min_len_not_allowed:
                #adj.append(np.array2string(next_state))
                ops.append(actual_i)
                ops.extend(actual_ans)
                #dp[mask] = ops
                # for i, mask2 in enumerate(adj):
                #     dp[mask2] = ops[i:]
                return ops
            
            # If still not solvable
            #dp[mask] = None
            # for i, mask2 in enumerate(adj):
            #     dp[mask2] = None
            return None
    else:
        # If not solvable by general method, then won't be solvable by the first condition
        #dp[mask] = None
        return None


def read_input():
    f = open("initial_state.txt", "r")
    n = int(f.readline())
    m = int(f.readline())
    matrix = []
    for i in range(n):
        s = f.readline()
        if s[-1] == "\n":
            s = s[:-1]
        matrix.append([int(x) for x in s])
    f.close()
    return n, m, np.array(matrix).flatten()

def check(initial_state, ans, operations, n, m, verbose = False):
    # Check if the solution is correct
    out = open("output2.txt", "w")
    print("Number of operations: ", len(ans), file = out)
    atual_state = initial_state.copy() % 2
    states = []
    states.append(atual_state.copy())
    if verbose:
        print("Initial: \n", atual_state.reshape((n, m)), file = out)
    for i, j in ans:
        if atual_state[i*m + j] == 1:
            print("Failed at operation: ", i, j)
            return None
        else:
            if verbose:
                print("Operation: ", i, j, file = out)
            atual_state += operations[i * m + j]
            atual_state = atual_state % 2
            states.append(atual_state.copy())
            if verbose:
                print("After: \n", atual_state.reshape((n, m)), file = out)
    out.close() 

    return states

def apply_ops(initial_state, ops, operations, n, m):
    atual_state = initial_state.copy() % 2
    for i, j in ops:
        atual_state += operations[i * m + j]
        atual_state = atual_state % 2
    return atual_state

def reduce(initial_state, ans, operations, n, m):
    # Lets try to reduce the number of operations
    # For each operation, we try to jump it to every operation from the end backwards
    # If we can jump it, then we can remove it
    
    actual_state = initial_state.copy() % 2
    #dp.clear()
    #vis.clear()
    for i in range(len(ans)):
        dp.clear()
        vis.clear()
        for j in range(len(ans) - 1, i, -1):
            
            s = "Trying to reduce from " + str(i) +  " to " +  str(j) +  " with " +  str(len(ans)) +  " operations"
            print(s, end = "\r")
            reach_state = apply_ops(actual_state, ans[i:j + 1], operations, n, m)
            new_ans = solve(actual_state, reach_state, operations, n, m, 2)
            if new_ans is not None and len(new_ans) < j - i + 1:
                print(" " * (len(s) + 10), end = "\r")
                new_ans = [(int(i / m), i % m) for i in new_ans]
                print("Reduced from ", len(ans), " to ", len(ans) - j + i - 1 + len(new_ans))
                print("INDEXES: ", i, j)
                ans_j = ans[j + 1:]
                #ans = ans[:i + 1]
                ans = []
                ans.extend(new_ans)
                ans.extend(ans_j)

                
                break
            else:
                print(" " * (len(s) + 10), end = "\r")
        if i < len(ans):
            actual_state = apply_ops(actual_state, [ans[i]], operations, n, m)

    return ans

def main():
    try_reduce = False
    n, m, initial_state = read_input()
    #initial_state =  np.random.randint(0, 1, size=(n, m)).flatten()
    reach_state = np.ones(shape = (n, m)).flatten()
    operations = op(n, m)
    ans = None
    tries = 1000
    import time

    start = time.time()
    for i in range(tries):
        dp.clear()
        vis.clear()
        print("Solving trie {}...".format(i), end = "\r")
        cur_ans = solve(initial_state, reach_state, operations, n, m, 0)
        end = time.time()
        print("({:02d}h:{:02d}m:{:02d}s)".format(int((end - start) / 3600), int((end - start) / 60), int((end - start) % 60)), end = " ")
        if cur_ans is None:
            print("No solution found in trie {}".format(i))
        else:
            print("Solution found in trie {} with size {}".format(i, len(cur_ans)))
        if cur_ans is not None and (ans is None or len(cur_ans) < len(ans)):
            print("New best solution found in trie {} with size {}".format(i, len(cur_ans)))
            ans = cur_ans
            if m == n == 30:
                if len(ans) < 430:
                    break
        
            
    # convert ans indexes to tuple (i, j)
    if ans is not None:
        ans = [(int(i / m), i % m) for i in ans]
        print("Operations: {}\n".format(len(ans)), ans)
        states = check(initial_state, ans, operations, n, m, verbose = True)
        # add wrong state and ans in ans and states
        # idx = np.random.randint(0, len(ans))
        # ans.insert(idx, (0, 0))
        # idx = np.random.randint(0, len(ans))
        # ans.insert(idx, (0, 0))
       
        if states is not None:
            print("Solution is correct")
            if not try_reduce:
                return
            new_ans = reduce(initial_state, ans, operations, n, m)
            if new_ans is None:
                print("Error")
                return
            print("Reduced operations: {} from {}\n".format(len(new_ans), len(ans)))
            print("Operations : \n", new_ans)
            new_states = check(initial_state, new_ans, operations, n, m, verbose = False)
            if new_states is not None:
                print("Reduction is correct")
            else:
                print("Reduction is wrong")
    else:
        print("No solution")


def profile():
    import cProfile
    cProfile.run('main()', sort='cumtime')




if __name__ == "__main__":
    #profile()
    main()