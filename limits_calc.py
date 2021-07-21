import cmath
from math import *
import numpy as np



def limits(Ybus, numbuses, Sbase, Vbase,V, d):
    V_complex=np.zeros((numbuses), dtype=complex)
    S=np.zeros((numbuses, numbuses), dtype=complex)
    Voltage_dev=np.zeros((numbuses))

    for i in range(numbuses):
        V_complex[i]=cmath.rect(V[i], d[i])
    print(V_complex)

    for i in range(numbuses):
        for j in range(numbuses):
            if not j==i:
                S[i][j]=V_complex[i]*(((V_complex[i]-V_complex[j]).conjugate())*(-Ybus[i][j].conjugate()))

    iv=np.genfromtxt("Initial_voltages.txt", dtype=float, filling_values=99.99)

                
    rem_capacity=np.zeros((numbuses, numbuses))


    tmp=np.genfromtxt("Grid_data.txt", dtype=float, filling_values=99.99)       
    Grid_data=np.delete(tmp, 0, 0)                                               
    length=Grid_data.shape                                                      

    for i in range(length[0]):
        left=int(Grid_data[i][1]-1)
        right=int(Grid_data[i][2]-1)
        rem_capacity[left][right]=Grid_data[i][5]/Sbase
        rem_capacity[right][left]=Grid_data[i][5]/Sbase




    transformers=np.genfromtxt("Transformers.txt", dtype=float, filling_values=99.99)   
    if not transformers.ndim==1:                                                        
        length2=transformers.shape                                                                                                   
    else:                                                                               
        length2=[0 ,0]                                                                  

    if not length2[0]==0:
        for i in range(length2[0]-1):
            left=int(transformers[i+1][1]-1)
            right=int(transformers[i+1][2]-1)
            rem_capacity[left][right]=transformers[i+1][6]/Sbase
            rem_capacity[right][left]=transformers[i+1][6]/Sbase
            a=transformers[i+1][3]
            y_mn=-Ybus[left][right]
            y_m=y_mn*(1-a)/a
            y_n=y_mn*(a-1)
            S[left][right]=V_complex[left]*(((V_complex[left]-V_complex[right]).conjugate())*(-Ybus[left][right].conjugate()))+y_m.conjugate()*(V[left])**2               
            S[right][left]=V_complex[right]*(((V_complex[right]-V_complex[left]).conjugate())*(-Ybus[left][right].conjugate()))+y_n.conjugate()*(V[right])**2  


    for i in range(numbuses):
        for j in range(numbuses):
            if not rem_capacity[i][j]==0:
                rem_capacity[i][j]=100*(rem_capacity[i][j]-abs(S[i][j]))/rem_capacity[i][j]

    for i in range(numbuses):
        Voltage_dev[i]=100*(V[i]-iv[i+1][3]/Vbase)/(iv[i+1][3]/Vbase)

    return S, rem_capacity, Voltage_dev

