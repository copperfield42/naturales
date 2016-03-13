""" 
Módulo de Números Naturales, submodulo de factorizacion de numeros 

"""
if __name__ == "__main__" and not __package__:
    print("idle trick")
    from relative_import_helper import relative_import_helper
    __package__ = relative_import_helper(__file__,1)
    del relative_import_helper

#from ._Naturales      import *

import collections, itertools, operator

from .errores             import NoEsNumeroNatural
from .generales           import productoria
from .generadores_primos  import primos_hasta 



__exclude_from_all__ = set(dir())

from .generadores_primos import descompocion_en_primos 

def factorizacion_ds(n:int) -> (int,int):
    """Regresa una tupla (d,s) con d impar tales que n = d*(2^s) [+1](segun n sea impar o no)

       Si n es par halla:       n  = d*2^s
       Si n es impar halla:   n -1 = d*2^s  """
    if n<2:
        raise ValueError("n debe ser >=2")
    d = n if not n&1 else n - 1
    s = 0
    while not d&1:#mientras d sea par
        d, s = d >> 1, s + 1
    return (d,s)

def factoresPrimos(n:int) -> [int]:
    """Da los factores primos del número n ordenados de menor a mayor"""
    return sorted( descompocion_en_primos(n,repeticion=False) )

def factorizacion(n:int) -> [(int,int)]:
    """Da una lista [(pi,mi)] con pi,mi el i-esimo primo y su multiplicidad ordenada
       por el número primo de menor a mayor"""
    resul = collections.Counter( descompocion_en_primos(n,repeticion=True) )
    return sorted( resul.items(),key=lambda x:x[0] )

def factores(n:int) -> [int]:
    """Da todos los factores o divisores de n ordenados de menor a mayor

       Equibalente a: [m for m in range(1,n+1) if n%m==0]
       pero más rápido y eficiente si n es grande."""
    if n >= 0:
        if n==0:
            return []
        fun   = lambda par : tuple(itertools.accumulate(itertools.chain([1],par[1]),operator.mul))
        resul = itertools.product( *map(fun, itertools.groupby( descompocion_en_primos(n,repeticion=True) )) )
        return sorted( productoria(m) for m in resul )
    else:
        raise NoEsNumeroNatural("El objeto no representa un número natural")    

def factoresPropios(n:int) -> [int]:
    """Da todos los factores propios de n,
       osea todos sus divisores menores que el"""
    return factores(n)[:-1]




__all__ = list( x for x in dir() if not (x.startswith("_") or x in __exclude_from_all__))
del __exclude_from_all__