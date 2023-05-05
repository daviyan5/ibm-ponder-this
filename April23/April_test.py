import numpy as np
import tkinter as tk

color0 = "white"
color1 = "black"
colorP = color0

def button_click(row, col):
    # if buttons[row][col]["bg"] == color1:
    #     return
    
    for i in range(len(buttons)):
        if buttons[i][col]["bg"] == color0:
            buttons[i][col]["bg"] = color1
        else:
            buttons[i][col]["bg"] = color0
    
    for j in range(len(buttons[0])):
        if buttons[row][j]["bg"] == color0:
            buttons[row][j]["bg"] = color1
        else:
            buttons[row][j]["bg"] = color0
    buttons[row][col]["bg"] = color1 if buttons[row][col]["bg"] == color0 else color0

def create_matrix(n, m, matrix=None):
    global buttons, initial_state
    buttons = [[None for j in range(m)] for i in range(n)]
    for i in range(n):
        for j in range(m):
            button = tk.Button(root, bg=colorP, command=lambda row=i, col=j: button_click(row, col))
            button.grid(row=i, column=j, sticky="nsew") # Use "sticky" to expand the buttons
            buttons[i][j] = button
    
    if matrix is not None:
        initial_state = matrix.copy()
        for i in range(n):
            for j in range(m):
                if matrix[i][j] == 1:
                    buttons[i][j]["bg"] = color1
                else:
                    buttons[i][j]["bg"] = color0
    else:
        initial_state = np.zeros((n, m))

    # Configure rows and columns to expand
    for i in range(n):
        root.grid_rowconfigure(i, weight=1)
    for j in range(m):
        root.grid_columnconfigure(j, weight=1)

def randomize_matrix():
    global initial_state
    new_matrix = np.random.randint(0, 2, size=initial_state.shape)
    initial_state = new_matrix.copy()
    for i in range(len(buttons)):
        for j in range(len(buttons[0])):
            if new_matrix[i][j] == 1:
                buttons[i][j]["bg"] = color1
            else:
                buttons[i][j]["bg"] = color0

def restart_matrix():
    for i in range(len(buttons)):
        for j in range(len(buttons[0])):
            if initial_state[i][j] == 1:
                buttons[i][j]["bg"] = color1
            else:
                buttons[i][j]["bg"] = color0

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
    return n, m, np.array(matrix)


root = tk.Tk()
root.title("Interactive Matrix")
n, m, M = read_input()
print(n, m, M)

create_matrix(n, m, M)

randomize_button = tk.Button(root, text="Randomize", command=randomize_matrix)
randomize_button.grid(row=len(buttons)+1, column=0, columnspan=len(buttons[0]))

restart_button = tk.Button(root, text="Restart", command=restart_matrix)
restart_button.grid(row=len(buttons)+2, column=0, columnspan=len(buttons[0]))

root.mainloop()
