""" Módulo de Números Naturales

Funciones sobre los numeros naturales 

"""
if __name__ == "__main__" and not __package__:
    print("idle trick")
    from relative_import_helper import relative_import_helper
    __package__ = relative_import_helper(__file__,1)
    del relative_import_helper

import itertools  
from decimal import Decimal


from .errores              import NoEsNumeroNatural, RequiereNumeroNaturalDesdeUno
from .clasificaciones      import esPrimo, esFermatNumber, esImpar, esPseudoprimoFuerte
from .factorizacion        import factorizacion, descompocion_en_primos
from .generales            import productoria, log

__exclude_from_all__=set(dir())

from .aritmetica_modular   import jacobi_simbol
from .generales            import isqrt
from .primos               import primordial

from . import combinatoria, aritmetica_modular

################################################################################
### --------------------------- Factorizacion ----------------------------------
################################################################################


def factorizacion_fermat_number(n) -> [int]:
    """Factoriza el número de fermat dado"""
    k = esFermatNumber(n,valor=True)
    if k is not None:
        dos = 2**(k+2)
        resul = list()
        while n!=1:
            if esPrimo(n):
                resul.append(n)
                print("n=",n,"es primo")
                n = 1
            else:
                for x,f in enumerate(itertools.count(dos+1,dos),1):
                    #f = x*dos +1
                    if n%f == 0:
                        resul.append(f)
                        print("n=",n,"tiene con x=",x,", factor de x*2^(%d+2)+1 ="%k,f)
                        n //= f
                        break
        return resul
    else:
        raise ValueError("No es un numero de Fermat")



################################################################################
### ----------------------- Funciones sobre los naturales ----------------------
################################################################################


def _moebius(n:int)-> "-1,0,1":
    """moebius(n) esta definida para todos los números naturales n (desde el 1)
       y tiene valores en (-1, 0, 1) dependiendo en la factorizacion de n
       en sus factores primos.

       Se define como sigue:
       * moebious(n) = 1  si n es libre de cuadrados y tiene un número par
         de factores primos distintos.
       * moebiuos(n) = -1 si n es libre de cuadrados y tiene un número impar
         de factores primos distintos.
       * moebiuos(n) = 0  si n es divisible por algún cuadrado."""
    if n >= 0:
        if n>0:
            if n==1:
                return 1
            else:
                fp=factorizacion(n)
                w=len(fp)
                om=0
                for p,m in fp:
                    om+=m
                if w==om:
                    return (-1)**w
                else:
                    return 0
        else:
            raise RequiereNumeroNaturalDesdeUno("Esta función sólo acepta números naturales mayores o iguales a 1")
    else:
        raise NoEsNumeroNatural("El objeto no representa un número natural")


def moebius(n:int,*,verbose:bool=False) -> "-1,0,1":
    """moebius(n) esta definida para todos los números naturales n (desde el 1)
       y tiene valores en (-1, 0, 1) dependiendo en la factorizacion de n
       en sus factores primos.

       Se define como sigue:
       * moebious(n) = 1  si n es libre de cuadrados y tiene un número par
         de factores primos distintos.
       * moebiuos(n) = -1 si n es libre de cuadrados y tiene un número impar
         de factores primos distintos.
       * moebiuos(n) = 0  si n es divisible por algún cuadrado."""
    m = _moebius(n)
    if m not in [-1,0,1]:
        raise RuntimeError("Error fatal: la función de moebius dio un resultado diferente de -1, 0 ó 1")
    if verbose:
        print("Se encontro que el número",n,"",end="")
        if m==1 or m==-1:
            print("es libre de cuadrados y tiene un número", "par" if m==1 else "impar" ,
                  "de factores primos distintos")
        elif m==0:
            print("es divisible por algun cuadrado")
    return m




def legendre_simbol(a:int,n:int) -> "-1,0,1":
    """Símbolo de Legendre
       https://en.wikipedia.org/wiki/Legendre_symbol"""
    if esPrimo(n):
        return jacobi_simbol(a,n)
    else:
        raise ValueError("El argumento n debe ser un número primo")

def liouville_function(n:int) -> "-1,1":
    """Calcula la función de Liouville.
       en.wikipedia.org/wiki/Liouville_function"""
    resul=0
    for p in descompocion_en_primos(n):
        resul += 1
    return (-1)**resul

def mertens_function(n:int) -> int:
    """Calcula la función de Mertens.
       en.wikipedia.org/wiki/Mertens_function"""
    return sum( moebius(k) for k in range(1,n+1) )

def radical(n:int,t:int=None) -> int:
    """Regresa el radical de n.
       El radical de n se define como el producto de
       todos los diferentes factores primos de n.
       Si t es suministrado, calcula el mayor divisor
       t-libre de n, que en el caso por defecto, t es 2
       por lo que se calcula el mayor divisor libre de
       cuadrados de n.

       https://en.wikipedia.org/wiki/Radical_of_an_integer"""
    if t is None or t==2:
        return productoria( descompocion_en_primos(n,repeticion=False) )
    else:
        return productoria( map(lambda par: par[0]**min(par[1],t-1),factorizacion(n)) )

def quality(a,b,c,*,context=None) -> Decimal:
    """Calcula log(c)/log(radical(abc))"""
    return log(radical(a*b*c),c,context=context)






################################################################################
### ------------------------------ Miselaneos ----------------------------------
################################################################################


def smallPsPF(aprueba,falla,inicio=9,verbose=True,muestra=10**6) -> int:
    """Calcula cual es el número más pequeño desde inicio tal que
       es Pseudoprimo Fuerte en las bases 'aprueba' pero no en las 'falla' """
    for n in itertools.count( inicio if esImpar(inicio) else (inicio+1) , 2 ):
        if verbose and n%muestra in (1,0):
            print("n=",n)
        if esPseudoprimoFuerte(n,aprueba) and not esPseudoprimoFuerte(n,falla):
            if verbose :
                print("NUMERO ENCONTRADO:",n)
            return n



__all__ = list( x for x in dir() if not (x.startswith("_") or x in __exclude_from_all__))
del __exclude_from_all__
