"""
Módulo de Números Naturales, submodulo de funciones generales
"""

if __name__ == "__main__" and not __package__:
    from relative_import_helper import relative_import_helper
    __package__ = relative_import_helper(__file__,1)
    del relative_import_helper
    print("idle trick")

import numbers, operator, math
from functools import reduce, wraps, partial
from decimal import Decimal, localcontext


from .natural_typing import Iterable, Union, Iterator
from .errores        import NoEsNumeroNatural, RequiereNumeroNaturalDesdeUno

__exclude_from_all__=set(dir())

def esNatural(n) -> bool:
    """Dice si el objeto representa a un número Natural: 0,1,2,3... """
    return isinstance(n,numbers.Integral) and n>=0

def esPar(n:int) -> bool:
    """Dice si n es multiplo de 2"""
    return not n&1

def esImpar(n:int) -> bool:
    """Dice si n no es multiplo de 2"""
    return not esPar(n)

def productoria(iterable:Iterable[int],*,
                start:int=1, m:int=None, zeroCheck:bool=False,
                mul=operator.mul, mod=operator.mod) -> int: #Name("value"):
    """Productoria sobre los elementos del iterable.

       Regresa el acumulado de la multiplicación de un iterable de números
       (o cualquier objeto que defina __mul__ ) de izquierda a derecha
       empesando por start que posee valor por defecto de 1.
       Por ejemplo,  productoria( [1, 2, 3, 4, 5] ) calcula (((((start*1)*2)*3)*4)*5)
       Si el iterable esta vacio, regresa start
       Si m es dado calcula la productoria mod m
       Si zeroCheck es true, calcula hasta que el primer cero sea encontrado
       y si m es dado, se trata true sin importar el valor espesificado"""
    mul_=mul
    if m is not None:
        mul_ = lambda a,b: mod(mul(a,b),m)
        zeroCheck = True
    if zeroCheck:
        for x in iterable:
            start = mul_(start,x)
            if not start:
                break
    else:
        start = reduce(mul_, iterable, start)
    return start if m is None else ( start%m )


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
        x = 2 ** sum( divmod(n.bit_length(), 2) )
        while True:
            y = (x + n // x) >> 1
            if y >= x:
                return x
            x = y
    else:
        raise NoEsNumeroNatural("El objeto no representa un número natural")

def esCuadradoPerfecto(n:int,*,valor:bool=False) -> Union[bool,int]:
    """Dice si un número es un cuadrado perfecto.
       N es cuadrado perfecto si existe un natural M tal que M^2==N

       Si valor es True, regresa el M si existe sino arroja ValueError"""
    if valor:
        raiz = isqrt(n)
        if n == raiz**2:
            return raiz
        raise ValueError("No es cuadrado perfecto")
    return n == isqrt(n)**2


def icbrt(n:int) -> int:
    """Raiz cubica entera de n."""
    #http://stackoverflow.com/questions/35254566/wrong-answer-in-spoj-cubert/35276426#35276426
    if n.bit_length() < 1024:  # float(n) safe from overflow
        a = int(round(n**(1/3.)))
        a = (2*a + n//a**2)//3  # Ensure a >= floor(cbrt(n)).
    else:
        a = 1 << -(-n.bit_length()//3)

    while True:
        d = n//a**2
        if a <= d:
            return a
        a = (2*a + d)//3


def nthroot(A, n:int,*, precision:int=None,decimales:int=None) -> Decimal:
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
            return - nthroot(-A, n, precision=precision, decimales=decimales)
    else:
        raise ValueError("El indice de la raiz debe ser mayor que 1")

def inthroot(A:int, n:int) -> int:
    """Raiz n-esima entera de A
       equivalente a floor(A**(1/n)) pero calculada enteramente con aritmetica entera"""
    #https://en.wikipedia.org/wiki/Nth_root_algorithm
    #https://en.wikipedia.org/wiki/Nth_root#nth_root_algorithm
    #http://stackoverflow.com/questions/35254566/wrong-answer-in-spoj-cubert/35276426#35276426
    #http://stackoverflow.com/questions/39560902/imprecise-results-of-logarithm-and-power-functions-in-python/39561633#39561633
    if A<0:
        if n%2 == 0:
            raise ValueError("Raiz par de un número negativo")
        return - inthroot(-A,n)
    if A==0:
        return 0
    n1 = n-1
    if A.bit_length() < 1024: # float(n) safe from overflow
        xk = round( pow(A,1.0/n) )
        xk = ( n1*xk + A//pow(xk,n1) )//n # Ensure xk >= floor(nthroot(A)).
    else:
        xk = 1 << -(-A.bit_length()//n) # 1 << sum(divmod(A.bit_length(),n))
                                        # power of 2 closer but greater than the nth root of A
    while True:
        sig = A // pow(xk,n1)
        if xk <= sig:
            return xk
        xk = ( n1*xk + sig )//n


def ln(n,*,context=None) -> Decimal:
    """Logaritmo natural de n.
       logaritmo en base e = 2.718281828459045235360287471..."""
    return Decimal(n).ln(context)

def log10(n,*,context=None) -> Decimal:
    """Logaritmo en base 10 de n"""
    return Decimal(n).log10(context)

def log(n,base,*,context=None) -> Decimal:
    """Logaritmo de n en la base dada"""
    return Decimal(n).ln(context) / Decimal(base).ln(context)

################################################################################
### ----------------------------- Decoradores ----------------------------------
################################################################################


def explote_on_none(fun=None,*,exc=ValueError, msj=None):
    """Decorador que arroja la excepcion dada si el resultado de la función es None"""
    if not fun:
        return partial(explote_on_none, exc=exc, msj=msj)
    @wraps(fun)
    def funcion(*argv,**karg):
        result = fun(*argv,**karg)
        if result is None:
            raise exc(msj)
        return result
    return funcion



################################################################################
### ------------------------------ Miselaneos ----------------------------------
################################################################################

def ilen(iterable:Iterable) -> int:
    """Cuenta la cantidad de elementos en el iterable
       Si es un Iterator/Generator el mismo es consumido"""
    try:
        return len(iterable)
    except (TypeError, OverflowError):
        pass
    return sum( 1 for _ in iterable )

def num_dig(n:int, base:int=10 ) -> Iterator[int]:
    """Generador de los digitos del número en la base dada.
       123 -> 3 2 1
       42 base=16 -> 10 2
       42 base=2  -> 0 1 0 1 0 1"""
    if n<0:
        n *= -1
    if n == 0:
        yield 0
        return
    while n:
        n,d = divmod(n,base)
        yield d

def num_from_dig(digitos:Iterable[int], base:int=10) -> int:
    """Dados los digitos del número en la base dada, reconstrulle el número que representan.
       Los digitos deben estar ordenados desde el primero al último
       [3,2,1] -> 123
       [10,2] base=16 -> 42
       [0,1,0,1,0,1], base=2 -> 42 """
    return sum( n*pow(base,i) for i,n in enumerate(digitos) if n )

def num_len(n:int, base:int=10) -> int:
    """Dice cuantos digitos tiene el número dado en la base espesificada.
       Equivalente a len(str(n)) pero sin la transformación a string"""
    if n<0:
        n*=-1
    if 0 <= n <base:
        return 1
    log = math.log10 if base==10 else (lambda x: math.log(x,base))
    estimado = math.floor( log(n) ) +1
    borde = pow(base,estimado-1)
    #print(estimado)
    if borde <= n < base*borde:
        #print("correcto")
        return estimado
    elif n<borde:
        #print("me pase")
        return estimado -1
    else:
        #print("no le llegue")
        return estimado +1
    #return ilen(num_dig(n,base))

################################################################################
### ------------------------------ Miselaneos ----------------------------------
################################################################################


def contruirNumeroCiclico(p:int,base:int=10) -> int:
    """www.youtube.com/watch?v=WUlaUalgxqI
       en.wikipedia.org/wiki/Cyclic_number

       Arroja RuntimeError en caso que no se pueda construir el número ciclico
       o ValueError en caso que las precondiciones no se cumplan

       https://en.wikipedia.org/wiki/Cyclic_number"""
    from .clasificaciones import sonCoprimos, esPrimo
    b=base
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
        raise ValueError("El contructor p del numero ciclico debe ser coprimo con la base b")

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



def revertir_numero(n:int,base:int=10) -> int:
    """Regresa el valor del número con los digitos invertidos en la base dada.
       123 -> 321, 300 -> 3 """
    if esNatural(n):
        digitos = tuple(num_dig(n,base))
        return sum( d*base**i for i,d in enumerate(reversed(digitos)) )
    else:
        raise NoEsNumeroNatural("El objeto no representa un número natural")


def glitch_number(k:int,m:int,base:int=10) -> int :
    """Son números de la forma b^k -b^m -1 con k>m>0
       estos número tiene la caracteristica de que
       por en base 10, todos sus digitos son 9
       excepto por uno de ellos que es 8

       https://www.youtube.com/watch?v=HPfAnX5blO0"""
    return base**k -base**m -1



__all__ = [ x for x in dir() if not (x.startswith("_") or x in __exclude_from_all__) ]
del __exclude_from_all__
