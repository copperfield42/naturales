""" Submodulo de pruebas de primalidad para determinar si un número es primo

Ofrece las principales pruevas de primalidad
"""

if __name__ == "__main__" and not __package__:
    print("idle trick")
    from relative_import_helper import relative_import_helper
    __package__ = relative_import_helper(__file__,1)
    del relative_import_helper


import collections, itertools, math#, random,
from decimal import Decimal

#from ._Naturales      import esCuadradoPerfecto

from .errores             import NoEsNumeroNatural
from .generales           import isqrt, esCuadradoPerfecto
from ._secuencias         import sucesiones_de_Lucas
from .factorizacion       import factorizacion_ds
from .aritmetica_modular  import jacobi_simbol
from .combinatoria        import triangulo_pascal
from .generadores_primos  import primos_hasta

SIEVE = 1000 #Para algunas de las pruebas de primalidad, precalcular los primos menores que este número
             #de modo de aplicar trial division con ellos
             
             
__exclude_from_all__=set(dir())



def esPrimo(n:int,**karg) -> bool:
    """Dice si un numero es primo: 2,3,5,7,11...

       Un número es primo si y sólo si es divisible exactamente por sigomismo
       y el 1(uno).

       Para esta función se elije el mejor test the primalidad que se disponga.
       Actualmente se usa el test de Baillie-PSW, ver help(primalidad_Test_PSW)
       para más detalles"""
    return primalidad_Test_PSW(n,**karg)

def __esPseudoprimoFuerte(n:int,base:int,d:int,s:int) -> bool:
    """Chequea:
       base^d = 1 (mod n)
       o
       base^( d*2^r ) = -1 (mod n) para algun 0 <= r < s """
    bd = pow(base,d,n)
    n_1 = n-1
    if bd == 1 or bd == n_1:
        return True
    for r in range(1,s):
        bd = pow(bd,2,n)
        if bd == n_1:
            return True
    return False

def esPseudoprimoFuerte(n:int,base:"int o [int]") -> bool:
    """Determina si el número es un fuerte Pseudo Primo.
       Estos son números impares que cumplen con:
       sea d y s numeros tales que n = d * 2^s +1 con d impar
       se cumple que

       base^d = 1 (mod n)
       o
       base^( d*2^r ) = -1 (mod n) para algun 0 <= r < s

       Si un número falla esta prueba con certeza es un número
       compuesto pero si la pasa solo se sabe que es candidato
       a primo en la base suministrada.

       El argumento base tambien puede ser un iterable de números
       en cuyo caso se realiza la prueba con todos ellos y se
       regresa si paso la prueba para todos ellos.

       https://en.wikipedia.org/wiki/Strong_pseudoprime"""
    if n >= 0:
        if not n&1 or n<3:
            return n==2
        if isinstance(base,collections.abc.Iterable):
            d,s = factorizacion_ds(n)
            return all(__esPseudoprimoFuerte(n,b,d,s) for b in base)
        elif base >= 0 :
            return __esPseudoprimoFuerte(n,base,*factorizacion_ds(n))
        else:
            raise NoEsNumeroNatural("El objeto no representa un número natural")
    else:
        raise NoEsNumeroNatural("El objeto no representa un número natural")



################################################################################
### ------------------------ Pruebas de Primalidad -----------------------------
################################################################################

#el mas basico de las pruebas de primalidad

def primalidad_Test_Trial_Division(n:int) -> bool:
    """Dice si un numero es primo: 2,3,5,7,11...

       Un número es primo si y sólo si es divisible exactamente por sigomismo
       y el 1(uno). Para comprobar esto se usa el método de Eratostenes con el
       criterio de Ibn-Al Banna al-Murrakushi para el calculo"""
    if n >= 0 :
        if n<2:
            return False
        elif n<4:
            return True
        elif not n&1 or n%3==0:
            return False
        else:
            mid = 1+isqrt(n)
            i=5
            while i<mid and n%i:
                i += 2
            return i>=mid
    else:
        raise NoEsNumeroNatural("El objeto no representa un número natural")


def __mr_tope(n:int) -> int:
    return math.floor( 2*math.pow(math.log(n),2)) +1

__known_primes = [] #primos_hasta(1000)

def primalidad_Test_MR(n:int,*,precision_for_huge_n:int=42,full_presicion:bool=False,verbose:bool=False) -> bool:
    """Miller–Rabin deterministic primality test. Exacto hasta 1.543e33

       Este asume como cierto Hipótesis generalizada de Riemann, la cual todavia
       no ha sido probada o falseada.
       Con estas asunción se pueden chequear numeros primos hasta al menos el 10°
       Mersenne prime, cosa que al test de divicion le tomaria toda la vida realizar.

       Los argumentos keyword-only determinan el comportamiento de la función para
       n muy grandes:
       Si n >= 1543267864443420616877677640751301 (1.543e33) entonces:
       full_presicion: de ser true se usa el sieve_eratosthenes para calcular
        los números primos hasta 2*pow(ln(n),2)))+1 y se prueba con todos ellos,
        este limite sale de la Hipótesis generalizada de Riemann que de ser
        cierto aseguraria un 100% de certesa a esta prueba.
       precision_for_huge_n: si full_presicion es falso, se usa esta cantidad de
        los primeros números primos para la cuenta. Con se esta prueba declarara
        a un número compuesto como primo con un probabilidad de
        (1/4)^k con k el valor de este argumento.
       verbose: indica cual de las modalidades anteriores esta usando.


       en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test#Deterministic_variants_of_the_test
       primes.utm.edu/prove/prove2_3.html
       http://mathworld.wolfram.com/StrongPseudoprime.html"""
    #rosettacode.org/wiki/Miller-Rabin_primality_test#Python
    if n < 0:
        raise NoEsNumeroNatural("El objeto no representa un número natural")
    if n < 2:
        return False
    if n < 4:
        return True
    if not n&1 or n%3==0:
        return False
    if not __known_primes :
        __known_primes.extend( primos_hasta(SIEVE) )
    if n in __known_primes :
        return True
    if any( (n % p) == 0 for p in __known_primes ):
        return False
    d, s = factorizacion_ds(n)
    if n < 1373653:
        return all(__esPseudoprimoFuerte(n, a, d, s) for a in (2, 3))
    if n < 9080191:
        return all(__esPseudoprimoFuerte(n, a, d, s) for a in (31, 73))
    if n < 25326001:
        return all(__esPseudoprimoFuerte(n, a, d, s) for a in (2, 3, 5))
    if n < 4759123141:
        return all(__esPseudoprimoFuerte(n, a, d, s) for a in (2, 7, 61))
    if n < 1122004669633:
        return all(__esPseudoprimoFuerte(n, a, d, s) for a in (2, 13, 23, 1662803))
    if n < 2152302898747:
        return all(__esPseudoprimoFuerte(n, a, d, s) for a in (2, 3, 5, 7, 11))
    if n < 3474749660383:
        return all(__esPseudoprimoFuerte(n, a, d, s) for a in (2, 3, 5, 7, 11, 13))
    if n < 341550071728321:
        return all(__esPseudoprimoFuerte(n, a, d, s) for a in (2, 3, 5, 7, 11, 13, 17))
    if n < 3825123056546413051:
        return all(__esPseudoprimoFuerte(n, a, d, s) for a in (2, 3, 5, 7, 11, 13, 17, 19, 23))
    if n < 318665857834031151167461:
        return all(__esPseudoprimoFuerte(n, a, d, s) for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37))
    if n < 3317044064679887385961981:
        return all(__esPseudoprimoFuerte(n, a, d, s) for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41))
    if n < 1543267864443420616877677640751301:#http://mathworld.wolfram.com/StrongPseudoprime.html
        return all(__esPseudoprimoFuerte(n, a, d, s) for a in
                       (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67))
    # otherwise
    if full_presicion:
        #asumiendo la Hipótesis generalizada de Riemann
        tope =  math.floor( 2*math.pow(math.log(n),2)) +1
        if verbose:
            print("n enorme, probando los primos en intervalo [2,%d] para el modo full_presicion"%tope)
        return all(__esPseudoprimoFuerte(n, a, d, s) for a in primos_hasta(tope))
    if verbose:
        print("n enorme, probando con los primeros",precision_for_huge_n,
              "números primos, los primos hasta", __known_primes[:precision_for_huge_n][-1])
    return all(__esPseudoprimoFuerte(n, a, d, s) for a in __known_primes[:precision_for_huge_n])


def primalidad_Test_PSW(n:int,*,verbose=False) -> bool:
    """Baillie-PSW primality test
       https://en.wikipedia.org/wiki/Baillie%E2%80%93PSW_primality_test
       https://www.youtube.com/watch?v=jbiaz_aHHUQ
       mpqs.free.fr/LucasPseudoprimes.pdf"""
    if verbose:
        print("Comprobando casos bases")
    if n < 0:
        raise NoEsNumeroNatural("El objeto no representa un número natural")
    if n < 2:
        return False
    if n < 4:
        return True
    if not n&1 or n%3==0:
        return False
    if not __known_primes :
        __known_primes.extend( primos_hasta(SIEVE) )
    if n in __known_primes :
        return True
    if any( (n % p) == 0 for p in __known_primes ):
        return False
    if esPseudoprimoFuerte(n,2):
        if verbose:
            print("Iniciando PSW")
        D = None
        for i,(x,s) in enumerate( zip(itertools.count(5,2),itertools.cycle([1,-1])) ):
            D = x*s
            J = jacobi_simbol(D,n)
            if J == -1:
                break
            elif J == 0:
                if verbose: print("Jacobi 0 con D=",D)
                return False
            if i==10:
                if verbose: print("esta tardando mucho, verificando cuadrado perfecto")
                if esCuadradoPerfecto(n):
                    return False
        P = 1
        Q = (1-D)//4
        d,s = factorizacion_ds(n+1)
        if verbose: print("P=",P,"Q=",Q,"D=",D,"d=",d,"s=",s)
        Ud,Vd,Qd = sucesiones_de_Lucas(d,P,Q,n,darQ=True)
        if Ud == 0:
            if verbose: print("condicion 1")
            return True
        if Vd == 0:
            if verbose: print("condicion 2 0")
            return True
        for r in range(1,s):
            Vd = ( Vd**2 - 2*Qd ) % n
            if Vd == 0:
                 if verbose: print("condicion 2",r)
                 return True
            Qd = pow(Qd,2,n)
        return False
    else:
        if verbose: print("No es Psudoprmo fuerte en base 2")
        return False


def __primalidad_Test_LLT(p:int) -> bool:
    """Lucas–Lehmer primality test. Determina si Mp = 2^p − 1 es primo.
       en.wikipedia.org/wiki/Lucas%E2%80%93Lehmer_primality_test"""
    if p==2:
        return True
    #para los primos impares
    mersenne = pow(2,p)-1 #M
    s = 4
    for x in range( p-2 ):
        s = pow(s,2,mersenne)-2
        #Performing the mod M at each iteration ensures
        #that all intermediate results are at most p bits
        #(otherwise the number of bits would double each iteration).
        #The same strategy is used in modular exponentiation.
    return s==0

def primalidad_Test_LLT(p:int) -> bool:
    """Lucas–Lehmer primality test. Determina si Mp = 2^p − 1 es primo.
       en.wikipedia.org/wiki/Lucas%E2%80%93Lehmer_primality_test"""
    if esPrimo(p):
        return __primalidad_Test_LLT(p)
    else:
        return False


def primalidad_Test_AKS(n:int,*,verbose=False,ies=10,progress_bar=None) -> bool:
    """
    https://en.wikipedia.org/wiki/AKS_primality_test
    https://www.youtube.com/watch?v=HvMSRWTE2mI
    http://www.cse.iitk.ac.in/users/manindra/algebra/primality_v6.pdf
    https://en.wikipedia.org/wiki/AKS_primality_test
    version binomial"""
    if n >= 0 :
        if verbose:
            print("probando casos bases",flush=True)
        if n<2:
            return False
        elif n<4:
            return True
        elif not n&1 or n%3==0:
            return False
        else:
            if verbose:
                if progress_bar:
                    print("probando fila de pascal",flush=True)
                    resul = True
                    with progress_bar( itertools.islice( triangulo_pascal(n) ,2,(n//2)+1), total=(n//2), initial=2 ) as bar:
                        for x in bar:
                            if x%n != 0:
                                resul = False
                                break
                    print(flush=True)
                    return resul
                print("probando la fila de pascal")
                for k,x in enumerate(itertools.islice( triangulo_pascal(n) ,2,(n//2)+1),2 ):
                    if x%n != 0:
                        print("falla en k=",k,"con valor=",x)
                        return False
                    elif k%ies==0:
                        print(k)
                return True
            return all( x%n == 0 for x in itertools.islice( triangulo_pascal(n) ,2,(n//2)+1) )
    else:
        raise NoEsNumeroNatural




__all__ = list( x for x in dir() if not (x.startswith("_") or x in __exclude_from_all__))
del __exclude_from_all__