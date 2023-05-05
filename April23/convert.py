# Read the second line of operations24.txt, operations30_0.txt, operations30_1.txt, operations30_2.txt, 
# Convert every tuple from i, j to n - i + 1, j + 1
# Write the converted tuples to converted24.txt, converted30_0.txt, converted30_1.txt, converted30_2.txt

import sys

def convert(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()
    f = open('converted' + filename[10:], 'w')
    s = lines[1][1:-2].split("),")
    for i in range(len(s)):
        if s[i][-1] != ')':
            s[i] += ')'
        if s[i][0] != '(':
            s[i] = s[i][1:]
    n = int(filename[10:12])
    print(n)
    f.write("[")
    for i in range(len(s)):
        print(s[i], end = ",")
        s[i] = s[i][1:-1].split(',')
        print(s[i], end = ",")
        s[i][0] = str(n - int(s[i][0]))
        s[i][1] = str(int(s[i][1]) + 1)
        s[i] = '(' + s[i][0] + ',' + s[i][1] + ')'
        print(s[i])
        f.write(s[i] + ',')
    f.write("]")
    f.close()

convert('operations24.txt')
convert('operations30_0.txt')
convert('operations30_1.txt')
convert('operations30_2.txt')