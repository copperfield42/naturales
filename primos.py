""" Submodulo de números primos

Ofrece variedad de pruevas de primalidad y generadores de numeros primos
"""

if __name__ == "__main__" and not __package__:
    from relative_import_helper import relative_import_helper
    __package__ = relative_import_helper(__file__,1)
    del relative_import_helper
    print("idle trick")


import itertools, math

from .natural_typing      import Iterator, Tuple
from .errores             import NoEsNumeroNatural, RequiereNumeroNaturalDesdeUno
from .generales           import productoria, isqrt, esPar, esNatural, ilen
from .aritmetica_modular  import mcd, coprimos
from ._secuencias         import mersenne


__exclude_from_all__=set(dir())

from .                   import primalidad_test, primalidad_test_otros
from .generadores_primos import primos, primos_hasta, sieve_eratosthenes, descompocion_en_primos
from .primalidad_test    import esPrimo, esPseudoprimoFuerte
from .factorizacion      import factoresPrimos



################################################################################
### ---------------------------- Números Primos --------------------------------
################################################################################


def contarPrimos(n:int) -> int:
    """Cuenta la cantidad real de primos menores que n"""
    return ilen(primos_hasta(n))



def estimar_cantidad_primos(n:int) -> Tuple[int,int]:
    """Estimado de la cantidad de primos en [0,n]
       Regresa una tupla (m,M) tal que el valor real P estara en m < P < M
       con P el valor real de la cantidad de primos.

       http://en.wikipedia.org/wiki/Prime-counting_function"""
    if n<17:#como son tan pocos, los cuento todos
        r = contarPrimos(n)
        return r-1,r+1 #para ser consistente con lo documentado
    else:
        estimado =  n/math.log(n)
        minimo = estimado
        maximo = 1.25506 * estimado
        if n >= 5393:
            minimo = n/(math.log(n) -1.0)
        if n >= 60184:
            maximo = n/(math.log(n) -1.1)
        return math.floor(minimo) , math.ceil(maximo)


def estimar_nesimo_primo(n:int) -> Tuple[int,int]:
    """Funcion que estima el valor del n-esimo primo.
       Regresa una tupla (m,M) tal que el valor real estara en m < P < M
       con P el valor real del primos."""
    if n >= 0 :
        if n<1:
            raise RequiereNumeroNaturalDesdeUno("Esta función sólo acepta números naturales mayores o iguales a 1")
        if n<=5:
            r = [2, 3, 5, 7, 11][n-1]
            return r-1,r+1
        else:
            estimado = math.log( n*math.log(n) )
            minimo = n*(estimado-1)
            maximo = n*estimado
            return math.floor(minimo) , math.ceil(maximo)
    else:
        NoEsNumeroNatural("El objeto no representa un número natural")




################################################################################
## ----------------------- Generadores de números Primos -----------------------
################################################################################


__wheels = { 30:(7,
                 frozenset({2, 3, 5}),
                 frozenset({1, 7, 11, 13, 17, 19, 23, 29}),
                 (True, False, True, True, False, True, True, False, True, False, False, True, True, False, False),
                 2
                 )
            }

def get_wheel(W:int,*,recordar:bool=True) -> Tuple[int,frozenset,frozenset,tuple,int]:
    """Regresa una tupla (M,Fact_w,Mod_w,Mask_w,step)
       Donde 'Fact_w' son los factores primos de W
       'Mod_w' son los coprimos de W
       'M' es el minimo de estos coprimos distinto de 1
       'Mask_w' es un indicador de cuales son los números desde M
       que caen en la clase Mod_w, llendo a paso 'step'
       'recordar' indica si se desea guardar en memoria esta
       Wheel para futuros uso evitando asi tener que recalcularla"""
    if W<2:
        raise ValueError("W debe se mayor que 1")
    if W in __wheels:
        return __wheels[W]
    else:
        Skip = frozenset( factoresPrimos(W) )
        MOD  = frozenset( coprimos(W) )
        M    = min( MOD-{1} )
        step = 2 if esPar(W) else 1
        MASK = tuple( n%W in MOD for n in range(M, M+W, step) )
        if recordar:
            __wheels[W] = (M,Skip,MOD,MASK,step)
        return M,Skip,MOD,MASK,step

def sieve_wheel_N_LB(L:int,B:int,W:int=30,*,recordar:bool=True) -> Iterator[int]:
    """Wheel Sieve de para encontra todos los primos en [ W*L, W*(L+B) ]
       Regresa los resultados desordenadamente"""
    #www.ams.org/journals/mcom/2004-73-246/S0025-5718-03-01501-1/S0025-5718-03-01501-1.pdf
    #algoritmo 2.1 del paper, modificado y generalizado
    #Emplea memoria proporcional a B
    if not esNatural(W) or W<2:
        raise ValueError("W debe ser un número natural mayor que 1")
    M,Skip,MOD,MASK,step = get_wheel(W,recordar=recordar)
    A = dict()
    S = L+B
    T = 1+isqrt( W*S )
    yield from ( p for p in Skip if  W*L < p < W*S )
    for d in MOD:
        A.update( zip(range(L,S),itertools.repeat(True)) )
        for q in itertools.compress(range(M,T,step),itertools.cycle(MASK)):  #range(M,T):
            for k in range(L,S):
                c = W*k + d
                if c%q == 0 and (c//q) >= q:
                    A[k]=False
        if L==0 and d==1 :
            A[0] = False
        yield from ( W*k + d for k,v in A.items() if v )


def mersenne_prime_base() -> Iterator[int] :
    """Regresa un generador con los números primos p tales que 2^p -1 es primo.
       Osea los p que producen Mersenne Primes

       Se usa el Lucas–Lehmer primality test para generar esta lista."""
    return filter(primalidad_test.__primalidad_Test_LLT,primos())


def mersenne_prime() -> Iterator[int]:
    """Generador de Mersenne Primes.
       Un Mersenne Primes son los números primos de la forma (2^p) -1
       para algun número primo p.

       Se usa el Lucas–Lehmer primality test para generar esta lista."""
    return map( mersenne, mersenne_prime_base() )
    #return ( mersenne(p) for p in mersenne_prime_base() )



def primordial(n:int) -> int :
    """Función que calcula el número primordial.
       Este número es la productoria de todos los primos
       menores o iguales que n"""
    if n >= 0 :
        return productoria(primos_hasta(n+1))
    else:
        raise NoEsNumeroNatural("El objeto no representa un número natural")


def _gcd_relation() -> Iterator[int]:
    resul = 7
    for n in itertools.count(2):
        yield resul
        resul = resul + mcd(n,resul)


def gcd_primes(unos:int=False) -> Iterator[int]:
    """en.wikipedia.org/wiki/Formula_for_primes"""
    seq = _gcd_relation()
    resul = next(seq)
    while True:
        n = next(seq)
        t = n-resul
        if unos or t!=1 :
            yield t
        resul = n

__all__ = list( x for x in dir() if not (x.startswith("_") or x in __exclude_from_all__))
del __exclude_from_all__
