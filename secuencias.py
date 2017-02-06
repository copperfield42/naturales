"""
Módulo de Números Naturales, submodulo de secuencias de numeros naturales

ofrece variadad de secuencias como las secuencia de Fibonacci, y Lucas entre otras
entre funciones generadoras de las mismas y

"""

if __name__ == "__main__" and not __package__:
    from relative_import_helper import relative_import_helper
    __package__ = relative_import_helper(__file__,1)
    del relative_import_helper
    print("idle trick")

#TO DO
#hacer todas las funciones que calculan solo el n-esimo,
#tambien regresen un generador con todos los elementos

import itertools, operator

#mis modulos
import itertools_recipes

from .natural_typing       import NumOrGen, Union, Iterator, Callable, Iterable, Tuple, Matrix3x3
from .errores              import NoEsNumeroNatural, RequiereNumeroNaturalDesdeUno, NoEsAntiPrimoError
from .generales            import esNatural, esPar, productoria, num_dig, num_from_dig, num_len, ilen
from .primos               import esPrimo, mersenne_prime_base, primos
from .aritmetica_modular   import coprimos, raicesPrimitivas
from .combinatoria         import combinatorio
from .factorizacion        import factorizacion
from .clasificaciones      import esCandidatoAntiPrime


__exclude_from_all__=set(dir())

from ._secuencias  import mersenne, lucas_sequences, lucas_sequence_gen
from ._secuencias  import lucas_sequence1, lucas_sequence2, lucas_sequence2q1



################################################################################
### --------------------- Secuencias de números Naturales ----------------------
################################################################################

def seq_range(seq:Iterable[int],ini:int,fin:int,key:Callable[...,int]=None) -> Iterator[int]:
    """Regresa un generador con los elementos en seq talque
       ini <= x <= fin para los x en seq
       (se asume que seq es una secuencia creciente de números)"""
    if key:
        return itertools.dropwhile(lambda x: ini>key(x), itertools.takewhile(lambda x: key(x)<=fin,seq))
    return itertools.dropwhile(lambda x: ini>x, itertools.takewhile(lambda x: x<=fin,seq))

def numeros_primos(n:int=None) -> NumOrGen:
    """Secuencias de todos los números primos.
       Si n es suministrado calcula el n-esimo numero primo"""
    if n is None:
        return primos()
    else:
        return itertools_recipes.nth(primos(),n)

def numeros_no_primos(n:int=None) -> NumOrGen:
    """Secuencias de todos los números no primos.
       Si n es suministrado calcula el n-esimo numero no primo"""
    if n is None:
        return itertools.chain.from_iterable(
            range(a+1,b)
                for a,b in
                    itertools_recipes.pairwise(
                            itertools.chain([-1],primos())
                        )
            )
    else:
        return itertools_recipes.nth(numeros_no_primos(),n)



def fibonacci(n:int=None, m:int=None) -> NumOrGen:
    """Generador de la suceción de números de Fibonacci.
       Si n es suministrado calcula el n-esimo elemento de la suceción de Fibonacci,
       se incluye además la extención a los números negativos.
       Si m es suministrado, calcula: fib(n) mod m (para todo n)

       La sucesión de Fibonacci se define como sigue:
       fib(0)= 0
       fib(1)= 1
       fib(n)= fib(n-1) + fib(n-2), para todo n>=2

       Si n es negativo, se calcula
       fib(-n) = (-1)^(n+1) * fib(n)

       en.wikipedia.org/wiki/Fibonacci_number"""
    if n is not None:
        if n>=0:
            return lucas_sequence1(n,m,param=(1,-1))
        else:
            n = abs(n)
            fn = fibonacci(n,m)
            if m:
                return (fn*pow(-1,n+1,m))%m
            return fn*pow(-1,n+1)
    else:
        return lucas_sequence_gen(bases=(0,1),param=(1,-1),mod=m)


def lucas(n:int=None,m:int=None) -> NumOrGen:
    """Generador de la sucesión de números de Lucas.
       Si n es suministrado calcula el n-esimo elemento de la sucesión de Lucas,
       se incluye además la extención a los números negativos.
       Si m es suministrado, calcula: Ln mod m (para todo n)

       La sucesión de Lucas se define como sigue:
       lucas(0)= 2
       lucas(1)= 1
       lucas(n)= lucas(n-1) + lucas(n-2), para todo n>=2

       Si n es negativo, se calcula
       lucas(-n) = (-1)^n * lucas(n)


       en.wikipedia.org/wiki/Lucas_number"""
    if n is not None:
        if n >= 0:
            if n == 0:
                return 2 if not m else 2%m
            Lk  =  1 # L1 Lk
            Lk1 =  3 # L2 Lk+1
            sig = -1 # (-1)^k
            if m: Lk,Lk1 = Lk % m, Lk1 % m
            control = 2**(n.bit_length() -1) >> 1
            while control:
                if n & control:
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
            n = abs(n)
            Ln = lucas(n,m)
            if m:
                return (pow(-1,n,m)*Ln)%m
            return pow(-1,n)*Ln
    else:
        return lucas_sequence2(mod=m, param=(1,-1))


def pell_number(n:int=None,m:int=None) -> NumOrGen :
    """Suceción de números de Pell.
       Si n es dado calcula el n-esimo elemento de la suceción de números de Pell.
       Si m es dado calcula calcula el número correspondiente modulo m.

       La suceción de números de Pell se define como sique:
       P(0) = 0
       P(1) = 1
       P(n) = 2*P(n-1) + P(n-2)

       en.wikipedia.org/wiki/Pell_number"""
    return lucas_sequence1( n=n, mod=m, param=(2,-1) )


def jacobsthal_number(n:int=None,m:int=None) -> NumOrGen :
    """Suceción de números de Jacobsthal.
       Si n es dado calcula el n-esimo elemento de la suceción de números de Jacobsthal.
       Si m es dado calcula ese numero correspondiente modulo m.

       la suceción de números de Jacobsthal se define como sique:
       J(0) = 0
       J(1) = 1
       J(n) = J(n-1) + 2*J(n-2)

       en.wikipedia.org/wiki/Jacobsthal_number"""
    if n is None:
        return lucas_sequence1( mod=m, param=(1,-2) )
    else:
        if m is None:
            return (pow(2,n)-pow(-1,n))//3
        else:
            return lucas_sequence1(n=n, mod=m, param=(1,-2) )


def jacobsthal_lucas_number(n:int=None,m:int=None) -> NumOrGen:
    """Suceción de números de Jacobsthal-Lucas.
       Si n es suminstrado calcula el n-esimo elemento de la suceción de números de Jacobsthal-Lucas.
       Si m es dado calcula ese numero correspondiente modulo m.

       la suceción de números de Jacobsthal-lucas se define como sique:
       J(0) = 2
       J(1) = 1
       J(n) = J(n-1) + 2*J(n-2)

       en.wikipedia.org/wiki/Jacobsthal_number"""
    if n is None:
        return lucas_sequence2( mod=m, param=(1,-2) )
    else:
        JLn = pow(2,n,m) + pow(-1,n,m)
        if m is None:
            return JLn
        return JLn % m

def x_n_1(x:int, n:int=None, mod:int=None) -> NumOrGen:
    """Secuencias de números de la forma: x^n +1.
       Si n es suministrado calcula el número en cuestion.
       Si mod es suministrado calcula:  x^n +1 modulo mod"""
    if n is None:
        return lucas_sequence2(mod=mod, param=(x+1,x))
    return ( pow(x,n,mod) +1 )% mod

def repunits(size:int=None, base:int=10, mod:int=None) -> NumOrGen:
    """Números de la forma 1,11,111,1111,... en la base dada.

       https://en.wikipedia.org/wiki/Repunit"""
    result = lucas_sequence1(n=size, mod=mod, param=(base+1,base))
    if size is None:
        next(result)
    return result

def fermat_number(n:int=None, mod:int=None) -> NumOrGen :
    """Suceción de números de Fermat.
       Si n es dado calcula el n-esimo número de Fermat.
       Si mod es dado calcula: Fn modulo mod
       Los números de fermat son aquellos de la forma:
       F(n) = 2^(2^n) +1

       en.wikipedia.org/wiki/Fermat_number"""
    if mod is not None and not mod:
        raise ZeroDivisionError
    if n is None:
        def fermat(mod=None):
            F = 3
            if mod:
                F%=mod
            while True:
                yield F
                F = pow(F-1,2,mod) + 1
                if mod:
                    F%=mod
        return fermat(mod)
    if mod:
        return (pow(2,2**n,mod) +1)%mod
    return 1 + 2**(2**n)


def carmichael(n:int=None) -> NumOrGen:
    """Secuencia de los números de Carmichael.
       Si n es suministrado, calcula el n-esimo
       números de Carmichael.
       Estos son números compuestos c tales que para
       todo b en 1<b<c coprimo con c se cumple que
       b^(c-1)=1 (mod c)"""
    if n is not None:
        return itertools_recipes.nth(carmichael(),n)
    else:
        return ( c for c in itertools.count(1)
                 if not esPrimo(c) and all( pow(b,c-1,c)==1 for b in coprimos(c) )
                 )



def perfectos(n:int=None) -> NumOrGen:
    """Generador de todos los números perfectos.
       Si n es suministrado calcula el n-esimo número perfecto"""
    if n is None:
        return map( lambda p: pow(2,p-1)*(pow(2,p)-1) , mersenne_prime_base() )
    else:
        return itertools_recipes.nth(perfectos(),n)





def cullen_number(n:int=None) -> NumOrGen :
    """Suceción de números de Cullen.
       Si n es suministrado calcula el n-esimo número de Cullen.
       Estos son los números de la forma:
       C(n)=n*2^n +1

       en.wikipedia.org/wiki/Cullen_number"""
    if n is None:
        return map(lambda x: 1+ x*pow(2,x), itertools.count())
    return 1+ n*(2**n)


def leylan(n:int) -> Iterator[Tuple[int,int,int]]:
    """https://www.youtube.com/watch?v=Lsu2dIr_c8k"""
    for x in range(2,n+1):
        for y in range(2,x+1):
            yield x, y, x**y + y**x

def wilson_number() -> Iterator[int] :
    """https://en.wikipedia.org/wiki/Wilson_prime#Wilson_numbers"""
    def W(n,m):
        resul = 1
        for k in coprimos(n):
            resul = (resul*k) % m
            if resul==0:
                break
        return (resul + ( 1 if raicesPrimitivas(n) else -1 )) %m
    #print(W.__qualname__,repr(W))
    for N in itertools.count(1):
        if W(N,N**2)==0:
            yield N

def thabit_number(n:int=None) -> NumOrGen:
    """Suceción de números de Thabit.
       Si n es dado calcula el n-esimo número de Thabit.
       Estos son los numeros de la forma 3*2^n -1"""
    if n is None:
        return map(lambda x: 3 * pow(2,x) -1, itertools.count())
    return 3 * pow(2,n) -1

def stern_brocot() -> Iterator[int]:
    """Suceción de números de Stern-Brocot.
       https://www.youtube.com/watch?v=DpwUVExX27E """
    num = iter( (1,) )
    a = 1
    while True:
        yield a
        b = next(num)
        num = itertools.chain( num, (a+b,b) )
        a = b



def secuencia_de_collatz(n:int) -> Iterator[int]:
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
            n = (n//2) if esPar(n) else ( 3*n+1 )
            yield n
    else:
        raise ValueError("n debe ser mayor o igual a 1")

def numeros_cuadrados(n:int=None) -> NumOrGen :
    """Generador con todos los números que son cuadrados perfectos.
       Estos son los números de la forma n^2
       Si n es dado regresa el n-esimo número cuadrado"""
    if n is not None:
        return pow(n,2)
    else:
        return itertools.accumulate( itertools.count(), lambda sq,k: sq + 2*k-1 )

def numeros_triangulares(n:int=None) -> NumOrGen :
    """Generador de todos los números Triangulares.
       Si n es dado calcula el n-esimo número Triangular.
       Estos números cuentan cuantos puntos son necesarios
       para contruir un triangulo equilatero.
       Estos son los números de la forma (n(n+1))/2
       También es la suma de todos los números naturales hasta n

       https://en.wikipedia.org/wiki/Triangular_number"""
    if n is None:
        return itertools.accumulate(itertools.count())
    elif esNatural(n) :
        return (n*(n+1))//2
    else:
        raise NoEsNumeroNatural("El objeto no representa un número natural")

def numeros_pentagonales(n:int=None) -> NumOrGen :
    """Generador de todos los números Pentagonales.
       Si n es suministrado calcula el n-esimo número pentagonal.
       Estos son los números de la forma (3n^2 -n)/2

       https://en.wikipedia.org/wiki/Pentagonal_number"""
    if n is None:
        return map(lambda x: (3*pow(x,2)-x)//2, itertools.count(0))
    if esNatural(n):
        return (3*n**2 -n)//2
    else:
        raise NoEsNumeroNatural

def numeros_hexagonales(n:int=None) -> NumOrGen :
    """Generador de todos los números Hexagonales.
       Si n es suministrado calcula el n-esimo número hexagonal.
       Estos son los números de la forma (3n^2 -n)/2
       https://en.wikipedia.org/wiki/Hexagonal_number"""
    if n is None:
        return map(lambda x: x*(2*x-1), itertools.count() )
    if esNatural(n):
        return n*(2*n-1)
    else:
        raise NoEsNumeroNatural


def numeros_poligonales(Lados:int,n:int=None) -> NumOrGen :
    """Generador de todos los numeros poligonales del poligono corespondiente
       a la cantidad de lados solicitadas.
       Si n es suministrado calcula el n-esimo número de la secuencia.
       Estos son los números que indican la cantidad de puntos que se
       necesitan para formar poligono regular de S lados de tamaño n
       https://en.wikipedia.org/wiki/Polygonal_number"""
    if Lados <=2:
        raise ValueError("El número de lados del poligono debe ser mayor o igual a 3")
    if n is None:
        return ( ((x**2)*(Lados-2) - x*(Lados-4))//2 for x in itertools.count() )
    else:
        return ((n**2)*(Lados-2) - n*(Lados-4))//2


def simplicial_polytopic_numbers(topic:int,n:int=None) -> NumOrGen:
    """Generador de todos los números analogos a los números triangulares
       para dimenciones arbitrarias.
       Es además la topic-esima diagonal del triangulo de Pascal.
       Si n es suministrado calcula el n-esimo número de la secuencia.

       https://en.wikipedia.org/wiki/Figurate_number
       https://www.youtube.com/watch?v=2s4TqVAbfz4"""
    if topic < 0:
        raise ValueError("topic debe ser mayor o igual que 0")
    if topic == 0:
        if n is None:
            return itertools.chain([0],itertools.repeat(1))
        return 0 if n==0 else 1
    if n is None:
        return ( combinatorio(n+topic-1,topic) for n in itertools.count() )
    return combinatorio(n+topic-1,topic)



def __pitagorianTree(root:Tuple[int,int,int],matrices:Tuple[Matrix3x3,...],tope:int) -> Iterator[Tuple[int,int,int]]:
    if all( x<tope for x in root):
        yield root
        for M in matrices:
            newroot = tuple( n for n in map(lambda x:itertools_recipes.dotproduct(root,x),M))
            yield from __pitagorianTree(newroot,matrices,tope)


def pitagorian_triple(tope:int=100,primitivos:bool=True) -> Iterator[Tuple[int,int,int]]:
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

def numeros_anti_primos(n:int=None,*,num_div=True) -> Union[int,Tuple[int,int],Iterator[int],Iterator[Tuple[int,int]]]:
    """Generador de los números altamente compuestos.
       Estos son los números tales que él tiene mayor cantidad de
       divisores que todos sus predecesores.

       Si n es dado regresa el n-esimo numero de la secuencia
       Si num_div es True entrega una tupla con el número y
       la cantidad de divisores que tiene, sino entrega solo
       el numero

       https://www.youtube.com/watch?v=2JM2oImb9Qg
       https://en.wikipedia.org/wiki/Highly_composite_number"""
    if n is None:
        def nap():
            yield from ( (1,1),(2,2) ) if num_div else (1,2)
            d = 2
            for n in itertools.count(4,2):
                try:
                    dn = productoria( m+1 for p,m in esCandidatoAntiPrime(n,valor=True) )
                    if dn > d:
                        d = dn
                        yield (n,d) if num_div else n
                except NoEsAntiPrimoError:
                    pass
        return nap()
    else:
        return itertools_recipes.nth(numeros_anti_primos(num_div=num_div),n)

def _perrin(a:int,b:int,c:int,m:int=None) -> Iterator[int]:
    """Función auxiliar para generar la relacion de recurrencia
       S(0) = a
       S(1) = b
       S(2) = c
       S(n) = S(n-2) + S(n-3)"""
    if m:
        a,b,c = (x%m for x in (a,b,c))
    while True:
        yield a
        a,b,c = b,c, (a+b) if m is None else ( (a+b)%m )

def perrin(n:int=None,m:int=None) -> NumOrGen:
    """Suceción de números de Perrin.
       Si n es suministrado calcula el n-esimo elemento de la suceción de Perrin.
       Si m es suministrado, calcula: perrin(n) mod m (para todo n)

       La sucesión de Perrin se define como sigue:
       perrin(0)= 3
       perrin(1)= 0
       perrin(2)= 2
       perrin(n)= perrin(n-2) + perrin(n-3), para todo n>=3


       https://en.wikipedia.org/wiki/Perrin_number
       http://mathworld.wolfram.com/PerrinSequence.html"""
    if n is None:
        return _perrin(3,0,2,m)
    else:
        return itertools_recipes.nth(perrin(None,m),n)

def fibonorial(n:int=None,m:int=None) -> NumOrGen:
    """Fibonacci factorial

       http://mathworld.wolfram.com/Fibonorial.html
       https://en.wikipedia.org/wiki/Fibonorial"""
    if n is None:
        return itertools.accumulate(itertools.islice(fibonacci(m=m),1,None),operator.mul)
    elif esNatural(n):
        if n == 0:
            raise RequiereNumeroNaturalDesdeUno
        return itertools_recipes.nth(fibonorial(),n-1)

def leonardo(n:int=None, m:int=None ) -> NumOrGen :
    """Generador de la suceción de números de Leonardo.
       Si n es suministrado calcula el n-esimo elemento de la suceción de Leonardo.
       Si m es suministrado, calcula: Leo(n) mod m (para todo n)

       La sucesión de Leonardo se define como sigue:
       Leo(0)= 1
       Leo(1)= 1
       Leo(n)= Leo(n-1) + Leo(n-2) +1, para todo n>=2

       https://en.wikipedia.org/wiki/Leonardo_number"""
    if n is None:
        fib = fibonacci(n, m)
        next(fib)
        return ( (2*f-1) if m is None else ((2*f-1)%m) for f in fib )
    if not esNatural(n):
        raise NoEsNumeroNatural
    leo = 2*fibonacci(n+1, m)-1
    return leo if m is None else leo%m

def padovan(n:int=None, m:int=None) -> NumOrGen:
    """Generador de la suceción de números de Padovan.
       Si n es suministrado calcula el n-esimo elemento de la suceción de Padovan.
       Si m es suministrado, calcula: Pad(n) mod m (para todo n)

       La sucesión de Leonardo se define como sigue:
       Pad(0)= 1
       Pad(1)= 1
       Pad(2)= 1
       Pad(n)= Pad(n-2) + Pad(n-3), para todo n>=3

       https://en.wikipedia.org/wiki/Padovan_sequence """
    if n is None:
        return _perrin(1,1,1,m)
    else:
        return itertools_recipes.nth(perrin(None,m),n)

def kaprekar_routine(n:int, size:int=None) -> Iterator[int]:
    """https://en.wikipedia.org/wiki/6174_(number)
       https://www.youtube.com/watch?v=d8TRcZklX_Q"""
    mem = set()
    if size is None:
        size = num_len(n)
    while n not in mem:
        yield n
        mem.add(n)
        dig = list(num_dig(n))
        dig.extend( 0 for _ in range(size -len(dig)) )
        dig.sort()
        a = num_from_dig(dig)
        b = num_from_dig(reversed(dig))
        n = abs(a-b)

def repfigit_sequence(seed:int, base:int=10, mod:int=None) -> Iterator[int]:
    """Repetitive Fibonacci-like Sequence.
       https://en.wikipedia.org/wiki/Keith_number"""
    if seed>0:
        from collections import deque
        if mod:
            n = [ d%mod for d in num_dig(seed,base) ]
        else:
            n = list(num_dig(seed,base))
        nums = deque(reversed(n),maxlen=len(n))
        del n
        while True:
            yield nums[0]
            nums.append( (sum(nums)%mod) if mod else sum(nums) )

def josephus(n:int=None) -> NumOrGen:
    """https://www.youtube.com/watch?v=uCsD3ZGzMgE
       https://en.wikipedia.org/wiki/Josephus_problem"""
    if n is None:
        return map(josephus,itertools.count(1))
    if n<1:
        raise RequiereNumeroNaturalDesdeUno
    mask = ( (1<<n.bit_length()) -1 ) >> 1
    return ( (n&mask)<<1 ) | 1

##def look_and_say(inicial:int=1) -> Iterator[str]:
##    """https://en.wikipedia.org/wiki/Look-and-say_sequence"""
##    if 0<=inicial<=9:
##        say = str(inicial)
##        while True:
##            yield say
##            say = "".join( str(ilen(g))+k for k,g in itertools.groupby(say))
##            say = num_from_dig(
##                itertools.chain.from_iterable(
##                    (d,ilen(g)) for d,g in itertools.groupby(num_dig(say))
##                    )
##                )
##    else:
##        raise ValueError("El valor inicial debe ser un numero de un digito: 0..9")

__all__ = [ x for x in dir() if not (x.startswith("_") or x in __exclude_from_all__) ]
del __exclude_from_all__
