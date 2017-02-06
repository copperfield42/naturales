"""
Módulo de Números Naturales, submodulo de aritmetica modular
"""
if __name__ == "__main__" and not __package__:
    from relative_import_helper import relative_import_helper
    __package__ = relative_import_helper(__file__,1)
    del relative_import_helper
    print("idle trick")

try:
    from math import gcd
except ImportError:
    from fractions import gcd

import itertools
from functools import reduce


from .natural_typing      import Iterable, List, values
from .errores             import NoEsNumeroNatural, RequiereNumeroNaturalDesdeUno, NoInversaModularError
from .generales           import productoria, esNatural
from .generadores_primos  import descompocion_en_primos




__exclude_from_all__ = set(dir())




def mod_eq(a:int,b:int,n:int) -> bool:
    """comprueba si a==b(mod n) que se lee "a es congruente con b modulo n" """
    return a%n == b%n

def mod_exp(x:int,n:int,m:int) -> int:
    """Calcula (x^n) mod m
       (alias de pow con tres argumentos)"""
    return pow(x,n,m)

def mod_mul(a:int,b:int,n:int) -> int:
    """calcula (a*b) mod n"""
    return ((a%n)*(b%n))%n

def mod_sum(a:int,b:int,n:int) -> int:
    """calcula (a+b) mod n"""
    return ((a%n)+(b%n))%n

def mod_res(a:int,b:int,n:int) -> int:
    """calcula (a-b) mod n"""
    return ((a%n)-(b%n))%n

def mod_inv(a:int,n:int) -> "a**(-1) mod n":
    """Halla la inversa de a modulo n.
       Esto es el número x tal que
       a*x = 1 (mod n)
       entonces x= a**(-1)
       Si x no existe arroja NoInversaModularError
       una subclass de ZeroDivisionError """
    gcd,x,y = mcd_extendido( a if a>=0 else (a%n) , n)
    if gcd == 1:
        return x%n
    else:
        raise NoInversaModularError("{} no es invertible modulo {}".format(a,n))

def digital_root(n:int,base:int=10) -> int:
    """The digital root (also repeated digital sum) of a non-negative integer
       is the (single digit) value obtained by an iterative process of summing
       digits, on each iteration using the result from the previous iteration
       to compute a digit sum. The process continues until a single-digit
       number is reached.

       For example, the digital root of 65,536 is 7, because 6 + 5 + 5 + 3 + 6 = 25
       and 2 + 5 = 7.

       https://en.wikipedia.org/wiki/Digital_root"""
    if not (esNatural(base) and base>=2):
        raise ValueError("La base debe ser mayor o igual a 2")
    if esNatural(n):
        b = base-1
        m = n%b
        return b if (m == 0 and n != 0) else m
        #return 1 + ((n-1)%(base-1))
    else:
        raise NoEsNumeroNatural("El objeto no representa un número natural")


################################################################################
# ------------------------------- MCD y mcm ------------------------------------
################################################################################

def mcd(a:int,b:int) -> int:
    """Máximo Común Divisor de a y b"""
    return gcd(a,b)

def mcd_extendido(a:int,b:int) -> "(mcd,x,y)":
    """Regresa una tupla tal que mcd(a,b) = a*x + b*y"""
    #https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm
    x, u = 0, 1
    y, v = 1, 0
    while a:
        q,r = divmod(b,a)
        x,u = u, x-u*q
        y,v = v, y-v*q
        b,a = a,r
    return b,x,y

def mcm(a:int,b:int) -> int:
    """Minimo Común Multiplo de a y b"""
    #Se usa redución por el máximo común divisor
    if a==0 or b==0:
        return 0
    else:
        return (a*b)//gcd(a,b)

def sonCoprimos(a:int,b:int) -> bool:
    """Dice si dos números son coprimos.
       Dos números son coprimos si su máximo
       común divisor es 1 """
    return mcd(a,b) == 1

def coprimos(n:int):
    """Regresa un generador con los coprimos de n en el intervalo [1,n]"""
    if n >= 0 :
        return ( c for c in range(1,n+1) if gcd(c,n)==1 )
    else:
        raise NoEsNumeroNatural("El objeto no representa un número natural")

def mcm_lista(iterable:Iterable[int]) -> int:
    """Calcula el máximo común multiplo de un iterable de números."""
    return reduce(mcm,iterable)

def mcd_lista(iterable:Iterable[int]) -> int:
    """Calcula el minimo común divisor de un iterable de números."""
    return reduce(gcd,iterable)



################################################################################
### --- Funciones sobre los naturales de interes para la aritmetica modular-----
################################################################################


def indicatriz(n:int, *, modo:int=2) -> int:
    """Función indicatriz de Euler. Cuenta cuantos coprimos
       tiene el número n en el intervalo [1,n]

       También conocida como Euler's totient function

       modos:
       1)contar los coprimos de n
       2)usar los factores primos de n y aplicar la formula de Euler

       https://en.wikipedia.org/wiki/Euler%27s_totient_function """
    if modo==1:
        return sum( 1 for _ in coprimos(n) )
    elif modo==2:
        from .primalidad_test import esPrimo
        if esPrimo(n):
            return n-1
        resul = n * productoria( 1-(1/p) for p in descompocion_en_primos(n,repeticion=False ) )
        return round(resul)
    else:
        raise ValueError("modo invalido")

def carmichael_funtion(n:int) -> int:
    """Función de Carmichael.
       Se define como el m más pequeño tal que para todo coprimo a con n se cumple
       a^m = 1 (mod n)
       en.wikipedia.org/wiki/Carmichael_function"""
    if n<1:
        raise RequiereNumeroNaturalDesdeUno("Esta función sólo acepta números naturales mayores o iguales a 1")
    elif n<2:
        return 1
    else:
        copr = frozenset(coprimos(n))
        if copr:
            for m in itertools.count(1):
                if all( pow(a,m,n)==1 for a in copr ):
                    return m
        else:
            raise RuntimeError("No se encontraron coprimos")

def __multiplicative_order(a:int, n:int) -> int:
    temp = 1
    resul = 1%n
    for k in itertools.count(1):
        temp = (temp*a)%n
        if temp==resul:
            return k

def multiplicative_order(a:int, n:int) -> int:
    """Orden multiplicativo de a modulo n.
       Si a y n son números coprimos, el orden multiplicativo de a modulo n
       es el número k>=1 más pequño tal que:

       a^k = 1 (mod n)

       https://en.wikipedia.org/wiki/Multiplicative_order """
    if n>0:
        if sonCoprimos(a,n):
            return __multiplicative_order(a,n)
        else:
            raise ValueError("a y n deben ser coprimos")
    else:
        raise RequiereNumeroNaturalDesdeUno("Esta función sólo acepta números naturales mayores o iguales a 1")

def esPrimitiveRoot(a:int, n:int) -> bool:
    """Dice si a es una raiz primitiva de n.
       El número a es raiz primitiva de n si
       ambos son coprimos, y el orden multiplicativo
       de a es igual a la indicatriz de n
       http://mathworld.wolfram.com/PrimitiveRoot.html"""
    if a<=n :
        try:
            return multiplicative_order(a,n) == indicatriz(n)
        except ValueError:
            pass
    return False

def raicesPrimitivas(n:int) -> List[int]:
    """Da una lista con las raices primitivas de n si tiene alguna.
       https://en.wikipedia.org/wiki/Primitive_root_modulo_n"""
    if n>=0:
        if n==1:
            return [0]
        resul = list()
        ind = 0
        for ind, a in enumerate(coprimos(n),1):
            resul.append( (a,__multiplicative_order(a,n)) )
        return [ rp for rp,mo in resul if mo == ind ]
    else:
        raise NoEsNumeroNatural("El objeto no representa un número natural")

def discrete_log(a:int, g:int, n:int) -> int :
    """log_g(a) (mod n) El logaritmo discreto en base g de a modulo n
       se sefine como el numero k más pequeño tal que:

       a = g^k (mod n)

       http://mathworld.wolfram.com/DiscreteLogarithm.html
       https://en.wikipedia.org/wiki/Discrete_logarithm"""
    if sonCoprimos(a,n):
        ind = indicatriz(n)
        try:
            if ind == multiplicative_order(g,n):  #esPrimitiveRoot(g,n):
                for r in range(1,ind):
                    if a%n == pow(g,r,n):
                        return r
            raise ValueError
        except ValueError:
            raise ValueError("{} debe ser raiz primitiva de {}".format(g,n) )
    else:
        raise ValueError("{} y {} deben ser coprimos".format(a,n))

def __jacobi_simbol(a:int, n:int) -> "-1,0,1":
    """https://cryptocode.wordpress.com/2008/08/16/jacobi-symbol/
       correcto para la tabla en
       https://en.wikipedia.org/wiki/Jacobi_symbol"""
    #version que hace el trabajo, y se olvida de verificar las precondiciones,
    #debido a la naturaleza recursiva del mismo, solo las verifico con la
    #otra versión, que es la de entrada y esta hace el trabajo
    #asumiendo que siempre se cumplen si al principio se cumplen
    if a==0:
        return 1 if n==1 else 0
    elif a==2:
        return 1 if n%8 in (1,7) else -1
    elif a==-1:
        return 1 if n%4==1 else -1
    elif a<0:
        return __jacobi_simbol(-1,n) * __jacobi_simbol(-a,n)
    elif a>=n:
        return __jacobi_simbol( a%n, n )
    elif not a&1:#si a es par
        return  __jacobi_simbol(2,n) * __jacobi_simbol(a//2,n)
    else:
        return -__jacobi_simbol(n,a) if a%4==3 and n%4==3 else __jacobi_simbol(n,a)

def jacobi_simbol(a:int, n:int) -> values(-1,0,1):
    """Símbolo de Jacobi.
       https://en.wikipedia.org/wiki/Jacobi_symbol
       http://mathworld.wolfram.com/JacobiSymbol.html """
    #version que verifica las precondiciones
    if n >= 0 :
        if n&1:#si n es impar
            return __jacobi_simbol(a,n)
        else:
            raise ValueError("n debe ser impar")
    else:
        raise ValueError("El parametro n debe ser un número natural")





__all__ =[ x for x in dir() if not (x.startswith("_") or x in __exclude_from_all__)]
del __exclude_from_all__
