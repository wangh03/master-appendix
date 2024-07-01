import sys

stdoutOrigin = sys.stdout
sys.stdout = open("ZCORNF.txt", "w")
print('ZCORN')

Dshallow = 1700  # shallowest point
dz = 50
dzdy = 25
NJ = 10  # number of cells in J direction
NI = 10  # number of cells in I direction
NK = 15 # number of cells in K direction
corI = 2 * NI
corII = 4 * NI

D = Dshallow
print(str(corI) + '*' + str(D))
D = D + dzdy
for i in range(NJ - 1):
    print(str(corII) + '*' + str(D))
    D = D + dzdy
print(str(corI) + '*' + str(D))

D = Dshallow + dz

for i in range(NK - 1):
    for k in range(2):
        ND = D
        print(str(corI) + '*' + str(ND))
        ND = ND + dzdy
        for K in range(9):
            print(str(corII) + '*' + str(ND))
            ND = ND + dzdy
        print(str(corI) + '*' + str(ND))
    D += dz

print(str(corI) + '*' + str(D))
D = D + dzdy

for i in range(NJ - 1):
    print(str(corII) + '*' + str(D))
    D = D + dzdy
print(str(corI) + '*' + str(D))
print('/')

sys.stdout.close()
sys.stdout = stdoutOrigin