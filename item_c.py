import numpy as np
import math
from utils import *

# definindo valores do item
n = 10
m=2
case=int(input("Qual dos casos do enunciado será testado (1, 2 ou 3, respectivamente)?"))

#definindo se ocorre deslocamento
hasShift = True

#definindo auto-valores e auto-vetores pelo metodo qr com deslocamento
eigenvalues,eigenvectors,iteracoes = qr_shifted(get_A(n,m, 0), hasShift)

frequencies = eigenvalues[::-1]**(1/2)
eigenvectors = eigenvectors[::-1]

#mostrando valores de frequências e modos de vibração
print('frequências:\n')
show(frequencies, 0)
print('modos de vibração:\n')
show(eigenvectors, 1)

# definindo deslocamentos iniciais
for i,key in enumerate(X_0):
    case_deslocs=X_0[key]
    for j in range(len(case_deslocs)):
        case_deslocs.append(case_deslocs[j])
X_0['case3']=eigenvectors[np.argmax(eigenvalues)]

#mostrando grafico de deslocamento das molas
get_plot(case,X_0, frequencies, eigenvectors)