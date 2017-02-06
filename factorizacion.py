"""
Módulo de Números Naturales, submodulo de factorizacion de numeros

"""
if __name__ == "__main__" and not __package__:
    from relative_import_helper import relative_import_helper
    __package__ = relative_import_helper(__file__,1)
    del relative_import_helper
    print("idle trick")


import itertools, operator


from .natural_typing      import Iterator, Tuple
from .errores             import NoEsNumeroNatural
from .generales           import productoria, ilen

#TO DO
# re-escribir factores en forma mas clara

__exclude_from_all__ = set(dir())

from .generadores_primos import descompocion_en_primos

def factorizacion_ds(n:int) -> Tuple[int,int]:
    """Regresa una tupla (d,s) con d impar tales que n = d*(2^s) [+1](segun n sea impar o no)

       Si n es par halla:       n  = d*2^s
       Si n es impar halla:   n -1 = d*2^s  """
    if n<2:
        raise ValueError("n debe ser >=2")
    d = n if not n&1 else (n - 1)
    s = 0
    while not d&1: #mientras d sea par
        d, s = d >> 1, s + 1
    return (d,s)

def factoresPrimos(n:int) -> Iterator[int]:
    """Regresa un generador con los factores primos del número n ordenados de menor a mayor"""
    return descompocion_en_primos(n,repeticion=False)

def factorizacion(n:int) -> Iterator[Tuple[int,int]]:
    """Regresa un generador de tuplas (pi,mi) con pi,mi el i-esimo primo y su multiplicidad
       ordenados por el número primo de menor a mayor"""
    for p, gru in itertools.groupby( descompocion_en_primos(n,repeticion=True) ):
        yield p,ilen(gru)

def factores(n:int) -> Iterator[int]:
    """Da todos los factores o divisores de n, sin orden

       Equibalente a: [m for m in range(1,n+1) if n%m==0]
       pero más rápido y eficiente si n es grande."""
    if n >= 0:
        if n==0:
            return
        if n==1:
            yield 1
            return
        fun   = lambda par : tuple(itertools.accumulate(itertools.chain([1],par[1]),operator.mul))              # type: Callable[ [Tuple[T,Iterable[int]]], Tuple[int,...] ]
        resul = itertools.product( *map(fun, itertools.groupby( descompocion_en_primos(n,repeticion=True) )) )  # type: Iterable[ Tuple[int,...] ]
        yield from ( productoria(m) for m in resul )
    else:
        raise NoEsNumeroNatural("El objeto no representa un número natural")

def factoresPropios(n:int) -> Iterator[int]:
    """Da todos los factores propios de n,
       osea todos sus divisores menores que él"""
    return filter(lambda x: x<n, factores(n) )




__all__ = [ x for x in dir() if not (x.startswith("_") or x in __exclude_from_all__) ]
del __exclude_from_all__
