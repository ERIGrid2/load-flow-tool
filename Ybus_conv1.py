import cmath
from math import *
import numpy as np

#Calculation of admittances' angles and magnitudes

def Ybus_calc(Ybus):
    g=np.zeros((len(Ybus),len(Ybus)))
    Y=np.zeros((len(Ybus),len(Ybus)))
    for j in range(len(Ybus)):
        for i in range(len(Ybus)):
            g[i][j]=round(cmath.phase(Ybus[i][j]),5)
            Y[i][j]=round(abs(Ybus[i][j]),5)
    return Y, g;    


