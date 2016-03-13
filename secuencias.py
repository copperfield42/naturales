""" 
Módulo de Números Naturales, submodulo de secuencias de numeros naturales

ofrece variadad de secuencias como las secuencia de Fibonacci, y Lucas entre otras
entre funciones generadoras de las mismas y 

"""

if __name__ == "__main__" and not __package__:
    print("idle trick")
    from relative_import_helper import relative_import_helper
    __package__ = relative_import_helper(__file__,1)
    del relative_import_helper
#TO DO
#hacer todas las funcines que calculan solo el n-esimo, tambien regresen un generador con todos los elementos

import itertools
#mis modulos
import itertools_recipes


from .errores              import NoEsNumeroNatural, RequiereNumeroNaturalDesdeUno
from .generales            import esNatural, esPar 
from .primos               import esPrimo, mersenne_prime_base 
from .aritmetica_modular   import coprimos, raicesPrimitivas

__exclude_from_all__=set(dir())

from ._secuencias  import mersenne, sucesiones_de_Lucas
from ._secuencias  import sucesion_de_Lucas_Generalizada
from ._secuencias  import sucesion_de_Lucas_Generalizada_n
from ._secuencias  import sucesion_de_lucas_primer_tipo
from ._secuencias  import sucesion_de_lucas_segundo_tipo
from ._secuencias  import sucesion_de_lucas_segundo_tipo_Q1


################################################################################
### --------------------- Secuencias de números Naturales ----------------------
################################################################################

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

    
def leylan(n:int) -> (int,int,int):
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



def __pitagorianTree(root,matrices,tope):
    if all( x<tope for x in root):
        yield root
        for M in matrices:
            newroot = tuple( n for n in map(lambda x:itertools_recipes.dotproduct(root,x),M))
            yield from __pitagorianTree(newroot,matrices,tope)
     

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
    
    
  



__all__ = list( x for x in dir() if not (x.startswith("_") or x in __exclude_from_all__))
del __exclude_from_all__
