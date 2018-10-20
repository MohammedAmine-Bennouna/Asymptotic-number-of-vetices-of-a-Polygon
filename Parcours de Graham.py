import random
import math
import matplotlib.pyplot as plt
import time



#Calcule l'angle entre (pivot, b) et (pivot,a)
def calcul_angle(b,a): 
    x=a[0]-b[0]
    y=a[1]-b[1]
    if a==b :
        return(-1) #condition pour que le pivot soit le premier element de la liste triee
    elif x==0 :
        return (math.pi/2)
    theta=math.atan(y/x)
    if x<0 :  
        return (-theta)
    else :
        return(math.pi-theta)
    

#Determine le point de plus petit ordonnée
def Pivot(l): 
    min=l[0][1]
    indice=0
    for i in range(1,len(l)) :
        if l[i][1]<min :
            min=l[i][1]
            indice=i
    return(l[indice])

#Determine si le tournant est gauche ou droit
def Tournant(a,b,c,bool = True):  
    val=(b[0]-a[0])*(c[1]-a[1])-(c[0]-a[0])*(b[1]-a[1])
    if val<0 :
        return True   #Tournant à gauche
    if val>0 :
        return False    #Tournant à droite
    return (bool) #bool est relatif a la definition de la convexité adoptee : si on garde trois point alignés ou pas


#Renvoi la liste des points triée par ordre croissant d'angle
def liste_angles_triee(l,pivot):  
    
    liste = sorted(l, key=(lambda a: calcul_angle(pivot,a)))
    
    return(liste) 

#Implementation de l'algorithme de Graham
def parcours_de_graham(Points):  
    pivot=Pivot(Points)
    list=liste_angles_triee(Points,pivot) #liste des points triee par ordre croissant des angles
    Pile=[pivot,list[1],list[2]] #le premier element de la liste est le pivot
    compteur=2
    n=len(Points)
    list.append(pivot)
    while (compteur<n):
        tournant=Tournant(Pile[-3],Pile[-2],Pile[-1])
        if tournant:         #Si c'est un tournant à gauche 
            compteur+=1
            Pile.append(list[compteur])
        else :               #Sinon
            sommet=Pile.pop()
            Pile.pop()
            Pile.append(sommet)


    Pile.append(pivot)   #Traitement des trois derniers points
    tournant=Tournant(Pile[-3],Pile[-2],Pile[-1])
    if not(tournant): 
        sommet=Pile.pop()
        Pile.pop()
        Pile.append(sommet)
        
    
    return(Pile) #retourne la liste des points constituant l'enveloppe convexe



#Trace l'enveloppe convexe d'une liste de points E
def tracer_EC(E):  
    X=[]
    Y=[]
    for i in range (len(E)):
        X.append(E[i][0])
        Y.append(E[i][1])
    
    plt.plot(X,Y, color = 'b')


#Affiche n points aléatoires dans le cercle unité et leur enveloppe convexe
def AfficheGraham(n):  
    L = generate_polaire(n)
    affiche(L)
    E= parcours_de_graham(L)
    tracer_EC(E)
    

#L'espérance de la taille de l'enveloppe convexe pour n points
def Esperance (n,m=30): 
    e = 0               #m représente le nombre de simulation pour avoir une taille moyenne pour tout n
    for k in range(m):
        L = generate_cart(n)
        Ec = parcours_de_graham(L)
        a = len (Ec)
        e = e+a
    return (e/(m))


#Tracée de l'espérance en fonction de n
def tracer_esperance(n): 
    
    X=[k for k in range(5, n+1)]
    Y=[Esperance(k) for k in range(5 , n+1)]
    
    plt.plot(X,Y)
        

#Tracée de c*n^(1/3)
def tracerapprox(c,n): 
    
    X=[k for k in range(5, n+1)]
    Y=[c*k**(1/3) for k in range(5 , n+1)]
    
    plt.plot(X,Y)



def estimationC(n):
    Y=[Esperance(k) for k in range(5 , n+1)]
    X=[Y[k-5]/(k**(1/3)) for k in range(5, n+1)]
    C = sum(X)/(n-4)
    return C

def estimatioMINMAX(n,m):
    Lmin=[]
    Lmax=[]
    for i in range (m):
        Y=[Esperance(k) for k in range(5 , n+1)]
        X=[Y[k-5]/(k**(1/3)) for k in range(5, n+1)]
        Lmin.append(min(X))
        Lmax.append(max(X))
    C1= sum(Lmin)/m
    C2= sum(Lmax)/m
    return (C1,C2)