import numpy as np
from utils import *

def item_a():
    #definindo valores do item
    n = int(input("Qual o tamanho da matriz?\n"))
    hasShift = int(input('Haverá deslocamento no algoritmo (0 para não e 1 para sim)?\n'))

    #criando matriz tridiagonal simetrica
    A = np.eye(n)*2
    for i in range(0,n):
        if i>0:
            A[i,i-1]=-1
        if i<n-1:
            A[i,i+1]=-1

    #obtendo valores da solucao
    eigenvalues, eigenvectors, iterations = qr_shifted(A, hasShift)

    #mostrando solucao
    print('\niterações: %s\n' %iterations)
    print('auto-valores')
    show(eigenvalues, 0)
    print('auto-vetores')
    show(eigenvectors, 1)

    #resultados conhecidos analiticamente
    vals=[]
    for i in range (1, n+1):
        lamb=2*(1-np.cos(i*np.pi/(n+1)))
        vals.append(lamb)

    vets=[]
    for i in range (1, n+1):
        vet = []
        for j in range (1, n+1):
            v=np.sin(i*j*np.pi/(n+1))
            vet.append(v)
        vet = vet/np.linalg.norm(vet)
        vets.append(vet)
    print('GABARITO:\n')
    print('auto-valores')
    show(vals, 0)
    print('auto-vetores')
    show(vets, 1)