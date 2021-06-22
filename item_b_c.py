import numpy as np
from utils import *

#item = True for b) and False for c)
def item_b_c(item  ):
    # definindo valores do item
    case=int(input("Qual dos casos do enunciado será testado (1, 2 ou 3, respectivamente)\n?"))
    mass=int(input("Para análisar gráficamente o comportamento de uma massa específica digite seu número, para analisar todas em conjunto digite 0:\n"))
    m=2
    n = 5 if item else 10

    #definindo se ocorre deslocamento
    hasShift = True

    #definindo auto-valores e auto-vetores pelo metodo qr com deslocamento
    eigenvalues,eigenvectors,iteracoes = qr_shifted(get_A(n,m, 0), hasShift)

    #invertendo auto-vetores e auto-valores para serem compatíveis com a ordem das massas 
    #o método QR implementado retorna valores com ordem invertida
    #quanto maior o coeficiente elastico maior a frequencia
    frequencies = eigenvalues[::-1]**(1/2)
    eigenvectors = eigenvectors[::-1]

    #mostrando valores de frequências e modos de vibração
    print('frequências:\n')
    show(frequencies, 0)
    print('modos de vibração:\n')
    show(eigenvectors, 1)

    # definindo deslocamentos iniciais para item c
    if not item:
        for i,key in enumerate(X_0):
            case_deslocs=X_0[key]
            for j in range(len(case_deslocs)):
                case_deslocs.append(case_deslocs[j])

    #adicionando modo 3 a X_0 (modo de vibracao referente a maior frequencia)
    X_0['case3']=eigenvectors[np.argmax(eigenvalues)]

    #mostrando grafico de deslocamento das molas
    get_plot(case,X_0, frequencies, eigenvectors, mass)