import cmath
import numpy as np


def Ybus_calculation(Grid_data, Zbase, numbuses, length, transformers, length2):
    Y1=np.zeros((length[0]), dtype=complex)
    Ybus=np.zeros((numbuses, numbuses),dtype=complex)
    for i in range(length[0]):
        Grid_data[i][3]=Grid_data[i][3]/Zbase
        Grid_data[i][4]=Grid_data[i][4]/Zbase
        Y1[i]=1/complex(Grid_data[i][3], Grid_data[i][4])

  
    for k in range(numbuses):
        for l in range(numbuses):
            if k==l:
                for m in range(length[0]):
                    if Grid_data[m][1]==k+1 or Grid_data[m][2]==k+1:
                        Ybus[k][l]=Ybus[k][l]+Y1[m]
            else:
                for m in range(length[0]):
                    if (Grid_data[m][1]==(k+1) or Grid_data[m][1]==(l+1))and(Grid_data[m][2]==(k+1) or Grid_data[m][2]==(l+1)):
                        Ybus[k][l]=-Y1[m]
    

    if not length2[0]==0:
        TR1=np.zeros((length2[0]-1),dtype=complex)
        
        for i in range(length2[0]-1):
            transformers[i+1][4]=transformers[i+1][4]/Zbase
            transformers[i+1][5]=transformers[i+1][5]/Zbase
            TR1[i]=1/complex(transformers[i+1][4], transformers[i+1][5])
            left=int(transformers[i+1][1])-1
            right=int(transformers[i+1][2])-1
            Ybus[left][left]=Ybus[left][left]+TR1[i]/(transformers[i+1][3])**2
            Ybus[right][right]=Ybus[right][right]+TR1[i]
            Ybus[left][right]=Ybus[left][right]-TR1[i]/transformers[i+1][3]
            Ybus[right][left]=Ybus[right][left]-TR1[i]/transformers[i+1][3]
            
            
    return Ybus


            
                    
            
