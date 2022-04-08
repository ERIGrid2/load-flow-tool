import cmath
from math import *
import numpy as np
import Ybus_constr
import Ybus_conv1
import limits_calc

#---------------------------------------------------------------------------------
# Initialization
numbuses=6
bl=np.genfromtxt("Bus_locations.txt", dtype=float, filling_values=99.99)
bus_type=np.zeros((numbuses))
Q_lim=np.zeros((numbuses, 2))
for i in range(numbuses):
    bus_type[i]=bl[i+1][3]
    Q_lim[i][0]=bl[i+1][4]
    Q_lim[i][1]=bl[i+1][5]

iv=np.genfromtxt("Initial_voltages.txt", dtype=float, filling_values=99.99)
V=np.zeros((numbuses))
d=np.zeros((numbuses))
for i in range(numbuses):
    V[i]=iv[i+1][1]
    d[i]=iv[i+1][2]

Delta_P=np.zeros((numbuses))
Delta_Q=np.zeros((numbuses))

P_spec=np.zeros((numbuses))
Q_spec=np.zeros((numbuses))



Q_gen=np.zeros((numbuses))

H=np.zeros((numbuses,numbuses))
N=np.zeros((numbuses,numbuses))
M=np.zeros((numbuses,numbuses))
L=np.zeros((numbuses,numbuses))


Zbase=225
Sbase=100000000
Vbase=150

#---------------------------------------------------------------------------------
# Calculation of aggregated power per bus
timeframe=2
ps=np.genfromtxt("Power_schedule2.txt", dtype=float, filling_values=99.99)
rc=np.genfromtxt("Resources_connectivity.txt", dtype=float, filling_values=99.99)
size=ps.shape

k=0
for i in range(size[0]-1):
    if not ps[i+1-k][0]==timeframe:
        ps=np.delete(ps, i+1-k, 0)
        k=k+1

size=ps.shape
for i in range(size[0]-1):
    index1=int(rc[i+1][1]-1)
    P_spec[index1]=P_spec[index1]+ps[i+1][1]/Sbase
    Q_spec[index1]=Q_spec[index1]+ps[i+1][2]/Sbase



#---------------------------------------------------------------------------------
# Calculation of admittances' angles and magnitudes

Ybus=np.zeros((numbuses, numbuses),dtype=complex)
tmp=np.genfromtxt("Grid_data.txt", dtype=float, filling_values=99.99)
Grid_data=np.delete(tmp, 0, 0)
length=Grid_data.shape

transformers=np.genfromtxt("Transformers.txt", dtype=float, filling_values=99.99)
if not transformers.ndim==1:
    length2=transformers.shape
else:
    length2=[0 ,0]


Ybus=Ybus_constr.Ybus_calculation(Grid_data, Zbase, numbuses, length,transformers, length2)
Y, g=Ybus_conv1.Ybus_calc(Ybus)



for counter in range(5):
#---------------------------------------------------------------------------------
# Check the BusType2 reactive power requirement and change the type of bus from 2
# to 1

    for i in range(numbuses):
        if bus_type[i]==2:
            B=0
            for j in range(numbuses):
                B=B+V[j]*Y[i][j]*sin(d[j]-d[i]+g[i][j])
            Q_gen[i]=-V[i]*B-Q_spec[i]
            
            if Q_gen[i]>=Q_lim[i][0]/Sbase:
                Q_spec[i]=Q_spec[i]+Q_lim[i][0]/Sbase
                bus_type[i]=12
            elif Q_gen[i]<=Q_lim[i][1]/Sbase:
                Q_spec[i]=Q_spec[i]+Q_lim[i][1]/Sbase
                bus_type[i]=12
                
#---------------------------------------------------------------------------------
# Calculation of DP(n) and DQ(n)


    for i in range(numbuses):
        if bus_type[i]==1 or bus_type[i]==12:
            A,B=0,0
            for j in range(numbuses):
                A=A+V[j]*Y[i][j]*cos(d[j]-d[i]+g[i][j])
                B=B+V[j]*Y[i][j]*sin(d[j]-d[i]+g[i][j])
            Delta_P[i]=P_spec[i]-V[i]*A
            Delta_Q[i]=Q_spec[i]+V[i]*B
        elif bus_type[i]==2:
            A=0
            for j in range(numbuses):
                A=A+V[j]*Y[i][j]*cos(d[j]-d[i]+g[i][j])
            Delta_P[i]=P_spec[i]-V[i]*A
            
    
#---------------------------------------------------------------------------------
# Calculation of matrices H, M, N and L for all buses

    for i in range(numbuses):
        for j in range(numbuses):
            if i!=j:
                H[i][j]=-V[i]*V[j]*Y[i][j]*sin(d[j]-d[i]+g[i][j])
                N[i][j]=V[i]*Y[i][j]*cos(d[j]-d[i]+g[i][j])
                M[i][j]=-V[i]*V[j]*Y[i][j]*cos(d[j]-d[i]+g[i][j])
                L[i][j]=-V[i]*Y[i][j]*sin(d[j]-d[i]+g[i][j])
            else:
                H[i][i]=0
                N[i][i]=2*V[i]*Y[i][i]*cos(g[i][i])
                M[i][i]=0
                L[i][i]=-2*V[i]*Y[i][i]*sin(g[i][i])
                for k in range(numbuses):
                    if i!=k:
                        H[i][i]=H[i][i]+V[i]*V[k]*Y[i][k]*sin(d[k]-d[i]+g[i][k])
                        N[i][i]=N[i][i]+V[k]*Y[i][k]*cos(d[k]-d[i]+g[i][k])
                        M[i][i]=M[i][i]+V[i]*V[k]*Y[i][k]*cos(d[k]-d[i]+g[i][k])
                        L[i][i]=L[i][i]-V[k]*Y[i][k]*sin(d[k]-d[i]+g[i][k])


#---------------------------------------------------------------------------------
# Calculation of final H, M, N and L matrices taking out slack and generation buses

    k=0
    Hn, Nn, Mn, Ln=H, N, M, L
    for i in range(numbuses):
       
        if bus_type[i]==0:
            Hn=np.delete(Hn,i,0)
            Hn=np.delete(Hn,i,1)
            Nn=np.delete(Nn,i,0)
            Nn=np.delete(Nn,i,1)
            Mn=np.delete(Mn,i,0)
            Mn=np.delete(Mn,i,1)
            Ln=np.delete(Ln,i,0)
            Ln=np.delete(Ln,i,1)
            k=k+1
        elif bus_type[i]==2:
            Nn=np.delete(Nn,i-k,1)
            Mn=np.delete(Mn,i-k,0)
            Ln=np.delete(Ln,i-k,0)
            Ln=np.delete(Ln,i-k,1)
            k=k+1
             
   
    JacobianUP=np.concatenate((Hn,Nn),axis=1)
    JacobianDOWN=np.concatenate((Mn,Ln),axis=1)
    Jacobian=np.concatenate((JacobianUP, JacobianDOWN),axis=0)

    invJac=np.linalg.inv(Jacobian)


#---------------------------------------------------------------------------------
# Calculation only of the necessary Delta P and Delta Q taking out
# slack bus and generation buses
    
    Delta_Pn, Delta_Qn=Delta_P, Delta_Q
    for i in range(numbuses):
        if bus_type[i]==0:
            Delta_Pn=np.delete(Delta_Pn,i)
            
    k=0
    for i in range(numbuses):
        if bus_type[i]==0 or bus_type[i]==2:
            Delta_Qn=np.delete(Delta_Qn,i-k)
            k=k+1

    DPQ=np.concatenate((Delta_Pn, Delta_Qn), axis=0)



    ddV=np.dot(invJac, DPQ) 
    
    
#---------------------------------------------------------------------------------
# Updating the angle/Voltage vectors

    k=0
    for i in range(numbuses):
        if not bus_type[i]==0:
            d[i]=d[i]+ddV[k]
            k=k+1
    for i in range(numbuses):
        if bus_type[i]==1 or bus_type[i]==12:
            V[i]=V[i]+ddV[k]
            k=k+1

k=0

print(V)
print(d)

#---------------------------------------------------------------------------------
# Calculation of P,Q of generators
for i in range(numbuses):
    if bus_type[i]==0:
        A, B=0, 0
        for j in range(numbuses):
            A=A+V[j]*Y[i][j]*cos(d[j]-d[i]+g[i][j])
            B=B+V[j]*Y[i][j]*sin(d[j]-d[i]+g[i][j])
        P_spec[i]=V[i]*A
        Q_spec[i]=-V[i]*B
    elif bus_type[i]==2:
        B=0
        for j in range(numbuses):
            B=B+V[j]*Y[i][j]*sin(d[j]-d[i]+g[i][j])
        Q_spec[i]=-V[i]*B

print(P_spec)
print(Q_spec)
        
np.savetxt('Voltage.txt', (V, d, P_spec, Q_spec), fmt='%1.3f')
S, rem_cap, V_dev=limits_calc.limits(Ybus, numbuses, Sbase, Vbase,V, d)
print(S)
print(rem_cap)
print(V_dev)
