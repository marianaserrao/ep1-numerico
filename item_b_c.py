import numpy as np
from utils import *

#item = True for b) and False for c)
def item_b_c(item  ):
    # definindo valores do item
    case=int(input("Qual dos casos do enunciado será testado (1, 2 ou 3, respectivamente)?\n"))
    mass=int(input("Para análisar gráficamente o comportamento de uma massa específica digite seu número, para analisar todas em conjunto digite 0:\n"))
    m=2
    n = 5 if item else 10

    #definindo deslocamentos iniciais
    X_0 = {
        'case1': [-2,-3,-1,-3,-1],
        'case2': [1,10,-4,3,-2],
    }

    #definindo se ocorre deslocamento
    hasShift = True

    #definindo auto-valores e auto-vetores pelo metodo qr com deslocamento
    eigenvalues,eigenvectors = qr_shifted(get_A(n,m, 0), hasShift)[0:2]

    #invertendo auto-vetores e auto-valores para serem compatíveis com a ordem das massas 
    #o método QR implementado retorna valores com ordem invertida
    #quanto maior o coeficiente elastico maior a frequencia
    eigenvalues = eigenvalues[::-1]
    eigenvectors = eigenvectors[::-1]

    #frequencias sao iguais as raizes dos auto-valores
    frequencies=eigenvalues**(1/2)

    #mostrando valores de frequências e modos de vibração
    print('\nfrequências:\n')
    show(frequencies)
    print('modos de vibração:\n')
    show(eigenvectors)

    # definindo deslocamentos iniciais para item c
    if not item:
        for i,key in enumerate(X_0):
            case_deslocs=X_0[key]
            for j in range(len(case_deslocs)):
                case_deslocs.append(case_deslocs[j])

    #adicionando modo 3 a X_0 (modo de vibracao referente a maior frequencia)
    X_0['case3']=eigenvectors[np.argmax(frequencies)]

    #obtendo valores de 'a' (da solucao geral: ai=y0i)
    A=get_Y_0(case, X_0, eigenvectors)

    # definindo os valores de tempos a serem plotados no grafico
    t = np.arange(0, 10, 0.025)

    # obtendo matriz de posicoes (linha: massa, coluna: tempo)
    Y_t=get_Y_t(A, frequencies, t)

    #voltando a base inicial
    X_t=(eigenvectors.T)@Y_t

    #mostrando grafico de deslocamento das molas
    get_plot(X_t, t, mass)