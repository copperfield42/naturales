"""Sub modulo dedicado a algoritmos especialisados de factorización de numeros naturales"""

if __name__ == "__main__" and not __package__:
    from relative_import_helper import relative_import_helper
    __package__ = relative_import_helper(__file__,1)
    del relative_import_helper
    print("idle trick")

import itertools
from .natural_typing     import Tuple, Vn1, Iterator, Union
from .aritmetica_modular import jacobi_simbol, mcd
from .primos             import primos, primos_hasta

__exclude_from_all__ = set(dir())

from .secuencias         import lucas_sequence2q1 as lucas2q1
from ._secuencias        import lucas_sequence2q1n


def lucas2q1_factorial(P:int,mod:int=None,tope:int=None) -> Iterator[Vn1]:
    """Regresa un iterador con los elementos de en sucesivos factoriales
       de la secuencia de lucas de segundo tipo Vn(P,1).
       L2q1(P) -> V1!(P,1), V2!(P,1), V3!(P,1), V4!(P,1),...[, Vtope!(P,1)]"""
    seq = range(2,tope+1) if tope is not None else itertools.count(2)
    seq = itertools.chain([lucas2q1(1,P,mod)],seq)
    return itertools.accumulate(seq,lambda Vk,n:lucas_sequence2q1n(n,Vk,mod))

def william_factorization(n:int) -> Tuple[int,...]:
    """https://en.wikipedia.org/wiki/Williams%27_p_%2B_1_algorithm"""
    for A in itertools.count(3):
        lucas_A = lucas2q1(A,mod=n)
        prime = itertools.islice( primos(),1,None)
        D = A**2 -4
        for p in prime:
            if -1 == jacobi_simbol(D,p):
                break
        M=p-1


    pass

















__all__ =[ x for x in dir() if not (x.startswith("_") or x in __exclude_from_all__)]
del __exclude_from_all__
