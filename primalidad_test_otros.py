""" Submodulo de pruebas de primalidad para determinar si un número es primo

Ofrece variedad de pruevas de primalidad
"""

if __name__ == "__main__" and not __package__:
    print("idle trick")
    from relative_import_helper import relative_import_helper
    __package__ = relative_import_helper(__file__,1)
    del relative_import_helper


import random, itertools
from decimal import Decimal

#from ._Naturales      import *
from .errores             import NoEsNumeroNatural
from .generales           import esCuadradoPerfecto, log
from .aritmetica_modular  import jacobi_simbol, sonCoprimos, mcd, indicatriz
from ._secuencias         import sucesiones_de_Lucas
from .clasificaciones     import esUnaPotencia, esFermatNumber, esProthNumber
from .combinatoria        import factorial
from .factorizacion       import factorizacion_ds 


__exclude_from_all__=set(dir())


################################################################################
### ---------------------- Otros test de primalidad ----------------------------
################################################################################


def primalidad_Test_Fermat(n:int,k:int=10,*,todos=False) -> bool:
    """Test de primalidad de Fermat
    Dice si un número es un posible primo
    n número a comprobar
    k número de veces a repetir el test, por defecto 10
    todos: repetir la prueba para todos los posibles valores
    en que tiene sentido la misma.

    https://en.wikipedia.org/wiki/Fermat_primality_test"""
    if n >= 0 :
        if n>3:
            if todos:
                return all( pow(a,n-1,n)==1 for a in range(2,n-1))
            ran=random.Random()
            for j in range(k):
                a=ran.randint(2,n-2)
                if not pow(a,n-1,n)==1:
                    return False
            return True
        else:
            return n==2
    else:
        raise NoEsNumeroNatural("El objeto no representa un número natural")


def primalidad_Test_Wilson(n:int) -> bool:
    """(n-1)! = -1 (mod n)
       https://en.wikipedia.org/wiki/Wilson%27s_theorem"""
    if n>=0:
        if n>1:
            return factorial(n-1,n) == n-1
        return False
    else:
        raise NoEsNumeroNatural("El objeto no representa un número natural")


def primalidad_Test_Pepin(f:int) -> bool:
    """Dice si el número de fermat f es primo
       https://en.wikipedia.org/wiki/P%C3%A9pin%27s_test"""
    if esFermatNumber(f):
        if f>3:
            return pow( 3, (f-1)//2 , f ) == f-1
        else:
            return True
    else:
        raise ValueError("No es un numero de Fermat")


def primalidad_Test_Proth(p:int) -> bool:
    """Dice si el Proth number dado es primo
       https://en.wikipedia.org/wiki/Proth%27s_theorem"""
    if esProthNumber(p):
        for a in range(2,p):
            if pow(a, (p-1)//2 , p)== p-1:
                return True
        return False
    else:
        raise ValueError("No es un número de Proth")



def esLucasPseudoprimoExtraFuerte(n:int,*,verbose=False) -> bool:
    """Dice si el número es un Pseudo Primo Extra Fuerte de Lucas.
       Estos son los números tales que:
       Sea d,s números tales que d*2^s = n+1 y sean Q=1 y
       P perteneciente a [3,4,5,6...] tal que con D = P^2 -4Q
       el simbolo de Jacobi es (D/n)==-1 cumplen alguna de las
       siquientes ondiciones:

       Ud(P,Q) = 0 (mod n) y Vd(P,Q) =+-2 (mod n)
       o
       V(d*2^r)(P,Q) = 0 (mod n) para algun 0 <= r < s-1

       donde Ux y Vx representan las sucesiones de Lucas y primer y
       segundo tipo.


       en.wikipedia.org/wiki/Lucas_pseudoprime#Strong_Lucas_pseudoprimes"""
    if n >= 0:
        if n<2:
            return False
        elif n<4:
            return True
        elif not n&1 or n%3==0:
            return False
        if not esCuadradoPerfecto(n):
            P=3
            for P in itertools.count(3):
                D = P**2 -4
                if jacobi_simbol(D,n)==-1:
                    break
            d,s = factorizacion_ds(n+1)
            if verbose: print("base:",P,"d=",d,"s=",s)
            Ud,Vd = sucesiones_de_Lucas(d,P,1,n)
            if Ud == 0 and Vd in {2,n-2}:
                if verbose: print("Condicion 1")
                return True
            if Vd == 0:
                if verbose: print("Condicion 2, 0")
                return True
            for r in range(1,s-1):
                Vd = (Vd**2 -2) % n
                if Vd == 0:
                    if verbose: print("Condicion 2, ",r)
                    return True
        else:
            if verbose: print("es cuadrado perfecto")
        return False
    else:
        raise NoEsNumeroNatural("El objeto no representa un número natural")




def fermat_test(n:int,testigo:int) -> bool:
    """Test de primalidad de Fermat
    Dice si un número es un posible primo bajo el testigo
    suministrado. Si el test es falso, con certesa el
    número es compuesto, pero si acierta solo se puede decir
    que podria ser un primo.

    Implementación del pequeño teorema de Fermat:

    a^(n-1) = 1 (mod n)

    con a el testigo suministrado.    """
    return pow(testigo,n-1,n)==1




def __aks_multiplicative_order(n,r,limite) -> bool:
    """Dice si multiplicative_order(n,r)>limite haciendo el calculo
       parcial del multiplicative_order(n,r)"""
    if sonCoprimos(n,r):
        temp = 1
        n %= r
        for k in range(1,limite+1):
            temp = (temp*n)%r
            if temp == 1: # encontre el orden multipicativo k
                return False #k <= limite
        return True #k > limite
    return False

def __aks_find_r(n:int,log_of_n=None,*,verbose=False) -> int:
    """Encuentra el r>=2 más pequeño tal que el orden multiplicativo de n modulo r
       sea mayor que el cuadrado del logaritmo de n.
       multiplicative_order(n,r) > log2(n)**2"""
    if not log_of_n:
        log_of_n = log(2,n)
    maxr = max(3,round(log_of_n**5)) + 1 #lema 4.3 del paper
    cota = round(log_of_n**2)+1
    if verbose :
        print("Buscando r en [ 2,",maxr,")","cota=",cota)
    for r in range(2, maxr):
        if __aks_multiplicative_order(n,r,cota):
            return r
        elif verbose and r%10000==0:
            print("probandos",r,"se ha escaneado el",100*r/maxr,"%")
    raise RuntimeError("Falla al encontrar el r")



def primalidad_Test_AKSv2(n:int,*,verbose:bool=False) -> bool:
    """http://www.cse.iitk.ac.in/users/manindra/algebra/primality_v6.pdf
       https://en.wikipedia.org/wiki/AKS_primality_test"""
    if n >= 0 :
        if n<2:
            return False
        elif n<4:
            return True
        elif not n&1 or n%3==0:
            return False
        else:
            #checar que no sea una potencia
            if verbose:print("paso 1")
            if esUnaPotencia(n):
                return False
            if verbose:print("paso 2")
            log2n = log(2,n)
            r = __aks_find_r(n,log2n,verbose=verbose)
            if verbose:print("paso 3","mi r=",r)
            a = r
            while a>1:
                #gcd = mcd(a,n)
                #print("gcd(%d,%d)"%(a,n),"=",gcd)
                if 1 < mcd(a,n) < n:
                    return False
                a -= 1
            if verbose:print("paso 4")
            if n <= r:
                return True
            if verbose:print("paso 5")
            techo = int( log2n * Decimal( indicatriz(r) ).sqrt() )
            a = 1
            if verbose:print("max",techo)
            while a <= techo:
                if pow(a,n,n)-a :#!=0:
                    return False
                a += 1
            if verbose:print("paso 6")
            return True
    else:
        raise NoEsNumeroNatural("El objeto no representa un número natural")



__all__ = list( x for x in dir() if not (x.startswith("_") or x in __exclude_from_all__))
del __exclude_from_all__