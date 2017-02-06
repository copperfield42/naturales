""" Módulo de Números Naturales


Este módulo ofrece unas series de funciones que están defenidas sobre los
números Naturales (0,1,2,3,...) como lo son pruebas de primalidad y otras
clasificaciones como números perfectos, variedad de suceciones como la de
Fibonacci y Lucas, aritmetica modular incluyendo el calculo de inversa,
máximos y minimos común divisor y multiplos, factorización en números
primos y funciones que dependen de ello como la indicatris de Euler (totient) y
el radical, factoriales y números combinatorios y de Stirling, funciones
más especialisadas como la Moebius, Carmichael, Liouville.


A continuación un lista de las funciones ofrecidas por este modulo:

Funciones generales:
    isqrt
    ln
    log
    log10
    mcd
    mcd_extendido
    mcd_lista
    mcm
    mcm_lista
    nthroot
    primer_digito
    productoria

Clasificación de números:
    esAbundante
    esCiclico
    esCuadradoPerfecto
    esCullenNumber
    esDeficiente
    esExtraño
    esFermatNumber
    esFibonacciNumber
    esHappy
    esImpar
    esLibreDeCuadrados
    esMelancolico
    esMersenneNumber
    esNarcisista
    esNatural
    esPar
    esPerfecto
    esPrimo
    esProthNumber
    esSphenicNumber
    esThabitNumber
    esUnaPotencia
    esVampiro
    sonCoprimos
    sonGemelos
    sonPrimosN

Aritmetica modular:
    mod_eq
    mod_exp
    mod_inv
    mod_mul
    mod_res
    mod_sum
    carmichael_funtion
    discrete_log
    esPrimitiveRoot
    multiplicative_order
    raicesPrimitivas

Pruebas de primalidad:
    esPseudoprimoFuerte
    primalidad_Test_AKS
    primalidad_Test_AKS_inocente
    primalidad_Test_Fermat
    primalidad_Test_LLT
    primalidad_Test_MR
    primalidad_Test_PSW
    primalidad_Test_Pepin
    primalidad_Test_Proth
    primalidad_Test_Trial_Division
    primalidad_Test_Wilson

RequiereNumeroNaturalDesdeUno("Esta función sólo acepta números naturales mayores o iguales a 1")
NoEsNumeroNatural("El objeto no representa un número natural")
MAX_PREC
Matrix2x2
NaturalError
NumeroFactorizado
Vector2
bell
carmichael
cdebil
cfuerte
combinatorio
combinatorioMulticonjunto
contarPrimos
contruirNumeroCiclico
coprimos
cullen_number
descompocion_en_primos
esLucasProbablePrime
esLucasPseudoprimo
esLucasPseudoprimoExtraFuerte
esLucasPseudoprimoFuerte
esLucasPseudoprimoFuerteP
estimar_cantidad_primos
estimar_nesimo_primo
factores
factoresPrimos
factoresPropios
factorial
factorialAscendente
factorialDescendente
factorizacion
factorizacion_ds
factorizacion_fermat_number
fermat_number
fermat_test
fibonacci
fila_pascal
gcd_primes
jacobi_simbol
jacobsthal_lucas_number
jacobsthal_number
legendre_simbol
leylan
liouville_function
lucas
mersenne
mersenne_prime
mersenne_prime_base
mertens_function
moebius
naturales
numeros_2_e_impar
pell_number
perfectos
pitagorian_triple
primer_primo
primordial
primos
pseudoFibo
pseudoFiboForever
quality
radical
sieve_eratosthenes
smallPsPF
stirling
sucesion_de_Lucas_Generalizada
sucesion_de_Lucas_Generalizada_n
sucesion_de_lucas_primer_tipo
sucesion_de_lucas_segundo_tipo
sucesion_de_lucas_segundo_tipo_Q1
sucesiones_de_Lucas
thabit
wilson_number
indicatriz,totient,euler




"""

version=9
################################################################################
# version 4:
# -esPrimo es mas efeciente chequeando solo numero impares y descartando casos triviales
# -como resultado el calculo de números perfectos que en la version 3 que era rápido solo 7,
#  ahora es rapido hasta 8
# -factores mucho más efeciente y rapido con el uso de itertools
#
# version 5:
# -factorizacion más eficiente abandonando los itertools por una implementacion más simple
#  y más eficiente
#
# version 6:
# -esPrimo regresa a ser puramente booleano y la parte que regresaba un numero se separo
#  en la funcion primer_primo
#
# version 7:
# -Añadido el Lucas–Lehmer primality test, que permite una rapida identificación de
#  Mersenne Primes, con lo cual el calculo de numeros perfectos se aumenta hasta 15
#  en un tiempo rasonable.
# -Añadido Miller–Rabin primality test. Exacto hasta 3.317e23
#
# version 8:
# -Añadidas secuencias de Lucas de primera y segunda especie con calculo en modulo N
#  para su uso en pruebas de primalidad, y redefinidas otras secuencias en base a estas
#  para los casos que aplica como los números de Fibonnaci y Lucas
# -Miller–Rabin primality test. Exacto hasta 1.543e33
#
# version 9:
# -agregada funcion para calcular raices enesimas, logaritmos
# -Añadido PSW primality test.
# -Añadida una limitada interface de linea de comando
#
#
################################################################################

import numbers, random, collections, itertools, math#, sys as _sys #, decimal
from functools import reduce, total_ordering
from decimal import Decimal, localcontext, Context #,MAX_PREC
#mis modulos
import itertools_recipes
#from compare import Compare

__exclude_from_all__=set(dir())


class NaturalError(ValueError):
    """Error del modulo de números naturales"""
    pass

class NoEsNumeroNatural(NaturalError):
    """El objeto no representa un número natural"""
    pass

class RequiereNumeroNaturalDesdeUno(NaturalError):
    """Esta función sólo acepta números naturales mayores o iguales a 1"""
    pass



SIEVE = 1000 #Para algunas de las pruebas de primalidad, precalcular los primos menores que este número
             #de modo de aplicar trial division con ellos

#-----------------------------------

def esNatural(n) -> bool:
    """Dice si el objeto representa a un número Natural: 0,1,2,3... """
    return isinstance(n,numbers.Integral) and n>=0


def naturales(*,start=0,stop=None,step=1):
    """Seceuncia de los números naturales, desde start hasta stop-1 con paso step.
       Si stop es omitido es una secuencia infinita.
       Los argumentos son keyword-only."""
    if esNatural(start) and esNatural(step):
        if stop is not None:
            if esNatural(stop):
                return range(start,stop,step)
            else:
                raise NoEsNumeroNatural("El objeto no representa un número natural")
        else:
            return itertools.count(start,step)
    else:
        raise NoEsNumeroNatural("El objeto no representa un número natural")



def mod_eq(a,b,n):
    """comprueba si a==b(mod n) que se lee "a es congruente con b modulo n" """
    return a%n == b%n

def mod_exp(x,n,m):
    """Calcula (x^n) mod m
       alias de pow"""
    return pow(x,n,m)

def mod_mul(a,b,n):
    """calcula (a*b) mod n"""
    return ((a%n)*(b%n))%n

def mod_sum(a,b,n):
    """calcula (a+b) mod n"""
    return ((a%n)+(b%n))%n

def mod_res(a,b,n):
    """calcula (a-b) mod n"""
    return ((a%n)-(b%n))%n

def mod_inv(a,n) -> "a**(-1) mod n":
    """Halla la inversa de a modulo n.
       Esto es el número x tal que
       a*x = 1 (mod n)
       entonces x= a**(-1)"""
    gcd,x,y = mcd_extendido( a if a>=0 else a%n , n)
    if gcd == 1:
        return x%n
    else:
        raise ZeroDivisionError("{} no es invertible modulo {}".format(a,n))

def esPar(n:int) -> bool:
    return not n&1

def esImpar(n:int) -> bool:
    return not esPar(n)

#def take(n, iterable) -> list:
#    "Return first n items of the iterable as a list"
#    return list(itertools.islice(iterable, n))

def productoria(iterable,start=1) -> "value":
    """Productoria sobre los elementos del iterable.

       Regresa el acumulado de la multiplicación de un iterable de números
       (o cualquier objeto que defina __mul__ ) de izquierda a derecha
       empesando por start que posee valor por defecto de 1.
       Por ejemplo,  productoria( [1, 2, 3, 4, 5] ) calcula (((((start*1)*2)*3)*4)*5)
       Si el iterable esta vacio, regresa start"""
    return reduce(lambda x,y: x*y, iterable, start)

def isqrt(n:int) -> int:
    """Raiz cuadrada entera de n.
       Equivalente a round(math.sqrt(n))
       pero calculada sin el uso de aritmetica punto flotante"""
    #Se usa el método de Newton.
    #https://en.wikipedia.org/wiki/Integer_square_root
    #https://gist.github.com/bnlucas/5879594
    if n>=0:
        if n == 0:
            return 0
        a, b = divmod(n.bit_length(), 2)
        x = 2 ** (a + b)
        while True:
            y = (x + n // x) >> 1
            if y >= x:
                return x
            x = y
    else:
        raise NoEsNumeroNatural("El objeto no representa un número natural")

def nthroot(n:int, A,*, precision=None,decimales=None) -> Decimal:
    """Calcula la raiz n-esima de A"""
    #https://en.wikipedia.org/wiki/Nth_root#Logarithmic_computation
    if n>1:
        if A>0:
            DA = Decimal(A)
            #N = Decimal(n)
            if not precision:
                dec = 21 + (decimales if decimales else 0)
                precision = max( 42+dec, ((abs(DA.adjusted())+1)//n ) + dec )
                #21 y 42 números arbitrarios para minimizar
                #errores de redondeo y entregar un numero
                #con precicion más que suficiente para lo
                #que se necesite. Se eligio 42 ya que es la
                #respuesta al universo, y 21 por se la mitad
                #de la respuesta
            with localcontext() as ctx:
                ctx.prec = precision
                resul = Decimal( DA.ln() / n ).exp()
                return resul if decimales is None else round(resul,decimales)
        elif A==0:
            return Decimal(0)
        else:
            if n%2==0:
                raise ValueError("Raiz par de un número negativo")
            return - nthroot(n, -A, precision=precision,decimales=decimales)
    else:
        raise ValueError("El indice de la raiz debe ser mayor que 1")

def digital_root(n:int,base=10) -> int:
    """https://en.wikipedia.org/wiki/Digital_root"""
    if not (esNatural(base) and base>=2):
        raise ValueError("LA base debe ser mayor o igual a 2")
    if esNatural(n):
        if n==0:
            return 0
        return 1 + ((n-1)%(base-1))
    else:
        raise NoEsNumeroNatural("El objeto no representa un número natural")

def ln(n,*,context=None) -> Decimal:
    """Logaritmo natural de n.
       logaritmo en base e = 2.718281828459045235360287471..."""
    return Decimal(n).ln(context)

def log10(n,*,context=None) -> Decimal:
    """Logaritmo en base 10 de n"""
    return Decimal(n).log10(context)

def log(b,n,*,context=None) -> Decimal:
    """Logaritmo en base b de n"""
    return Decimal(n).ln(context) / Decimal(b).ln(context)





################################################################################
### ------------------------ Pruebas de Primalidad -----------------------------
################################################################################


##def numeros_2_e_impar(stop:int=None):
##    """Generador de los números [2,3,5,...,stop-1]
##       genera los números 2 y todos los impares desde 3 hasta stop-1"""
##    if stop is not None:
##        if stop>2:
##            return itertools.chain([2],range(3,stop,2))
##        else:
##            return []
##    else:
##        return itertools.chain([2],itertools.count(3,2))



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


def _esLucasProbablePrime(n:int,P:int,Q:int) -> bool:
    raise NotImplementedError()
    if P>0 and esImpar(n):
        D = P*P -4*Q
        index = n - jacobi_simbol(D,n)
        return sucesion_de_lucas_primer_tipo(index,P,Q,n) == 0
    else:
        raise ValueError()


def _esLucasPseudoprimo(n:int,P:int,Q:int) -> bool:
    raise NotImplementedError()
    if P>0 and esImpar(n):
        D = P*P -4*Q
        if jacobi_simbol(D,n) == -1:
            return sucesion_de_lucas_primer_tipo(n+1,P,Q,n) == 0
        return False
    else:
        raise ValueError()


def _esLucasPseudoprimoFuerte(n:int,P:int,Q:int) -> bool:
    raise NotImplementedError()
    if P>0 :
        if esImpar(n):
            D = P*P -4*Q
            if sonCoprimos(n,D):
                index = n - jacobi_simbol(D,n)
                d,s = factorizacion_ds(index)
                if sucesion_de_lucas_primer_tipo(d,P,Q,n) == 0:
                    return True
                for r in range(s):
                    if sucesion_de_lucas_segundo_tipo(d*(2**r),P,Q,n) == 0:
                        return True
                return False
            return False
        else:
            return False
    else:
        raise ValueError()

def _esLucasPseudoprimoFuerteP(n:int,*,verbose=False) -> bool:
    """Dice si el número es un Pseudo Primo Fuerte de Lucas para alguna base P.
       Estos son los números tales que:
       Sea d,s números tales que d*2^s = n+1 y sean Q=1 y
       P perteneciente a [1,2,3,4,5,6...] tal que con D = P^2 -4Q
       el simbolo de Jacobi es (D/n)==-1 cumplen alguna de las
       siquientes ondiciones:

       Ud(P,Q) = 0 (mod n) y Vd(P,Q) =+-2 (mod n)
       o
       V(d*2^r)(P,Q) = 0 (mod n) para algun 0 <= r < s-1


       en.wikipedia.org/wiki/Lucas_pseudoprime#Strong_Lucas_pseudoprimes"""
    raise NotImplementedError()
    if n>=0:
        if n<2:
            return False
        if n<4:
            return True
        if not n&1 or n%3==0 or esCuadradoPerfecto(n):
            return False
        pass
        return False
    else:
        raise NoEsNumeroNatural("El objeto no representa un número natural")

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



def primalidad_Test_Wilson(n:int) -> bool:
    """(n-1)! = -1 (mod n)
       https://en.wikipedia.org/wiki/Wilson%27s_theorem"""
    if n>=0:
        if n>1:
            return factorial(n-1,n) == n-1
        return False
    else:
        raise NoEsNumeroNatural("El objeto no representa un número natural")




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

def primalidad_Test_AKS(n:int,*,verbose:bool=False) -> bool:
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
##  if n < 118670087467:
##        if n == 3215031751:
##            return False
##        return all(__esPseudoprimoFuerte(n, a, d, s) for a in (2, 3, 5, 7))
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
##    if n < 2**64:
##        return all(__esPseudoprimoFuerte(n, a, d, s) for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37))
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

def __primalidad_Test_LLT(p:int) -> bool:
    """Lucas–Lehmer primality test. Determina si Mp = 2^p − 1 es primo.
       en.wikipedia.org/wiki/Lucas%E2%80%93Lehmer_primality_test"""
    if p==2:
        return True
    #para los primos impares
    mersenne = (2**p)-1 #M
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



################################################################################
### ---------------------------- Números Primos --------------------------------
################################################################################


def esPrimo(n:int,**karg) -> bool:
    """Dice si un numero es primo: 2,3,5,7,11...

       Un número es primo si y sólo si es divisible exactamente por sigomismo
       y el 1(uno).

       Para esta función se elije el mejor test the primalidad que se disponga.
       Actualmente se usa el test de Baillie-PSW, ver help(primalidad_Test_PSW)
       para más detalles"""
    if isinstance(n,NumeroFactorizado):
        return n.esPrimo()
    return primalidad_Test_PSW(n,**karg)


def contarPrimos(n) -> int:
    """Cuenta la cantidad real de primos menores que n"""
    resul = 0
    for resul,p in enumerate( primos_hasta(n),1): pass
    return resul


def estimar_cantidad_primos(n:int) -> (int,int):
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


def estimar_nesimo_primo(n:int) -> (int,int):
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


def sonGemelos(a:int,b:int) -> bool:
    """Dice si dos números son primos gemelos
       Un número es Gemelo si ambos son primos
       y uno es 2 unidades menor o mayor que el otro"""
    return (a==b+2 or a==b-2) and esPrimo(a) and esPrimo(b)


def sonPrimosN(a:int,b:int,n:int=2):
    """Dice si a y b estan separados n unidades y son primos ambos"""
    return (a==b+n or a==b-n) and esPrimo(a) and esPrimo(b)

################################################################################
## ----------------------- Generadores de números Primos -----------------------
################################################################################


def sieve_eratosthenes(n:int):
    """Generador que implementa el sieve de Eratosthenes para encontrar números primos
       menores que n, siempre que n<sys.maxsize"""
    #más rapido pero a cambio de gastar mucha más memoria
    if n >= 0 :
        if n<=2:
            return
            #raise StopIteration()
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
    else:
        raise NoEsNumeroNatural("El objeto no representa un número natural")


__wheels = { 30:(7,
                 frozenset({2, 3, 5}),
                 frozenset({1, 7, 11, 13, 17, 19, 23, 29}),
                 (True, False, True, True, False, True, True, False, True, False, False, True, True, False, False),
                 2
                 )
             }
def get_wheel(W:int,*,recordar=True) -> (int,frozenset,frozenset,tuple,int):
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

def sieve_wheel_N_LB(L,B,W=30,*,recordar=True):
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

#def _soe(n):
#    return _ilen( sieve_eratosthenes(n) )
#
#def _swn(n,w=30):
#    return _ilen( sieve_wheel_N_LB(0,n,w) )

def primos_hasta(n:int,*,W=30,verbose=False):
    """Generador de todos los números primos menores que n"""
    #http://stackoverflow.com/questions/2211990/how-to-implement-an-efficient-infinite-generator-of-prime-numbers-in-python/10733621#10733621
    #erat3 by tzot
    #usa memoria proporcional a la cantidad de primos en [0,sqrt(n)]
    if n >= 0 :
        M,Skip,MODULOS,MASK,step = get_wheel(W)
        yield from ( p for p in Skip if p < n )
        Compuestos = dict()
        for num in itertools.compress( range(M,n,step),itertools.cycle(MASK) ):
            p = Compuestos.pop(num,None)
            if p is None:
               yield num
               sq = num**2
               if sq < n:
                   Compuestos[sq]=num
            else:
                x = num + 2*p
                while x<n and (x in Compuestos or (x%W) not in MODULOS):
                    x += 2*p
                if x<n:
                    Compuestos[x] = p
            if verbose:print(num, len(Compuestos))
    else:
        raise NoEsNumeroNatural("El objeto no representa un número natural")


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


#def _pn(n):
#    return _ilen(primos_hasta(n))
#def _p(n):
#    return _ilen( itertools.islice(primos(),n) )



def mersenne_prime():
    """Generador de Mersenne Primes.
       Un Mersenne Primes son los números primos de la forma (2^p) -1
       para algun número primo p.

       Se usa el Lucas–Lehmer primality test para generar esta lista."""
    return ( mersenne(p) for p in filter(__primalidad_Test_LLT,primos()) )


def mersenne_prime_base():
    """Regresa una lista con los números primos p tales que 2^p -1 es primo.
       Osea los p que producen Mersenne Primes

       Se usa el Lucas–Lehmer primality test para generar esta lista."""
    return filter(__primalidad_Test_LLT,primos())


def primordial(n):
    """Función que calcula el número primordial.
       Este número es la productoria de todos los primos
       menores o iguales que n"""
    if n >= 0 :
        return productoria(primos_hasta(n+1))
    else:
        raise NoEsNumeroNatural("El objeto no representa un número natural")


def _gcd_relation():
    resul = 7
    for n in itertools.count(2):
        yield resul
        resul = resul + mcd(n,resul)


def gcd_primes(unos:int=False):
    """en.wikipedia.org/wiki/Formula_for_primes"""
    seq = _gcd_relation()
    resul = next(seq)
    while True:
        n = next(seq)
        t = n-resul
        if unos or t!=1 :
            yield t
        resul = n

################################################################################
### --------------------------- Factorizacion ----------------------------------
################################################################################


def primer_primo(n:int) -> int:
    """Regresa el primer número primo que divida exactamente
       al número n, que de ser primo sera él mismo."""
    if n >= 0:
        if n<2:
            raise ValueError("No exite número primo menor que "+str(n))
        elif not n&1: #si es par
            return 2
        elif esPrimo(n):
            return n
        else:
            mid = 1+isqrt(n)
            i = 3
            while(i<mid and not n%i==0):
                i += 2
            if i >= mid:
                return n
            else:
                return i
    else:
        raise NoEsNumeroNatural("El objeto no representa un número natural")

def descompocion_en_primos(n:int,*,repeticion=True):
    """Generador de los factores primos de n, con repetición de acuerdo a la multiplicidad
       de cada factor primo de n en caso de que asi sea solicitado"""
    if isinstance(n,NumeroFactorizado):
        yield from n.descompocion_en_primos(repeticion)
        return
        #raise StopIteration
    if n >= 0:
        if n<2:
            return
            #raise StopIteration
        if esPar(n):
            n,s = factorizacion_ds(n)
            if repeticion:
                yield from ( 2 for _ in range(s) )
            else:
                yield 2
        if esPrimo(n):
            yield n
            return
            #raise StopIteration
        primos_test = primos_hasta(n)
        while n!=1:
            p = next(primos_test)
            if n%p==0:
                yield p
                n //= p
                while n%p == 0:
                    n //= p
                    if repeticion:
                        yield p
                if esPrimo(n):
                    yield n
                    return 
                    #raise StopIteration
    else:
        raise NoEsNumeroNatural("El objeto no representa un número natural")

def descompocion_en_primos_sieve(n,*,repeticion=True,verbose=False,buffer=1000,W=30):
    if isinstance(n,NumeroFactorizado):
        yield from n.descompocion_en_primos(repeticion)
        return
        #raise StopIteration
    if n >= 0:
        if n<2:
            return
            #raise StopIteration
        if esPar(n):
            n,s = factorizacion_ds(n)
            if repeticion:
                yield from ( 2 for x in range(s) )
            else:
                yield 2
        if esPrimo(n):
            yield n
            return 
            #raise StopIteration
        cota = 0
        if verbose:
            i=0
        while n!=1:
            if verbose:
                print("ciclo",i,"rango de busqueda",W*cota,W*(cota+buffer) )
                i += 1
            for p in sieve_wheel_N_LB(cota,buffer,W):
                if n%p == 0:
                    if verbose: print("encontrado factor",p)
                    yield p
                    n //= p
                    while n%p == 0:
                        n //= p
                        if repeticion:
                            yield p
                    if esPrimo(n):
                        if verbose: print("el remanente es primo",n)
                        yield n
                        return
                        #raise StopIteration
            cota += buffer
    else:
        raise NoEsNumeroNatural("El objeto no representa un número natural")

def __si(n):
    n = isqrt(n)
    cota = 1
    for i in itertools.count(1):
        if 30*(cota-1) <= n <= 30*(2*cota-1):
            return i,cota
        cota *= 2

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
        fun   = lambda par : list(itertools_recipes.acumulado(lambda x,y:x*y,par[1],1))
        resul = itertools.product( *map(fun, itertools.groupby( descompocion_en_primos(n,repeticion=True) )) )
        return sorted( productoria(m) for m in resul )
    else:
        raise NoEsNumeroNatural("El objeto no representa un número natural")    


#factor=factores #por posible retrocompativilidad con alguno de mis otros modulos


def factoresPropios(n:int) -> [int]:
    """Da todos los factores propios de n,
       osea todos sus divisores menores que el"""
    return factores(n)[:-1]


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
# ------------------------------- MCD y mcm ------------------------------------
################################################################################

def mcd(a:int,b:int) -> int:
    """Máximo Común Divisor de a y b
       Se usa el algoritmo de Euclides"""
    while b:
        a,b = b , a%b
    return a


def mcd_extendido(a,b) -> "(mcd,x,y)":
    """Regresa una tupla tal que mcd(a,b) = a*x + b*y"""
    #https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm"""
    x, u = 0, 1
    y, v = 1, 0
    while a:
        q,r = divmod(b,a)
        x,u = u, x-u*q
        y,v = v, y-v*q
        b,a = a,r
    return b,x,y


def mcm(a:int,b:int) -> int:
    """Minimo Común Multiplo de a y b
       Se usa redución por el máximo común divisor"""
    if a==0 or b==0:
        return 0
    else:
        return (a*b)//mcd(a,b)

def sonCoprimos(a:int,b:int) -> bool:
    """Dice si dos números son coprimos.
       Dos números son coprimos si su máximo
       común divisor es 1 """
    return mcd(a,b)==1

def coprimos(n:int):
    """Regresa un generador con los coprimos de n en el intervalo [1,n]"""
    if n >= 0 :
        return ( c for c in range(1,n+1) if mcd(c,n)==1 )
    else:
        raise NoEsNumeroNatural("El objeto no representa un número natural")

def mcm_lista(iterable) -> int:
    """Calcula el máximo común multiplo de un iterable de números."""
    return reduce(lambda x,y:mcm(x,y),iterable)

def mcd_lista(iterable) -> int:
    """Calcula el minimo común divisor de un iterable de números."""
    return reduce(lambda x,y:mcd(x,y),iterable)



################################################################################
### ----------------------- Funciones sobre los naturales ----------------------
################################################################################


def indicatriz(n:int,*,modo=2) -> int:
    """Función indicatriz de Euler. Cuenta cuantos coprimos
       tiene el número n en el intervalo [1,n]

       También conocida como Euler's totient function

       modos:
       1)contar los coprimos de n
       2)usar los factores primos de n y aplicar la formula de Euler

       https://en.wikipedia.org/wiki/Euler%27s_totient_function"""
    if isinstance(n,NumeroFactorizado):
        return n.indicatriz()
    if modo==1:
        resul = 0
        for x in coprimos(n):
            resul += 1
        return resul
    elif modo==2:
        resul = n * productoria( map(lambda p: 1-(1/p),descompocion_en_primos(n,repeticion=False )) )
        return round(resul)
    else:
        raise ValueError("modo invalido")

totient = indicatriz
euler   = indicatriz

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

def __multiplicative_order(a,n) -> int:
    temp = 1
    resul = 1%n
    for k in itertools.count(1):
        temp = (temp*a)%n
        if temp==resul:
            return k

def multiplicative_order(a:int,n:int) -> int:
    """Orden multiplicativo de a modulo n.
       Si a y n son números coprimos, el orden multiplicativo de a modulo n
       es el número k>=1 más pequño tal que:

       a^k = 1 (mod n)
       https://en.wikipedia.org/wiki/Multiplicative_order"""
    if n>0:
        if sonCoprimos(a,n):
            return __multiplicative_order(a,n)
        else:
            raise ValueError("a y n deben ser coprimos")
    else:
        raise RequiereNumeroNaturalDesdeUno("Esta función sólo acepta números naturales mayores o iguales a 1")

def esPrimitiveRoot(a:int,n:int) -> bool:
    """Dice si a es una raiz primitiva de n.
       El número a es raiz primitiva de n si
       ambos son coprimos, y el orden multiplicativo
       de a es igual a la indicatriz de n
       http://mathworld.wolfram.com/PrimitiveRoot.html"""
    if a<=n :
        try:
            return multiplicative_order(a,n) == indicatriz(n)
        except:
            pass
    return False

def raicesPrimitivas(n:int) -> [int]:
    """Da una lista con las raices primitivas de n si tiene alguna.
       https://en.wikipedia.org/wiki/Primitive_root_modulo_n"""
    if n>=0:
        if n==1:
            return [0]
        resul = list()
        ind = 0
        for a in coprimos(n):
            ind += 1
            resul.append( (a,__multiplicative_order(a,n)) )
        return list(map(lambda x:x[0],filter(lambda y:y[1]==ind,resul)))
    else:
        raise NoEsNumeroNatural("El objeto no representa un número natural")


def discrete_log(a,g,n):
    """log_g(a) (mod n)
       http://mathworld.wolfram.com/DiscreteLogarithm.html
       https://en.wikipedia.org/wiki/Discrete_logarithm"""
    if sonCoprimos(a,n) and esPrimitiveRoot(g,n):
        for r in range(1,indicatriz(n)):
            if a%n == pow(g,r,n):
                return r
    raise ValueError()



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
        raise NaturalError("Error fatal: la función de moebius dio un resultado diferente de -1, 0 ó 1")
    if verbose:
        print("Se encontro que el número",n,"",end="")
        if m==1 or m==-1:
            print("es libre de cuadrados y tiene un número", "par" if m==1 else "impar" ,
                  "de factores primos distintos")
        elif m==0:
            print("es divisible por algun cuadrado")
    return m


def __jacobi_simbol(a:int,n:int) -> "-1,0,1":
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


def jacobi_simbol(a:int,n:int) -> "-1,0,1":
    """Símbolo de Jacobi.
       en.wikipedia.org/wiki/Jacobi_symbol"""
    #version que verifica las precondiciones
    if n >= 0 :
        if n&1:#si n es impar
            return __jacobi_simbol(a,n)
        else:
            raise NaturalError("n debe ser impar")
    else:
        raise NaturalError("El parametro n debe ser un número natural")


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
### --------------------- Clasificaciones de números Naturales -----------------
################################################################################


def esPerfecto(n:int) -> bool:
    """Dice si un número es perfecto.
       Un número es perfecto si la suma de todos sus factores
       propios es igual a él"""
    if n >= 0:
        return n==sum(factoresPropios(n)) if n>0 else False
    else:
        raise NoEsNumeroNatural("El objeto no representa un número natural")


def esAbundante(n) -> bool:
    """Dice si un número es Abundante.
       Un número es Abundante si la suma de sus factores propios
       es mayor que él"""
    if n >= 0 :
        if n>0:
            return n<sum(factoresPropios(n))
        else:
            raise RequiereNumeroNaturalDesdeUno("Esta función sólo acepta números naturales mayores o iguales a 1")
    else:
        raise NoEsNumeroNatural("El objeto no representa un número natural")


def esDeficiente(n) -> bool:
    """Dice si un número es Deficiente.
       Un número es Deficiente si la suma de sus factores propios
       es menor que él"""
    if n >= 0 :
        if n>0:
            return n>sum(factoresPropios(n))
        else:
            raise RequiereNumeroNaturalDesdeUno("Esta función sólo acepta números naturales mayores o iguales a 1")
    else:
        raise NoEsNumeroNatural("El objeto no representa un número natural")



def esCuadradoPerfecto(n:int) -> bool:
    """Dice si un número es un cuadrado perfecto.
       N es cuadrado perfecto si existe un natural M tal que M^2==N"""
    return n == isqrt(n)**2

def esLibreDeCuadrados(n:int) -> bool:
    """Dice si el número n es libre de cuadrados.
       Esto es si el número No es divisible por algun cuadrado perfecto
       menor que n diferente de 1."""
    if n>0:
        cp = 1
        for k in range(2, 1+ isqrt(n) ):
            cp += 2*k - 1
            if n % cp == 0:
                return False
        return True
    return False



def esNarcisista(n:int) -> bool:
    """Dice si un número es narcisista.
       N es narcisista si la suma cada digito en el número elevado a
       la cantidad de digitos del mismo es igual a N."""
    if esNatural(n):
        num = str(n)
        tam = len(num)
        return n == sum(map(lambda x: int(x)**tam,num))
    else:
        raise NoEsNumeroNatural("El objeto no representa un número natural")

def esPerfectDigitalInvariant(n:int,e:int) -> bool:
    """Dice si un número es Perfect Digital Invariant (PDI).
       N es PDI si la suma cada digito en el número elevado a
       la e es igual a N."""
    if esNatural(n):
        return n == sum(map(lambda x: int(x)**e,str(n)))
    else:
        raise NoEsNumeroNatural("El objeto no representa un número natural")


def esCiclico(n:int,*,base:int=10) -> bool:
    """Dice si el número es ciclico en la base espesificada.
       www.youtube.com/watch?v=WUlaUalgxqI
       en.wikipedia.org/wiki/Cyclic_number"""
    if not esNatural(n):
        raise NoEsNumeroNatural("El objeto no representa un número natural")
    long = len(str(n))
    if n *(long+1) == int("9"*long):
        try:
            return n == contruirNumeroCiclico(long+1,base)
        except:
            pass
    long+=1
    if n *(long+1) == int("9"*long):
        try:
            return n == contruirNumeroCiclico(long+1,base)
        except:
            pass
    return False


def esHappy(n:int,*,e:int=2,verbose:bool=False) -> bool:
    """Dice si el número es Feliz con exponente e
       www.youtube.com/watch?v=kC6YObu61_w
       www.youtube.com/watch?v=_DpzAvb3Vk4"""
    if not esNatural(n):
        raise NoEsNumeroNatural("El objeto no representa un número natural")
    recuerdo = set()
    if verbose:
            print(n)
    while True:
        n = sum( x**e for x in map(lambda y:int(y),str(n))  )
        if verbose:
            print(n)
        if n == 1:
            return True
        if n in recuerdo:
            return False
        else:
            recuerdo.add(n)


def esMelancolico(n:int,*,e:int=2,verbose=False) -> bool:
    return not esHappy(n,e,verbose)


def esVampiro(n:int,*,valor:bool=False) -> bool:
    """Dice si un número es un vampiro.
       www.youtube.com/watch?v=3ZMnVd4ivKQ
       en.wikipedia.org/wiki/Vampire_number"""
    if n<1000:
        return False
    nstr = str(n)
    if len(nstr)%2==0:
        factor_len = len(nstr) // 2
        temp1 = ( x for x in factores(n) if factor_len==len(str(x)) )
        temp2 = ( c for c in itertools.combinations(temp1,2)
                  if n == productoria( c ) #reduce(lambda x,y:x*y,c,1)
                  and 1 >= sum(map(lambda z:str(z).endswith("0"),c)) )
        nstr = sorted(nstr)
        temp3 = list( c for c in temp2 if nstr == sorted( "".join(map(str,c)) ) )
        return temp3 if valor else bool(temp3)
    else:
        return False

def esExtraño(n:int) -> int:
    """Dice si un número es extraño.
       Los números extraños son números abundantes, tales
       que ningun subconjuto de los divisores propios de n
       sume igual a n

       https://en.wikipedia.org/wiki/Weird_number"""
    fact = factoresPropios(n)
    if n<sum(fact):
        return not any( n == sum(sub) for sub in itertools_recipes.powerset(fact) )
    else:
        return False

def esProthNumber(n:int,*,valor:bool=False) -> bool:
    """Dice si es un número de Proth.
       Estos son los números de la forma:
       k*2^m +1 donde k es impar y 0<k<2^m

       en.wikipedia.org/wiki/Proth_number"""
    if n&1 and n>1:
        k,m = factorizacion_ds(n)
        if k<2**m:
            return (k,m) if valor else True
    return None if valor else False

def esCullenNumber(n:int,*,valor:bool=False) -> bool:
    """Dice si es número de Cullen.
       Estos son los números de la forma:
       m*2^m +1  para algun m natural

       en.wikipedia.org/wiki/Cullen_number"""
    if esImpar(n):
        d,s = factorizacion_ds(n)
        if valor:
            return d if d==s else None
        return d==s
    else:
        return None if valor else False

def esFermatNumber(n:int,*,valor:bool=False) -> bool:
    """Dice si es un número de Fermat.
       Estos son los números de la forma
       2^(2^m) +1 para algun m natural.

       Si 'valor' es cierto entonces si
       cumple la condición regresa el m
       si sino regresa None"""
    if n>2 and esImpar(n):
        d,s = factorizacion_ds(n)
        if d==1 and s>0:
            if s in [1,2]: #m=0,1
                if valor:
                    return 0 if s==1 else 1
                else:
                    return True
            else:
                if esPar(s):
                    dd,m = factorizacion_ds(s)
                    if dd==1 and m>1:
                        return m if valor else True
    return None if valor else False

def esMersenneNumber(n:int,*,valor:bool=False) -> bool:
    """Dice si es un número de Mersenne.
       Eston son los números de la forma 2^m -1 """
    if n==0:
        return 0 if valor else True
    if n>=1:
        if esImpar(n):
            d,s = factorizacion_ds(n+1)
            if d==1:
                return s if valor else True
    return None if valor else False

def esSphenicNumber(n:int,*,valor:bool=False) -> bool:
    """Dice si es un número de Sphenic.
       Estos son los números tales que tienen exactamente 3 factores primos distintos
       con multiplicidad 1 cada uno.
       https://en.wikipedia.org/wiki/Sphenic_number"""
    facto = factorizacion(n)
    if len(facto)==3:
        if all( m==1 for p,m in facto):
            return list( p for p,m in facto) if valor else True
    return None if valor else False

__golden_ratio = Decimal("1.61803398874989484820458683436563811772030917980576286213544862270526046281890244970720720418939113748475")
#https://oeis.org/A001622

def esFibonacciNumber(n:int,*,valor=False) -> bool:
    """Dice si n es número de la secuencia de Fibbocci."""
    #en.wikipedia.org/wiki/Fibonacci_number#Recognizing_Fibonacci_numbers
    temp = 5*(n**2)
    if valor:
        sig = None
        if esCuadradoPerfecto( temp +4 ):
            sig =  1
        elif esCuadradoPerfecto( temp -4 ):
            sig = -1
        if sig:
            return round(log(__golden_ratio, (n*Decimal(5).sqrt() + Decimal(5*n**2 +sig*4).sqrt())/2))
        else:
            return None
    else:
        return esCuadradoPerfecto( temp +4 ) or esCuadradoPerfecto( temp-4 )


def esUnaPotencia(n,*,valor=False,verbose=False,size=100) -> bool:
    """Dice si n = a^b para algun a y b con b>1
       Si valor es true, regresa en cambio (a,b) si existen, tal que b es minimo,
       sino existen tales valores se regresa None.
       Si verbose es cierto se mostrara cual es el b que se esta considerando.
       En el modo verbose, el valor 'a' calculado para un momento dado
       se mostrara su valor real si la cantidad de digitos en el mismo
       es menor o igual al parametro 'size' sino se mostrara una aproxiamación  """
    if n>3:
        a = isqrt(n)
        if a**2 == n:
            if verbose: print("Es cuadrado perfecto")
            return True if not valor else (a,2)
        else:
            if verbose:
                #print("No es cuadrado perfecto")
                print("b= 2 a=", +Decimal(a,Context(prec=size)) )
        DN = Decimal(n)
        espacio_busqueda = primos_hasta( 1+round( log(2,DN) ) )
        #solo examino raices primas, pues si no es de una de estas tampoco sera
        #de un número compuesto
        next(espacio_busqueda) #elimino 2, pues ya lo examine
        for b in espacio_busqueda:
            a = nthroot(b,DN,decimales=0)
            if verbose:
                print("b=",b,"a=", +Decimal(a,Context(prec=size)) )
            a = round(a)
            if a**b == n:
                return (a,b) if valor else True

    if verbose: print("No esa una potencia")
    return False if not valor else None

def esThabitNumber(n,*,valor=False) -> bool:
    """Dice si n es un número de Thabit.
       Los números de Thabit son los números
       de la forma 3*2^k -1 para algun k>=0
       Si valor es True, regresa ese k si es
       un número de Thabit, sino regresa None.

       https://en.wikipedia.org/wiki/Thabit_number"""
    if n==2:
        return 0 if valor else True
    elif esImpar(n) and n>2:
        d,s = factorizacion_ds(n+1)
        if d==3:
            return s if valor else True
    return None if valor else False

def esDeletablePrime(n,*,valor=False):
    """Dice si el número es un Deletable Prime.
       Un deletable prime es un número tal que si
       eliminando 1 digito cualquiera del mismo
       el resultado es primo, y esto se mantiene
       hasta llegar a un primo de un solo dijito."""
##    Esta es mi respuesta a al problema palnteado en:
##    http://stackoverflow.com/questions/33505735/recursive-function-for-tracing-deletable-primes-python-3
    if esPrimo(n):
        N = str(n)
        S = len(N)
        if S>1 and any( p in N for p in "2 3 5 7".split()) :
            resul = list()
            for num in set( map(lambda x:int("".join(x)),itertools.combinations(N,S-1))):
                temp = esDeletablePrime(num,valor=True)
                if temp:
                    resul.extend( (n,)+tt for tt in temp )
            if valor:
                return tuple(filter(lambda r:len(r)==S, resul ))
            else:
                return any( len(r)==S for r in resul )
        elif n in {2,3,5,7}:
            return ((n,),) if valor else True
    return tuple() if valor else False

def esGlitchNumber(n,base=10,*,valor=False,verbose=False):
    """Son números de la forma b^k -b^m -1 con k>m>0
       estos número tiene la caracteristica de que
       por en base 10, todos sus digitos son 9
       excepto por uno de ellos que es 8

       https://www.youtube.com/watch?v=HPfAnX5blO0"""
    if n >= base**2 - base - 1:
        n += 1
        k,m = 0,0
        if verbose: print("paso1",n,0,0)
        while n%base == 0:
            n //= base
            k += 1
            m += 1
        n += 1
        if verbose: print("paso2",n,k,m)
        while n%base == 0:
            n //= base
            k += 1
        if verbose: print("paso3",n,k,m)
        if 0<m<k and n == 1:
            return (k,m) if valor else True
    return None if valor else False

def esPalindromo(n:int,base=10) -> bool:
    """Dice si el número dado es palindromo en la base dada"""
    return n == revertir_numero(n,base)

def esPalindromoAlado(n:int,base=10) -> bool:
    if esPalindromo(n):
        num = str(n)
        tam = len(num)
        if tam%2==1 and len(set(num)) == 2:
            middle = num[tam//2]
            if 1 == num.count(middle):
                return True #len( set( num.replace( num[tam//2], "" ) ) ) == 1
    return False

def esTriagularNumber(Tn:int,*,valor=False) -> bool:
    """Dice si Tn es un número Triangular.
       Estos son los números de la forma (n(n+1))/2 para algun n>=0
       Si valor es cierto regresa en cambio este n si exite.
       https://en.wikipedia.org/wiki/Triangular_number"""
    if esNatural(Tn) :
        discriminate = 8*Tn +1
        temp = isqrt(discriminate)
        if temp**2 == discriminate:
            if (temp-1)%2==0:
                return (temp-1)//2 if valor else True
    return None if valor else False

def esPentagonalNumber(Pn:int,*,valor=False) -> bool:
    """Dice si Pn es un número Pentagonal.
       Estos son los números de la forma (3n^2 -n)/2 para algun n>0
       Si valor es cierto regresa en cambio este n si exite.
       https://en.wikipedia.org/wiki/Pentagonal_number"""
    if esNatural(Pn) and Pn >0:
        discriminate = 24*Pn +1
        temp = isqrt(discriminate)
        if temp**2 == discriminate:
            if (temp+1)%6==0:
                return (temp+1)//6 if valor else True
    return None if valor else False

def esHexagonalNumber(Hn:int,*,valor=False) -> bool:
    """Dice si Hn es un número Hexagonal.
       Estos son los números de la forma (5n^2 -3n)/2 para algun n>0
       Si valor es cierto regresa en cambio este n si exite.
       https://en.wikipedia.org/wiki/Hexagonal_number"""
    if esNatural(Hn) and Hn >0:
        discriminate = 8*Hn +1
        temp = isqrt(discriminate)
        if temp**2 == discriminate:
            if (temp+1)%4==0:
                return (temp+1)//4 if valor else True
    return None if valor else False

def esPolygonalNumber(Pn:int,S:int,*,valor=False) -> bool:
    """Dice si Pn es un S-gonal númber.
       Pn es un S-gonal númber si se puede puner esa cantidad
       de puntos formando un poligono regular de S lados.
       Si valor es cierto regresa en cambio el indice de ese número.
       https://en.wikipedia.org/wiki/Polygonal_number"""
    if not (esNatural(S) and S>2):
        raise ValueError("El número de lados del poligono debe ser mayor o igual a 3")
    if esNatural(Pn) and Pn>0:
        discriminate = 8*(S-2)*Pn + (S-4)**2
        temp = isqrt(discriminate)
        if temp**2 == discriminate:
            temp += S-4
            if temp % (2*(S-2)) == 0:
                return (temp // (2*(S-2))) if valor else True
    return None if valor else False

################################################################################
### --------------------- Sucesión de números de Lucas -------------------------
################################################################################
#https://en.wikipedia.org/wiki/Lucas_sequence

def sucesion_de_Lucas_Generalizada(a,b,P,Q,M=None):
    """Generador de la sucesión de Lucas generalizada con casos base a y b y parametros P y Q.
       Si M es suministrado calcula LG(n) mod M para todo n
       La sucesiones de Lucas generalizada se define como sigue:
       LG(0) = a
       LG(1) = b
       LG(n) = P*LG(n-1) - Q*LG(n-2)"""
    Ln    = a
    Lnext = b
    if M: Ln,Lnext = Ln % M, Lnext % M
    while True:
        yield Ln
        Ln,Lnext = Lnext, P*Lnext -Q*Ln if not M else (P*Lnext -Q*Ln) % M

def sucesion_de_Lucas_Generalizada_n(n,a,b,P,Q,M=None) -> int:
    """Calcula el n-esimo elemento de la sucesión de Lucas generalizada
       con casos base a y b y parametros P y Q.
       Si M es suministrado calcula LG(n) mod M
       La sucesiones de Lucas generalizada se define como sigue:
       LG(0) = a
       LG(1) = b
       LG(n) = P*LG(n-1) - Q*LG(n-2)"""
    #en.wikipedia.org/wiki/Recurrence_relation#Solving_via_linear_algebra
    if M:
        a,b = a % M, b % M
    resul = ( pow(Matrix2x2(P,-Q,1,0),n,M) * Vector2(b,a) )[1]
    return resul if not M else resul%M

def sucesiones_de_Lucas(n:int,P:int,Q:int,M:int=None,*,darQ=False) -> "( Un(p,q), Vn(p,q) )":
    """Calcula el n-esimo elemento de las sucesiones de Lucas de primer y segundo tipo.
       Si M es suministrado calcula: Un mod M y Vn mod M
       Si darQ es cierto, regresa en cambio ( Un(p,q), Vn(p,q), Q^n )
       que estara en modulo si M es suministrado

       Estas sucesiones se definen como sigue:
       Primer tipo
       U0(p,q) = 0
       U1(p,q) = 1
       Un(p,q) = p*Un-1(p,q) - q*Un-2(p,q) para todo n>1

       Segundo tipo
       V0(p,q) = 2
       V1(p,q) = p
       Vn(p,q) = p*Vn-1(p,q) - q*Vn-2(p,q) para todo n>1

       en.wikipedia.org/wiki/Lucas_sequence"""
    if n<0:
        raise NoEsNumeroNatural("El objeto no representa un número natural")
    if n==0:
        return (0,2) if not M else (0 , 2 % M)
    else:
        Uk  = 1  # U1  Uk
        Uk1 = P  # U2  Uk+1
        Vk  = P  # V1  Vk
        Qk  = Q  # Q^1 Q^k
        if M: Uk, Uk1, Vk, Qk = Uk % M , Uk1 % M, Vk % M, Qk % M
        control = 2**(n.bit_length()-1) >>1
        while control >0:
            if n & control == control:
                Uk1, Uk  = P*Uk1**2 -2*Q*Uk1*Uk , Uk1**2 - Q*Uk**2 # U2k+2, U2k+1
                Vk = 2*Uk1 - P*Uk                                  #        V2k+1
                Qk = Qk*Qk*Q                                       #        Q^(2k+1)
            else:
                Uk1, Uk  = Uk1**2 -Q*Uk**2 , 2*Uk1*Uk -P*Uk**2     # U2k+1, U2k
                Vk = Vk**2 -2*Qk                                   #        V2k
                Qk = Qk*Qk                                         #        Q^2k
            if M: Uk, Uk1, Vk, Qk = Uk % M , Uk1 % M, Vk % M, Qk % M
            control >>= 1
        if darQ:
            return Uk,Vk,Qk
        return Uk,Vk


def sucesion_de_lucas_primer_tipo(n:int,P:int,Q:int,M:int=None) -> "Un(p,q)":
    """Un(p,q) Da el n-esimo elemento de la sucesión de Lucas de primer tipo.
       Si M es otorgado calcula: Un(P,Q) mod M
       Esta sucesiones se define como sigue:

       U0(p,q) = 0
       U1(p,q) = 1
       Un(p,q) = p*Un-1(p,q) - q*Un-2(p,q) para todo n>1"""
    if n<0 :
        raise NoEsNumeroNatural("El objeto no representa un número natural")
    if n==0:
        return 0
    Uk  = 1  # U1 Uk
    Uk1 = P  # U2 Uk+1
    if M: Uk, Uk1 = Uk % M , Uk1 % M
    control = 2**(n.bit_length()-1) >>1
    while control >0:
        if n & control == control:
            Uk1, Uk  = P*Uk1**2 -2*Q*Uk1*Uk , Uk1**2 - Q*Uk**2 # U2k+2, U2k+1
        else:
            Uk1, Uk  = Uk1**2 -Q*Uk**2 , 2*Uk1*Uk -P*Uk**2     # U2k+1, U2k
        if M: Uk, Uk1 = Uk % M , Uk1 % M
        control >>= 1
    return Uk


def sucesion_de_lucas_segundo_tipo(n:int,P:int,Q:int,M:int=None,*,darQ=False) -> "Vn(p,q)":
    """Vn(p,q) Da el n-esimo elemento de la sucesión de Lucas de segundo tipo.
       Si M es otorgado calcula: Vn(P,Q) mod M
       Si darQ es cierto, regresa en cambio ( Vn(p,q), Q^n )
       que estaran en modulo si M es suministrado.

       Esta sucesión se define como sigue:

       V0(p,q) = 2
       V1(p,q) = p
       Vn(p,q) = p*Vn-1(p,q) - q*Vn-2(p,q) para todo n>1"""
    if n<0:
        raise NoEsNumeroNatural("El objeto no representa un número natural")
    if n==0:
        return 2 if not M else 2%M
    Vk  = P           #V1  Vk
    Qk  = Q           #Q^1 Q^k
    Vk1 = P*P -Q*2    #V2  Vk+1
    if M: Vk,Vk1,Qk = Vk % M ,Vk1 % M , Qk % M
    control = 2**(n.bit_length()-1) >>1
    while control > 0:
        if n & control == control:
            Vk  = Vk1*Vk - Qk*P   # V2k+1
            Vk1 = Vk1**2 -2*Qk*Q  # V2k+2
            Qk  = Qk*Qk*Q         # Q^(2k+1)
        else:
            Vk1 = Vk1*Vk - Qk*P   # V2k+1
            Vk  = Vk**2 -2*Qk     # V2k
            Qk  = Qk*Qk           # Q^2k
        if M: Vk,Vk1,Qk= Vk % M ,Vk1 % M , Qk % M
        control >>= 1
    if darQ:
        return Vk,Qk
    return Vk

def sucesion_de_lucas_segundo_tipo_Q1(n:int,P:int,M:int=None) -> "Vn(P,1)":
    """Calcula la sucesión de Lucas de segunda especie con parametro Q=1: Vn(P,1).
       Si M es otorgado calcula: Vn(P,1) mod M

       Estas sucesión se definen como sigue:
       V0(p,q) = 2
       V1(p,q) = p
       Vn(p,q) = p*Vn-1(p,q) - q*Vn-2(p,q) para todo n>1"""
    if n<0:
        raise NoEsNumeroNatural("El objeto no representa un número natural")
    if n==0:
        return 2 if not M else 2%M
    Vk = P        #V1 Vk
    Vk1 = P**2 -2 #V2 Vk+1
    if M: Vk,Vk1 = Vk % M ,Vk1 % M
    control = 2**(n.bit_length()-1) >>1
    while control > 0:
        if n & control == control:
            Vk  = Vk*Vk1 - P #V2k+1
            Vk1 = Vk1**2 - 2 #V2k+2
        else:
            Vk1 = Vk*Vk1 - P #V2k+1
            Vk  = Vk**2  - 2 #V2k
        if M: Vk,Vk1 = Vk % M ,Vk1 % M
        control >>= 1
    return Vk


################################################################################
### --------------------- Secuencias de números Naturales ----------------------
################################################################################



def mersenne(n:int=None,m:int=None):
    """Secuencia de los números de Mersenne.
       Estos son los números de la forma 2^n -1
       para algun n natural.
       Si n es suministrado, calcula el n-esimo
       número de Mersenne.
       Si m es suministrado calcula el modulo de
       ese número o de toda la secuencia segun
       sea el caso"""
    if n is not None and n>=0:
        if m:
            return (pow(2,n,m)-1)%m  #sucesion_de_lucas_primer_tipo(n,3,2,m)
        return (2**n)-1
    return sucesion_de_Lucas_Generalizada(0,1,3,2,m)


def carmichael(n:int=None):
    """Secuencia de los números de Carmichael.
       Si n es suministrado, calcula el n-esimo
       números de Carmichael.
       Estos son números compuestos n tales que para
       todo b en 1<b<n coprimo con n se cumple que
       b^(n-1)=1 (mod n)"""
    if n is not None and n>=0:
        car=carmichael()
        if n>0:
            itertools_recipes.consume(n,car)
        return next(car)
    else:
        return ( i for i in itertools.count(1)
                 if not esPrimo(i) and all( pow(b,i-1,i)==1 for b in coprimos(i) )
                 )


__PERFECT_NUMBER_LIMIT = 15 #limitite hasta el cual el calculo de números perfectos es "instantaneo"

def perfectos(n:int,*,verbose=True,continuar="") -> [int]:
    """Da una lista con los primeros n números perfectos"""
    if n>0:
        if n>__PERFECT_NUMBER_LIMIT and continuar!="si":
            print( "Ha solicitado", n, "números perfectos, esta operación puede tomar mucho tiempo.")
            print( "¿¿Desea continuar??")
            print( "Escriba \"si\" para proceder con el calculo solicitado tome el tiempo que tome.")
            print( "Escriba \"cota\" para entregara una lista con los primeros",
                    __PERFECT_NUMBER_LIMIT,"números perfectos")
            print( "Si no desea continuar, presione enter para salir" )
            respuesta = input("Eligio: ")
            if respuesta=="cota":
                n = __PERFECT_NUMBER_LIMIT
            elif respuesta!="si":
                return []
        res=[]
        for i,x in enumerate( itertools.islice(mersenne_prime_base(),n) ,1 ):
            z = ((2**(x-1))*(2**x-1))
            res.append(z)
            if verbose:
                print( i,"-->",z)#,"raiz",x,"Mersenne prime (2**%d)-1="%x,(2**x)-1)
        if verbose:
            print("\n\n")
        return res
    else:
        if n==0:
            raise RequiereNumeroNaturalDesdeUno("Esta función sólo acepta números naturales mayores o iguales a 1")
        raise NoEsNumeroNatural("El objeto no representa un número natural")


def fila_pascal(n:int):
    """Generador que da la n-esima fila del triangulo de Pascal"""
    if n >= 0:
        yield 1
        if n==0:
            return
            #raise StopIteration
        elif n==1:
            yield 1
        else:
            yield n
            resul = n
            for i in range(1,n):
                resul = (resul*(n-i))//(i+1)
                yield resul
    else:
        raise NoEsNumeroNatural("El objeto no representa un número natural")




def pseudoFiboForever(a:int,b:int,m:int=None):
    """Generador de una sucecion como la de Fibonacci con casos bases a y b
       Si m es suministrado, calcula: PF(n) mod m para todo n

       La sucesion de PseudoFibonacci se define como sigue:
       PF(0) = a
       PF(1) = b
       PF(n) = PF(n-1) + PF(n-2), para todo n>=2"""
    return sucesion_de_Lucas_Generalizada(a,b,1,-1,m)


def pseudoFibo(n:int,a:int,b:int,m:int=None) -> int:
    """N-esimo elemento de una sucecion como la de Fibonacci con casos bases a y b
       Si m es suministrado, calcula: PF(n) mod m

       La sucesion de PseudoFibonacci se define como sigue:
       PF(0) = a
       PF(1) = b
       PF(n) = PF(n-1) + PF(n-2), para todo n>=2"""
    if n >= 0:
        return sucesion_de_Lucas_Generalizada_n(n,a,b,1,-1,m)
    else:
        raise NoEsNumeroNatural("El objeto no representa un número natural")


def fibonacci(n:int=None,m:int=None):
    """Suceción de números de Fibonacci.
       Si n es suministrado calcula el n-esimo elemento de la suceción de Fibonacci.
       Si m es suministrado, calcula: fib(n) mod m (para todo n)

       La sucesión de Fibonacci se define como sigue:
       fib(0)=0
       fib(1)=1
       fib(n)=fib(n-1) + fib(n-2), para todo n>=2


       en.wikipedia.org/wiki/Fibonacci_number"""
    if n is not None:
        return sucesion_de_lucas_primer_tipo(n,1,-1,m)
    else:
        return sucesion_de_Lucas_Generalizada(0,1,1,-1,m)


def lucas(n:int=None,m:int=None) -> int:
    """Sucesión de números de Lucas.
       Si n es suministrado calcula el n-esimo elemento de la sucesión de Lucas.
       Si m es suministrado, calcula: Ln mod m (para todo n)
       La sucesión de Lucas se define como sigue:
       lucas(0)=2
       lucas(1)=1
       lucas(n)=lucas(n-1)+lucas(n-2), para todo n>=2"""
    if n is not None:
        if n >= 0:
            if n == 0:
                return 2 if not m else 2%m
            Lk  =  1 # L1 Lk
            Lk1 =  3 # L2 Lk+1
            sig = -1 # (-1)^k
            if m: Lk,Lk1 = Lk % m, Lk1 % m
            control = 2**(n.bit_length() -1) >> 1
            while control > 0:
                if n & control == control:
                    Lk  = Lk1*Lk -sig   # L2k+1
                    Lk1 = Lk1**2 +2*sig # L2k+2
                    sig = -1            # (-1)^(2k+1)
                else:
                    Lk1 = Lk1*Lk - sig  # L2k+1
                    Lk  = Lk**2 -2*sig  # L2k
                    sig = 1             # (-1)^2k
                if m: Lk,Lk1 = Lk % m, Lk1 % m
                control >>= 1
            return Lk
        else:
            raise NoEsNumeroNatural("El objeto no representa un número natural")
    else:
        return sucesion_de_Lucas_Generalizada(2,1,1,-1,m)







def pell_number(n,m=None):
    """Calcule el n-esimo elemento de la suceción de números de Pell
       la suceción de números de Pell se define como sique:
       P(0) = 0
       P(1) = 1
       P(n) = 2*P(n-1) + P(n-2)

       en.wikipedia.org/wiki/Pell_number"""
    return sucesion_de_lucas_primer_tipo(n,2,-1,m)

def jacobsthal_number(n):
    """Calcule el n-esimo elemento de la suceción de números de Jacobsthal
       la suceción de números de Jacobsthal se define como sique:
       J(0) = 0
       J(1) = 1
       J(n) = J(n-1) + 2*J(n-2)

       en.wikipedia.org/wiki/Jacobsthal_number"""
    return (2**n - (-1)**n)//3

def jacobsthal_lucas_number(n):
    """Calcule el n-esimo elemento de la suceción de números de Jacobsthal-Lucas
       la suceción de números de Jacobsthal-lucas se define como sique:
       J(0) = 2
       J(1) = 1
       J(n) = J(n-1) + 2*J(n-2)

       en.wikipedia.org/wiki/Jacobsthal_number"""
    return 2**n + (-1)**n

def fermat_number(n:int) -> int:
    """Calcule el n-esimo número de Fermat.
       Los numeros de fermat son aquellos de la forma:
       F(n) = 2^(2^n) +1

       en.wikipedia.org/wiki/Fermat_number"""
    return 1 + 2**(2**n)

def cullen_number(n:int) -> int:
    """Calcule el n-esimo número de Cullen.
       Estos son los números de la forma:
       C(n)=n*2^n +1

       en.wikipedia.org/wiki/Cullen_number"""
    return 1+ n*(2**n)

def leylan(n:int):
    """https://www.youtube.com/watch?v=Lsu2dIr_c8k"""
    for x in range(2,n+1):
        for y in range(2,x+1):
            yield x,y,x**y +y**x

def wilson_number():
    """https://en.wikipedia.org/wiki/Wilson_prime#Wilson_numbers"""
    def W(n,m):
        resul = 1
        for k in coprimos(n):
            resul = (resul*k) % m
            if resul==0:
                break
        return (resul + ( 1 if raicesPrimitivas(n) else -1 )) %m
    print(W.__qualname__,repr(W))
    for N in itertools.count(1):
        if W(N,N**2)==0:
            yield N

def thabit_number(n):
    """Da el n esimo número de Thabit.
       Estos son los numeros de la forma
       3*2^n -1"""
    return 3 * 2**n -1

def glitch_number(k,m,base=10) -> int :
    """Son números de la forma b^k -b^m -1 con k>m>0
       estos número tiene la caracteristica de que
       por en base 10, todos sus digitos son 9
       excepto por uno de ellos que es 8

       https://www.youtube.com/watch?v=HPfAnX5blO0"""
    return base**k -base**m -1

def secuencia_de_collatz(n:int) -> int:
    """Generador de la secuencia de Collatz iniciando en n.
       La secuencia de Collatz se define como sigue:
       
       C_0 = n 
       C_i = F( C_(i-1) )   con F(n) = n/2 if esPar(n) else 3n+1
       
       la secuencia termina cuando C_i sea 1.
       Se ha conjeturado, pero no se ha demostrado que para todo n la 
       secuencia termina.
       
       
       https://en.wikipedia.org/wiki/Collatz_conjecture"""
    if esNatural(n) and n>0:
        yield n
        while n!=1:
            if esPar(n):
                n //= 2
            else:
                n = 3*n+1
            yield n
    else:
        raise ValueError("n debe ser mayor o igual a 1")

def triangular_number(n):
    """Da el n-esimo número triangular.
       Estos son los números de la forma (n(n+1))/2
       También en la suma de todos los números naturales
       hasta n
       https://en.wikipedia.org/wiki/Triangular_number"""
    if esNatural(n) :
        return (n*(n+1))//2
    else:
        raise NoEsNumeroNatural("El objeto no representa un número natural")

def pentagonal_number(n):
    """Da el n-esimo número pentagonal.
       Estos son los números de la forma (3n^2 -n)/2
       https://en.wikipedia.org/wiki/Pentagonal_number"""
    if esNatural(n) and n>0:
        return (3*n**2 -n)//2
    else:
        raise RequiereNumeroNaturalDesdeUno("Esta función sólo acepta números naturales mayores o iguales a 1")

def hexagonal_number(n):
    """Da el n-esimo número pentagonal.
       Estos son los números de la forma (3n^2 -n)/2
       https://en.wikipedia.org/wiki/Hexagonal_number"""
    if esNatural(n) and n>0:
        return n*(2*n-1)
    else:
        raise RequiereNumeroNaturalDesdeUno("Esta función sólo acepta números naturales mayores o iguales a 1")


def polygonal_number(n:int,S:int) -> int:
    """Da el n-esimo número S-gonal.
       Estos son los números que indican la cantidad de puntos que se
       necesitan para formar poligono regular de S lados de tamaño n
       https://en.wikipedia.org/wiki/Polygonal_number"""
    if not (esNatural(S) and S>2):
        raise ValueError("El número de lados del poligono debe ser mayor o igual a 3")
    if esNatural(n) and n>0:
        return ((n**2)*(S-2) - n*(S-4))//2
    else:
        raise ValueError("No se puede construir un poligono de tamaño menor que 1")
################################################################################
# --------------------------- Teoria de Conjuntos ------------------------------
################################################################################


def factorial(n:int,m:int=None) -> int:
    """Factorial de n o n!. Si m es dado, calcula n! mod m
       Cuenta todos los posibles arreglos lineales de n objetos"""
    if n >= 0 :
        if not m:
            return productoria( range(1,n+1) )
        else:
            if 0 <= m <= n:
                return 0
            resul = 1 % m
            for x in range(2,n+1):
                resul = (resul*x) % m
                if resul==0:
                    return 0
            return resul
    else:
        raise NoEsNumeroNatural("El objeto no representa un número natural")



def factorialDescendente(n:int,k:int) -> int:
    """Factorial descendente de N con K descensos.
       Cuenta todas las forma de hacer arreglos lineales de longitud K
       con un conjunto de N objetos"""
    if n >= 0 and k >= 0:
        return productoria( range( (n-k+1),n+1 ) )
        #return reduce(lambda x,y: x*y, range((n-k+1),n+1) ,1 )
    else:
        raise NoEsNumeroNatural("El objeto no representa un número natural")



def factorialAscendente(n:int,k:int) -> int:
    """Factorial ascendente de N con K ascensos.
       Cuenta la cantidad de formas de meter N objetos
       en K cajas formando ordenes lineales dentro de las cajas"""
    if n >= 0 and k >= 0:
        return productoria( range(n,n+k) )
        #return reduce(lambda x,y:x*y, range(n,n+k),1)
    else:
        raise NoEsNumeroNatural("El objeto no representa un número natural")



def combinatorio(n:int,k:int) -> int:
    """Número combinatorio N en K.
       Cuenta el número de sub-conjuntos de tamaño K de un N-conjunto
       O la cantidad de formas de elegir K objetos de entre N de ellos"""
    if n >= 0 and k >= 0 :
        if n==k:
            return 1
        elif k<n:
            return factorialDescendente(n,k)//factorial(k)
        else:
            return 0
    else:
        raise NoEsNumeroNatural("El objeto no representa un número natural")



def combinatorioMulticonjunto(n:int,k:int) -> int:
    """Número combinatorio de multiconjunto N en K.
       Cuenta el número de sub-multi-conjuntos de tamaño K de un N-conjunto
       O la cantidad de formas de elegir K objetos de entre N de ellos con
       la posibilidad de repetir uno o más de los objetos elegidos"""
    if n >= 0 and k >= 0:
        return factorialAscendente(n,k)//factorial(k)
    else:
        raise NoEsNumeroNatural("El objeto no representa un número natural")



def cfuerte(n:int,k:int) -> int:
    """Combinaciones fuertes del número N en K pedasos.
       Cuenta la cantidad de soluciones a la ecuación:
         X1+X2+X3+....+Xk = N, para todo Xi>0 y N,K>0
       O cuenta la cantidad de formas meter N objetos indistinguibles en
        K cajas indistinguibles sin dejar ninguna vacia"""
    if n >= 0 and k >= 0:
        if n>0 and k>0:
            return combinatorio(n-1,k-1)
        else:
            raise RequiereNumeroNaturalDesdeUno("Esta función sólo acepta números naturales mayores o iguales a 1")
    else:
        raise NoEsNumeroNatural("El objeto no representa un número natural")


def cdebil(n:int,k:int) -> int:
    """Combinaciones débiles del número N en K pedasos.
       Cuenta la cantidad de soluciones a la ecuación:
        X1+X2+X3+...+Xk=N, para todo Xi>=0 y K>0
       O cuenta la cantidad de formas de meter N objetos indistinguibles en
        K cajas indistinguibles pudiendo dejar una o más cajas vacias"""
    if n >= 0 and k >= 0:
        if k>0:
            return combinatorioMulticonjunto(n+1,k-1)
        else:
            raise NaturalError("k debe ser mayor o igual que 1")
    else:
        raise NoEsNumeroNatural("El objeto no representa un número natural")




def bell(n:int) -> int:
    """Número de Bell. Cuenta todas las particiones posibles de un N-conjunto.

       Se emplea el algoritmo del Triangulo de Bell para calcularlos
       http://en.wikipedia.org/wiki/Bell_number"""
    if n >= 0:
        if n==0 or n==1:
            return 1
        else:
            def __nextFilaBell(_x,_r):
                for _y in _x:
                    _r.insert(0,_y+_r[0])
                return _r
            def __lastFilaBell(_m,_b):
                while _m>0:
                    _t=_b[0]
                    _b.reverse()
                    _b=__nextFilaBell(_b,[_t])
                    _m-=1
                return _b
            t=__lastFilaBell(n-1,[1])
            return t[0]
    else:
        raise NoEsNumeroNatural("El objeto no representa un número natural")



def stirling(n:int,k:int,*,lista:bool=False):
    """Número de Stirling de segunda especie.
       Cuenta la cantidad de formas de particionar un N-conjunto en K-bloques.
       O cuenta las formas de colocar N objetos diferentes en K cajas
       indistingibles sin dejar ninguna vacia.
        Notece que cuando las cajas tienen algo,
        ya son diferenciable por ese algo

       Si lista=True, se regresa en cambio una lista con los
       numeros de Stirling para K en 0<=K<=N"""
    if n >= 0 and k >= 0:
        if k>n and not lista:
            return 0
        elif n==k and not lista:
            return 1
        elif k==0 and not lista:
            return 0
        elif k==1 and not lista:
            return 1
        else:
            def __nextFilaStir(_xyz,_fn,_k):
                while len(_xyz)>1:
                    _x=_xyz.pop(0)
                    _y=_xyz[0]
                    _fn.append(_x+_k*_y)
                    _k+=1
                if len(_xyz)==0:
                    return _fn
                elif len(_xyz)==1:
                    _fn.append(1)
                    return _fn
                else:
                    raise NaturalError("Esto nunca debe pasar")
            def __lastFilaStir(_lf,_n):
                while _n>0:
                    _lf = __nextFilaStir(_lf,[0],1)
                    _n-=1
                return _lf
            lfs=__lastFilaStir([1],n)
            if lista:
                return lfs
            else:
                return lfs[k]
    else:
        raise NoEsNumeroNatural("El objeto no representa un número natural")


################################################################################
### ------------------------------ Miselaneos ----------------------------------
################################################################################


def contruirNumeroCiclico(p:int,b:int=10) -> int:
    """www.youtube.com/watch?v=WUlaUalgxqI
       en.wikipedia.org/wiki/Cyclic_number
       
       Arroja RuntimeError en caso que no se pueda construir el número ciclico"""
    if sonCoprimos(p,b):
        if esPrimo(p):
            t = 0
            r = 1
            n = 0
            while True:
                t = t+1
                x = r*b
                d = x//p
                r = x%p
                n = n*b + d
                if r==1:
                    break
            if t == p-1:
                return n
            else:
                raise RuntimeError("No se pudo contruir un número ciclico con este constructor")
        else:
            raise ValueError("El contructor p del número ciclico debe ser primo")
    else:
        raise ValueError("El contructor p del numero ciclico de ser coprimo con la base b")

def primer_digito(n:int) -> int:
    """Dice cual es el primer digito del número dado"""
    if n==0:
        return 0
    if n<0:
        return primer_digito(-n)
    if 0 < n < 1:
        while n < 1:
            n *= 10
    mod = log10(n) % 1
    for k in range(1,11):
        if log10(k) <= mod <= log10(k+1):
            return k

def revertir_numero(n:int,base=10) -> int:
    """Regresa el número con los digitos invertidos en la base dada. 123 -> 321"""
    if esNatural(n):
        digitos = list()
        while n != 0:
            n,d = divmod(n,base)
            digitos.insert(0,d)
        return sum( d*base**i for i,d in enumerate(digitos) )
    else:
        raise NoEsNumeroNatural("El objeto no representa un número natural")

def pitagorian_triple(tope:int=100,primitivos=True) -> (int,int,int):
    """Generedor de tripletas de números pitagoricos (a,b,c).
       Estos son los números naturales mayores que cero tales:

       a^2 + b^2 = c^2  con a,b,c en [1,tope), a<b y si primitivos es cierto, coprimos cada par de ellos
       
       https://en.wikipedia.org/wiki/Tree_of_primitive_Pythagorean_triples"""
    A = ( ( 1,-2, 2 ),
          ( 2,-1, 2 ),
          ( 2,-2, 3 )
        )
    B = ( ( 1, 2, 2 ),
          ( 2, 1, 2 ),
          ( 2, 2, 3 )
        )
    C = ( (-1, 2, 2),
          (-2, 1, 2),
          (-2, 2, 3)
         )
    ini = (3,4,5)
    generador = ( (min(a,b),max(a,b),c) for a,b,c in __pitagorianTree(ini,(A,B,C),tope) )
    if primitivos:
        yield from generador
    else:
        for tri in generador:
            yield tri
            for n in range(2,tope):
                newtri = tuple(map(lambda x:x*n,tri))
                if all( x<tope for x in newtri):
                    yield newtri
                else:
                    break
    
    
def __pitagorianTree(root,matrices,tope):
    if all( x<tope for x in root):
        yield root
        for M in matrices:
            newroot = tuple( n for n in map(lambda x:itertools_recipes.dotproduct(root,x),M))
            yield from __pitagorianTree(newroot,matrices,tope)
        
#smallPsPF([2,7,61],[3,5], 25326001)
#n=                      3883000001
# respuesta              4759123141
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



class Vector2(collections.namedtuple("Vector2_base","x y")):
    """Vector2(x,y) Vector de tamaño 2"""

    def __add__(self,otro):
        if isinstance(otro,(self.__class__,tuple)):
            if len(otro)!=2:
                raise ValueError("Vectores de tamaño diferente")
            x,y = self
            a,b = otro
            return self.__class__( x+a, y+b )
        else:
            return NotImplemented

    def __mul__(self,otro):
        if isinstance(otro,numbers.Number):
            x,y = self
            return self.__class__(x*otro,y*otro)
        if isinstance(otro,self.__class__):#producto punto
            x,y = self
            a,b = otro
            return x*a + y*b
        return NotImplemented

    def __mod__(self,m):
        x,y = self
        return self.__class__( x % m, y % m )


class Matrix2x2(collections.namedtuple("Matrix2x2_base","x y z w")):
    """Matrix2x2(x, y, z, w) Matriz cuadrada de 2x2 con campos nombrados tales que
             |x y|
             |z w|
       Ofrece la suma de matrices, multiplicación de matrices, por escalar, y vectores,
       exponenciación por un escalar natural y modulo por número"""

    def __identidad__(self):
        return self.__class__(1,0,0,1)

    def __add__(self,otro):
        if isinstance(otro,self.__class__):
            x,y,z,w = self
            a,b,c,d = otro
            return self.__class__(x+a, y+b, z+c, w+d)
        else:
            return NotImplemented

    def __mul__(self,otro):
        if isinstance(otro,self.__class__):
            x,y,z,w = self
            a,b,c,d = otro
            return self.__class__( x*a+y*c , x*b+y*d, z*a+w*c, z*b+w*d )
        if isinstance(otro,numbers.Number):
            x,y,z,w = self
            return self.__class__(x*otro, y*otro, z*otro, w*otro)
        if isinstance(otro,Vector2):#multiplicacion por vector por derecha
            x,y,z,w = self
            a,b = otro
            return otro.__class__(x*a + y*b , z*a + w*b )
        return NotImplemented

    def __rmul__(self,otro):
        if isinstance(otro,Vector2):#multiplicacion por vector por izquierda
            a,b = otro
            x,y,z,w = self
            return otro.__class__(a*x + b*z , a*y + b*w )
        return NotImplemented

    def __pow__(self,n:int,M:int=None):
        if n<0:
            return NotImplementedError("No se ha implementado el calculo de inversa de esta matriz")
        if n==0:
            I = self.__identidad__()
            return I if not M else I % M
        if n==1:
            return self if not M else self%M
        if n==2:
            M2 = self*self
            return M2 if not M else M2 % M
        m1 = pow(self,n//2,M)
        m2 = pow(m1,2,M)
        if not n&1:
            return m2
        else:
            m3 = self*m2
            return m3 if not M else m3 % M

    def __mod__(self,mod:int):
        x,y,z,w = self
        return self.__class__(x%mod, y%mod, z%mod, w%mod)

    def determinante(self):
        a,b,c,d = self
        return a*d - b*c

    def __str__(self):
        x,y,z,w = self
        return "|{} {}|\n|{} {}|".format(x,y,z,w)



class _Matrix2x2_Simetrica(collections.namedtuple("Matrix2x2_base_simetrica","x y z"),Matrix2x2):
    """Matrix2x2_Simetrica(x, y, z) Matriz cuadrada simetrica de 2x2 con campos nombrados tales que
             |x y|
             |y z|
       Ofrece la suma con otras matrices simetricas, multiplicación con otras matrices simetricas
       y por escalar, exponenciación por un escalar natural y modulo por un número.

       Esta matriz asume que no importa lo que se le haga resulta en una matriz simetrica
       ya que con esa supocisión se ahorra memoria usando solo 3 campos en lugar de 4.
       Usar solo si ese es el caso, sino usar la versión no simetrica."""

    def __identidad__(self):
        return self.__class__(1,0,1)

    def __eq__(self,otro):
        if isinstance(otro,self.__class__):
            return tuple(self)==tuple(otro)
        x,y,z = self
        return (x,y,y,z) == otro

    def __add__(self,otro):
        x,y,z = self
        if isinstance(otro,self.__class__):
            a,b,c = otro
            return self.__class__(x+a, y+b, z+c)
        else:
            return Matrix2x2(x,y,y,z)+otro

    def __mul__(self,otro):
        x,y,z = self
        if isinstance(otro,self.__class__):
            a,b,c = otro
            yb = b*y
            return self.__class__( x*a+yb, x*b+y*c, yb+z*c)
        if isinstance(otro,numbers.Number):
            return self.__class__(x*otro, y*otro, z*otro)
        else:
            return Matrix2x2(x,y,y,z)*otro

    def __mod__(self,mod:int):
        x,y,z =  tuple.__iter__(self)
        return self.__class__(x%mod, y%mod, z%mod)

    def __str__(self):
        x,y,z = self
        return str(Matrix2x2(x,y,y,z))

    def determinante(self):
        x,y,z = self
        return Matrix2x2(x,y,y,z).determinante()




@total_ordering
class NumeroFactorizado(numbers.Number): #numbers.Integral):
    """Calse para números naturales mayores o iguales a 1
       factorizados en factores primos"""

    def __init__(self,*argv,**karg):
        self.__factores=dict()
        for x in argv:
            if esNatural(x):
                if esPrimo(x):
                    if x in self.__factores:
                        self.__factores[x] += 1
                    else:
                        self.__factores[x] = 1
                else:
                    raise ValueError("El factor %d no es primo"%x)
            elif isinstance(x,collections.Sequence) and len(x)==2:
                p,m = x
                if esNatural(p) and esNatural(m) and m>0:
                    if esPrimo(p):
                        if p in self.__factores:
                            self.__factores[p] += m
                        else:
                            self.__factores[p] = m
                    else:
                        raise ValueError("El factor "+str(x)+" no es (primo,int)")
                else:
                    raise ValueError(str(x)+" No es valido")
            else:
                raise ValueError(str(x)+" No es valido")

    def __str__(self):
        if self.__factores:
            return " * ".join( map(lambda x:"**".join(map(str,x)),sorted(self.__factores.items(),key=lambda y:y[0])) )
        return "1"

    def __repr__(self):
        return self.__class__.__qualname__ + "( " + ",".join( map( repr, self.__factores.items() ) ) +" )"

    def __int__(self):
        return productoria( map(lambda par:pow(*par) ,self.__factores.items()) )

    def __eq__(self,otro):
        if isinstance(otro,self.__class__):
            return self.__factores == otro.__factores
        else:
            return int(self) == otro

    def __lt__(self,otro):
        resul = 1
        if resul < otro:
            for p,m in self.__factores.items():
                for x in range(m):
                    resul *= p
                    if not resul < otro:
                        return False
            return True
        else:
            return False

    def __hash__(self):
        return hash(int(self))

    def __add__(self,otro):
        return int(self) + otro

    def __mul__(self,otro):
        if isinstance(otro,self.__class__):
            new = dict( self.__factores.items() )
            for p,m in otro.__factores.items():
                if p in new:
                    new[p] += m
                else:
                    new[p] = m
            resul = self.__class__()
            resul.__factores = new
            return resul
        elif esNatural(otro):
            if otro == 0:
                return 0
            if otro == 1:
                return self
            else:
                new = dict( self.__factores.items() )
                for p,m in factorizacion(otro):
                    if p in new:
                        new[p] += m
                    else:
                        new[p] = m
                resul = self.__class__()
                resul.__factores = new
                return resul
        return int(self)*otro

    def __pow__(self,exp,mod=None):
        if mod is not None:
            if mod == 0:
                raise ZeroDivisionError()
        if esNatural(exp):
            if exp == 0:
                return self.__class__() if not mod else 1 % mod
            if exp == 1:
                return self if not mod else self % mod
            else:
                if mod:
                    resul = 1
                    for p,m in self.__factores.items():
                        resul *= pow(p,m*exp,mod)
                        if resul == 0:
                            return 0
                    return resul
                else:
                    new = dict(  )
                    for p,m in self.__factores.items():
                        new[p] = m*exp
                    resul = self.__class__()
                    resul.__factores = new
                    return resul
        else:
            return pow( int(self), exp, mod )

    def __mod__(self,mod):
        resul = 1
        for p,m in self.__factores.items():
            resul *= pow(p,m,mod)
            if resul == 0:
                return 0
        return resul

    def __and__(self,otro):
        if otro == 1:
            if 2 in self.__factores:
                return 0
            return 1
        return int(self) & otro

    def descompocion_en_primos(self,repeticion=True):
        if repeticion:
            return itertools.chain.from_iterable(map(lambda par: itertools.repeat(par[0],par[1]),self.__factores.items()))
        return self.__factores.keys()

    def factores(self):
        resul = {1}
        for p in self.descompocion_en_primos(True):
            resul.update( [x*p for x in resul] )
        return sorted(resul)

    def factoresPropios(self):
        return self.factores()[:-1]

    def factoresPrimos(self):
        return sorted( self.descompocion_en_primos(False) )

    def factorizacion(self):
        return sorted( self.__factores.items() , key=lambda par:par[0] )

    def esPrimo(self):
        if len(self.__factores) == 1:
            p,m = list(self.__factores.items())[0]
            if m==1:
                return True
        return False

    def indicatriz(self):
        resul = 1
        for p,m in self.__factores.items():
            resul *= (p-1)*(p**(m-1))
        return resul


##    def __abs__(self):
##        return self
##
##    def __pos__(self):
##        return self
##
##    def __neg__(self):
##        return -int(self)
##    def __ceil__(self,*argv,**karg):
##        raise NotImplementedError()
##    def __floor__(self,*argv,**karg):
##        raise NotImplementedError()
##    def __floordiv__(self,*argv,**karg):
##        raise NotImplementedError()
##    def __invert__(self,*argv,**karg):
##        raise NotImplementedError()
##    def __lshift__(self,*argv,**karg):
##        raise NotImplementedError()
##    def __or__(self,*argv,**karg):
##        raise NotImplementedError()
##    def __radd__(self,*argv,**karg):
##        raise NotImplementedError()
##    def __rand__(self,*argv,**karg):
##        raise NotImplementedError()
##    def __rfloordiv__(self,*argv,**karg):
##        raise NotImplementedError()
##    def __rlshift__(self,*argv,**karg):
##        raise NotImplementedError()
##    def __rmod__(self,*argv,**karg):
##        raise NotImplementedError()
##    def __rmul__(self,*argv,**karg):
##        raise NotImplementedError()
##    def __ror__(self,*argv,**karg):
##        raise NotImplementedError()
##    def __round__(self,*argv,**karg):
##        raise NotImplementedError()
##    def __rpow__(self,*argv,**karg):
##        raise NotImplementedError()
##    def __rrshift__(self,*argv,**karg):
##        raise NotImplementedError()
##    def __rshift__(self,*argv,**karg):
##        raise NotImplementedError()
##    def __rtruediv__(self,*argv,**karg):
##        raise NotImplementedError()
##    def __rxor__(self,*argv,**karg):
##        raise NotImplementedError()
##    def __truediv__(self,*argv,**karg):
##        raise NotImplementedError()
##    def __trunc__(self,*argv,**karg):
##        raise NotImplementedError()
##    def __xor__(self,*argv,**karg):
##        raise NotImplementedError()




################################################################################
### ---------------------- Comand Line interface -------------------------------
################################################################################

__all__ = list( x for x in dir() if not (x.startswith("_") or x in __exclude_from_all__))

if __name__=="__main__" :
    import sys
    if len(sys.argv)>1:

        import argparse

        parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description='Interface de linea de comandos del Modulo de Números Naturales'
            )
        subparser = parser.add_subparsers(help="Funciones disponibles en linea de comando de este modulo")

        fun = factorial
        fun_parser = subparser.add_parser(fun.__name__,help="Factorial de numero N")
        fun_parser.add_argument(fun.__name__,type=int,metavar="N",help="Número que se desea calcular el factorial")

        fun = smallPsPF
        fun_parser = subparser.add_parser(
            fun.__name__,
            help="Calcula el Pseudo primo más pequeño desde -ini que es fuerte en -pass y falla en -fail")
        fun_parser.add_argument(fun.__name__,type=int,help="Desde donde empezar a buscar",metavar="N")
        fun_parser.add_argument("-pass",type=int,nargs="+",help="Base que apruba",metavar="N")
        fun_parser.add_argument("-fail",type=int,nargs="+",help="Base que falla",metavar="N")
        fun_parser.add_argument("-muestra",type=int,help="inda cada cuanto muetra el progreso",metavar="N")


        del fun
        argv = parser.parse_args()
        print(argv)
        aplicar = vars(argv)
        if factorial.__name__ in aplicar:
            print(factorial(aplicar[factorial.__name__]))
        if smallPsPF.__name__ in aplicar:
            print(
                smallPsPF( aplicar["pass"],aplicar["fail"],aplicar[smallPsPF.__name__],True,
                           aplicar["muestra"] if aplicar["muestra"] else 10**6
                           )
                )
    else:
        del sys
        print("<<<<<<<<<cargado módulo Naturales>>>>>>>>>")


##parser = argparse.ArgumentParser(description='Process some integers.')
##parser.add_argument('integers', metavar='N', type=int, nargs='+',
##                   help='an integer for the accumulator')
##parser.add_argument('--sum', dest='accumulate', action='store_const',
##                   const=sum, default=max,
##                   help='sum the integers (default: find the max)')
##
##args = parser.parse_args()
##print(args.accumulate(args.integers))

##>>> # create the top-level parser
##>>> parser = argparse.ArgumentParser(prog='PROG')
##>>> parser.add_argument('--foo', action='store_true', help='foo help')
##>>> subparsers = parser.add_subparsers(help='sub-command help')
##>>>
##>>> # create the parser for the "a" command
##>>> parser_a = subparsers.add_parser('a', help='a help')
##>>> parser_a.add_argument('bar', type=int, help='bar help')
##>>>
##>>> # create the parser for the "b" command
##>>> parser_b = subparsers.add_parser('b', help='b help')
##>>> parser_b.add_argument('--baz', choices='XYZ', help='baz help')
##>>>
##>>> # parse some argument lists
##>>> parser.parse_args(['a', '12'])
##Namespace(bar=12, foo=False)
##>>> parser.parse_args(['--foo', 'b', '--baz', 'Z'])
##Namespace(baz='Z', foo=True)


################################################################################
### ------------------------- Test del modulo ----------------------------------
################################################################################

