""" Submodulo auxiliar del submodulo de números primos

Ofrece variedad de generadores de número primos
"""

if __name__ == "__main__" and not __package__:
    print("idle trick")
    from relative_import_helper import relative_import_helper
    __package__ = relative_import_helper(__file__,1)
    del relative_import_helper


import itertools
from .generales import isqrt
from .errores   import NoEsNumeroNatural

__exclude_from_all__=set(dir())


################################################################################
## ----------------------- Generadores de números Primos -----------------------
################################################################################

def primos():
    """Generador de todos los números primos"""
    #http://stackoverflow.com/questions/2211990/how-to-implement-an-efficient-infinite-generator-of-prime-numbers-in-python/10733621#10733621
    #postponed_sieve by Will Ness
    #usa memoria proporcional a la cantidad de primos en [0,sqrt(n)] con n el punto del calculo actual
    yield from (2,3,5,7)
    Compuestos = dict()
    ps = primos()
    p = next(ps) and next(ps) #p=3
    Marca = p**2              # =9
    for num in itertools.count(9,2):
        multiplos = None
        if num in Compuestos:
            multiplos = Compuestos.pop(num)
        elif num < Marca:
            yield num
            continue
        else: #num==Marca
            multiplos = itertools.count(Marca + 2*p,2*p)  # 15,...
            p = next(ps)  #p=5,...
            Marca = p**2  # =25,...
        for m in multiplos:
            if m not in Compuestos:
                break
        Compuestos[m] = multiplos #15,...

def primos_hasta(n:int):
    """Generador de todos los números primos menores que n"""
    #http://stackoverflow.com/questions/2211990/how-to-implement-an-efficient-infinite-generator-of-prime-numbers-in-python/10733621#10733621
    #erat3 by tzot
    #usa memoria proporcional a la cantidad de primos en [0,sqrt(n)]
    if n >= 0 :
        yield from ( p for p in (2, 3, 5) if p < n )
        MODULOS = {1, 7, 11, 13, 17, 19, 23, 29}
        MASK    = (True, False, True, True, False, True, True, False, True, False, False, True, True, False, False)
        Compuestos = dict()
        for num in itertools.compress( range(7,n,2),itertools.cycle(MASK) ):
            p = Compuestos.pop(num,None)
            if p is None:
               yield num
               sq = num**2
               if sq < n:
                   Compuestos[sq]=num
            else:
                x = num + 2*p
                while x<n and (x in Compuestos or (x%30) not in MODULOS):
                    x += 2*p
                if x<n:
                    Compuestos[x] = p
            #if verbose:print(num, len(Compuestos))
    #else:
        #raise NoEsNumeroNatural("El objeto no representa un número natural")

def sieve_eratosthenes(n:int):
    """Generador que implementa el sieve de Eratosthenes para encontrar números primos
       menores que n, siempre que n<sys.maxsize"""
    #más rapido pero a cambio de gastar mucha más memoria
    if n >= 0 :
        if n<=2:
            return
        if 2<n:
            yield 2
        resul = [True]*n
        for i in range(3,1+isqrt(n),2):
            if resul[i]:
                yield i
                for j in range( i*i ,n, i ):
                    resul[j]=False
        for j in range(i,n,2):
            if resul[j]:
                yield j
#    else:
#        raise NoEsNumeroNatural("El objeto no representa un número natural")

def descompocion_en_primos(n:int,*,repeticion=True):
    """Generador de los factores primos de n, con repetición de acuerdo a la multiplicidad
       de cada factor primo de n en caso de que asi sea solicitado, que por defecto asi es."""
    if n >= 0:
        if n<2:
            return
        primos_test = primos_hasta(n)
        while n!=1:
            p = next(primos_test)
            if n%p == 0:
                yield p
                n //= p
                while n%p == 0:
                    n //= p
                    if repeticion:
                        yield p
    else:
        raise NoEsNumeroNatural("El objeto no representa un número natural")




__all__ = list( x for x in dir() if not (x.startswith("_") or x in __exclude_from_all__))
del __exclude_from_all__