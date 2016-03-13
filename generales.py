""" 
Módulo de Números Naturales, submodulo de funciones generales
"""

if __name__ == "__main__" and not __package__:
    print("idle trick")
    from relative_import_helper import relative_import_helper
    __package__ = relative_import_helper(__file__,1)
    del relative_import_helper

import numbers,  collections    
from .errores  import NoEsNumeroNatural, RequiereNumeroNaturalDesdeUno
from functools import reduce
from decimal import Decimal, localcontext

class Name(object):
    def __init__(self,name):
        self.name=name
    def __repr__(self):
        return self.name


class Hint(object):
    def __init__(self,nombre):
        self.nombre=nombre
    def __getitem__(self,*param):
        print(param,type(param))
        return Name("{}[{}]".format(self.nombre,", ".join(map(self.getStr,*param))))
    def getStr(self,val):
        re=str(val)
        if re.startswith("<class '"):
            return re[8:-2]
        return re


Generator = Hint("Generator")

__exclude_from_all__=set(dir())

def esNatural(n) -> bool:
    """Dice si el objeto representa a un número Natural: 0,1,2,3... """
    return isinstance(n,numbers.Integral) and n>=0

def esPar(n:int) -> bool:
    return not n&1

def esImpar(n:int) -> bool:
    return not esPar(n)

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

def esCuadradoPerfecto(n:int,*,valor:bool=False) -> bool:
    """Dice si un número es un cuadrado perfecto.
       N es cuadrado perfecto si existe un natural M tal que M^2==N
       
       Si 'valor' es cierto entonces si
       cumple la condición regresa el M
       si sino regresa None    """
    if valor:
        raiz = isqrt(n)
        return raiz if n == raiz**2 else None
    return n == isqrt(n)**2         
        
        
        
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

   

__all__ = list( x for x in dir() if not (x.startswith("_") or x in __exclude_from_all__))
del __exclude_from_all__
