import numpy as np
import matplotlib.pyplot as plt

#criterio de parada de iteracoes
err=10**(-6)

# definindo deslocamentos iniciais (itens b e c)
X_0 = {
    'case1': [-2,-3,-1,-3,-1],
    'case2': [1,10,-4,3,-2],
}

#print colored items in array (0 for pink, 1 for green)
def show(items, color=2):
    for index,value in enumerate(items):
        # c = ['95m','32m','0m']
        print("%s: %s" %(index+1,np.round_(value, 3)))
    print()

#obtendo valores do seno e cosseno para a rotacao de givens
def get_givens_params(A, k):
    alfa = A[k,k]
    beta = A[k+1,k]
    if abs(alfa)>abs(beta):
        t = -beta/alfa 
        c = 1/((1+t**2)**(1/2))
        s=c*t
    else:
        t = -alfa/beta
        s = 1/((1+t**2)**(1/2))
        c=s*t
    return (c, s)

#obtendo cada transformacao de givens
def get_q(c, s, k, m):
    q=np.identity(m)
    q[k,k]=q[k+1,k+1]=c
    q[k,k+1]=-s
    q[k+1,k]=s
    return q 

# obtendo decomposicao QR
def get_qr_decomposition(A):
    k=0
    R=A
    m=np.size(A,0)
    Q = np.identity(m)
    while k<=m-2:
        c,s = get_givens_params(R,k)
        q=get_q(c,s,k,m)
        Q = Q@(q.T)
        R=q@R
        k+=1
    return (Q, R) 

#obtendo auto-valores e auto-vetores com ou sem (hasShift) deslocamento espectral
def qr_shifted(A, hasShift, err=err):
    m = n = np.size(A,0)
    V=np.identity(n)
    A_=A
    u=0
    k=0
    
    #iteracao para cada auto-valor
    while m>=2:
        #iterando decomposicoes QR
        while abs(A_[m-1,m-2])>err:
            #definindo deslocamento espectral
            if k>0 and hasShift:
                d = (A_[m-2,m-2]-A_[m-1,m-1])/2
                sgn = np.sign(d or 1)
                u=A_[m-1,m-1]+d-sgn*(d**2+A_[m-1,m-2]**2)**(1/2)

            uI=u*np.identity(m)
            A_[0:m,0:m]-=uI
            Q,R = get_qr_decomposition(A_[0:m,0:m])
            A_[0:m,0:m]=R@Q+uI
            V[:,0:m]=V[:,0:m]@Q
            k+=1
        m-=1

    eigenvalues = np.diag(A_)
    eigenvectors = V.T
    iterations = k

    return (eigenvalues, eigenvectors, iterations)


# ITENS B E C

# obtendo valores para matriz A
def get_k(i, item):
    k = 40+2*i if item ==0 else 40+2*(-1)**i
    return k

# obtendo matriz A (0 para item b e 1 para item c)
def get_A(n , m, item):
    A=np.zeros([n,n])
    for i in range(n):
        A[i,i]=get_k(i+1, item)+get_k(i+2, item)
        if i<n-1:
            A[i,i+1]=-get_k(i+2, item)
        if i>0:
            A[i,i-1]=-get_k(i+1, item)
    return A/m

# obtendo graficos
def get_plot(case, X_0, frequencies, eigenvectors, mass=0):

    X_0=X_0['case'+str(case)]

    # array contendo os coeficientes "a" de cada mola (Coversao X(t)->Y(t): Y(t)=Q.T*X(t))
    A=(eigenvectors.T)@X_0

    # valores de tempo
    t = np.arange(0 , 60, 0.01)

    # matriz que conterá as posicoes (coluna: tempo, linha: mola)
    Y_t=np.zeros([len(X_0),len(t)])

    #preenchendo a matriz X_t de acordo com a solucao geral (velocidade inicial = 0 -> coeficiente 'b' = 0)
    for (i,j) , x in np.ndenumerate(Y_t):
        Y_t[i,j]=A[i]*np.cos(frequencies[i]*t[j])

    #coversao Y(t)->X(t): X(t)=Q*Y(t)
    X_t=eigenvectors@Y_t

    #criando grafico
    fig, ax = plt.subplots()

    #gerando escala de cores para o grafico
    c = plt.cm.get_cmap('hsv', len(X_0)+1)

    #se o parametro mass for passado apenas o deslocamento da massa escolhida aparecera no grafico
    if mass:
        ax.plot(t, X_t[mass-1])
        plt.title('Deslocamento das Massa ' + str(mass))
    else:
        for i in range(len(X_0)):
            label='Massa '+str(i+1)
            ax.plot(t,X_t[i], color=c(i), label=label)
            ax.legend()
            plt.title('Deslocamento das Massas')

    plt.xlabel('Tempo (s)')
    plt.ylabel('Deslocamento (m)')
    plt.grid(True)
    plt.show()