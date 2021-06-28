import numpy as np
import matplotlib.pyplot as plt

#criterio de parada de iteracoes
err=10**(-6)

#print colored items in array (0 for pink, 1 for green)
def show(items):
    for index,value in enumerate(items):
        print("%s: %s\n" %(index+1,np.round_(value, 3)))

# obtendo decomposicao QR
def get_qr_decomposition(A):
    k=0
    R=A.copy()
    m=np.size(A,0)
    Q = np.identity(m)

    #funcao para obtencao dos valores do seno e cosseno para a rotacao de givens
    def get_givens_params():
        alfa = R[k,k]
        beta = R[k+1,k]
        if abs(alfa)>abs(beta):
            t = -beta/alfa 
            c = 1/((1+t**2)**(1/2))
            s=c*t
        else:
            t = -alfa/beta
            s = 1/((1+t**2)**(1/2))
            c=s*t
        return (c, s)

    #funcao para obtencao de cada transformacao de givens
    def get_q():
        q=np.identity(m)
        q[k,k]=q[k+1,k+1]=c
        q[k,k+1]=-s
        q[k+1,k]=s
        return q 

    #loop para decomposicao qr
    while k<=m-2:
        c,s = get_givens_params()
        q=get_q()
        Q = Q@(q.T)
        R=q@R
        k+=1

    return (Q, R) 

#obtendo auto-valores e auto-vetores com ou sem (hasShift) deslocamento espectral
def qr_shifted(A, hasShift, err=err):
    m = n = np.size(A,0)
    V=np.identity(n)
    A_=A.copy()
    u=0
    k=0

    #funcao para obtencao do deslocamento
    def get_Shift():
        u=0
        I=np.identity(m)
        if k>0 and hasShift:
            d = (A_[m-2,m-2]-A_[m-1,m-1])/2
            sgn = np.sign(d or 1)
            u=A_[m-1,m-1]+d-sgn*(d**2+A_[m-1,m-2]**2)**(1/2)
        return u*I
    
    #iteracao para cada auto-valor
    while m>=2:
        #iterando decomposicoes QR para 'zerar' beta
        while abs(A_[m-1,m-2])>err:

            #definindo deslocamento espectral
            shift = get_Shift()

            A_[0:m,0:m]-=shift
            Q,R = get_qr_decomposition(A_[0:m,0:m])
            A_[0:m,0:m]=R@Q+shift
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

#alterando base para simplificar solucao (posicao dependendo de apenas uma variavel)
def get_Y_0(case, X_0, eigenvectors):

    #selecionando caso desejado do dicionario X_0
    X_0=X_0['case'+str(case)].copy()

    # conversao X(t)->Y(t): Y(t)=Q.T*X(t), obtendo Y_0 (array que contem os coeficientes 'a')
    Y_0=eigenvectors@X_0

    return Y_0

def get_Y_t(A, frequencies, t):
    Y_t=np.zeros([len(A), len(t)])

    #preenchendo a matriz Y_t de acordo com a solucao geral (velocidade inicial = 0 -> coeficiente 'b' = 0)
    for (i,j),y in np.ndenumerate(Y_t):
        Y_t[i,j]=A[i]*np.cos(frequencies[i]*t[j])
    
    return Y_t

# obtendo graficos
def get_plot(X_t, t, comparative=0):

    masses_amount = np.size(X_t,0)

    #definindo numero de graficos na imagem
    sub = 1 if comparative else masses_amount

    #criando o grafico
    fig, axs = plt.subplots(sub, sharey=True, sharex=True)

    #gerando escala de cores para o grafico
    c = plt.cm.get_cmap('hsv', masses_amount+1)

    #funcao para plotagem de cada massa
    def plot_line(ax):
        label='Massa '+str(i+1)
        ax.plot(t,X_t[i], color=c(i), label=label)
        ax.grid(True)
        ax.legend()

    #criando grafico
    if comparative:
        for i in range(masses_amount):
                plot_line(axs)
    else:
        for i, ax in enumerate(axs):
            plot_line(ax)
            

    fig.suptitle('Deslocamento das Massas (m) por Tempo (s)', fontsize='xx-large')
    plt.xlabel('Tempo (s)')
    plt.show()