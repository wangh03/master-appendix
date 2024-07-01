#import matplotlib.pyplot as plt
# Create a porosity field
import numpy as np
from gstools import SRF,Gaussian

fmu = 0.20 # Field data mean value
fvariance = 1e-3 # variance value
# number of grid cells in x,y,z direction
x=range(10)
y=range(10)
z=range(15)

se = 1
sModel = Gaussian(dim = 3,var = fvariance, len_scale = 2)
sSrf = SRF(sModel,seed = se)
aafField = sSrf.structured([x,y,z])
aafField += fmu

# Save the reshaped array to a text file
np.savetxt('poro_array.txt',aafField.flatten(order='F'),fmt = '%f',delimiter = ' ')
aafkField = 10**(10*aafField)
# Save the reshaped array to a text file
np.savetxt('perm_array.txt', aafkField.flatten(order='F'), fmt='%f')





