import numpy as np
import math
from utils import *

#criando matriz tridiagonal simetrica
n = int(input("Qual o tamanho da matriz?"))

A = np.eye(n)*2
for i in range(0,n):
    if i>0:
        A[i,i-1]=-1
    if i<n-1:
        A[i,i+1]=-1

#definindo se ocorre deslocamento
hasShift = True

eigenvalues, eigenvectors, iterations = qr_shifted(A, hasShift)

print('\niterações: %s\n' %iterations)
print('autovalores')
show(eigenvalues, 0)
print('autovetores')
show(eigenvectors, 1)

#resultados conhecidos analiticamente
vals=[]
for i in range (1, n+1):
    lamb=2*(1-math.cos(i*math.pi/(n+1)))
    vals.append(lamb)

vets=[]
for i in range (1, n+1):
    vet = []
    for j in range (1, n+1):
        v=math.sin(i*j*math.pi/(n+1))
        vet.append(v)
    vets.append(vet)
print('GABARITO:\n')
print('autovalores')
show(vals, 0)
print('autovetores')
show(vets, 1)