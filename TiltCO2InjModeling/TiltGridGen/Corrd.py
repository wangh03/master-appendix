import sys

stdoutOrigin = sys.stdout
sys.stdout = open("COORDF.txt", "w")
print('COORD')

NJ = 10  # number of cells in J direction
NI = 10  # number of cell in I direction
X = 10*50  # cell size in X direction
Y = 10*50  # cell size in Y direction

Zmin = 0  # minimum depth
Zmax = 1000  # maximum depth

for j in range(NJ + 1):
    for i in range(NI + 1):
        print(str(i * X) + ' ' + str(j * Y) + ' ' + str(Zmin) + ' '\
              + str(i * X) + ' ' + str(j * Y) + ' ' + str(Zmax))
print('/')
sys.stdout.close()
sys.stdout = stdoutOrigin
