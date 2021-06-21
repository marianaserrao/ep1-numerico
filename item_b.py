import numpy as np
import math
from utils import *

# definindo valores do item
n = 5
m=2
case=3

#definindo se ocorre deslocamento
hasShift = True

#definindo auto-valores e auto-vetores pelo metodo qr com deslocamento
eigenvalues,eigenvectors,iteracoes = qr_shifted(get_A(n,m, 0), hasShift)

print('frequências:\n')
show(eigenvalues, 0)
print('modos de vibração:\n')
show(eigenvectors, 1)
X_0['case3']=eigenvectors[np.argmax(eigenvalues)]

get_plot(case,X_0, eigenvalues)