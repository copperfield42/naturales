""" 
Módulo de Números Naturales, submodulo de clasificaciones de los numeros 

"""

if __name__ == "__main__" and not __package__:
    print("idle trick")
    from relative_import_helper import relative_import_helper
    __package__ = relative_import_helper(__file__,1)
    del relative_import_helper


#from ._Naturales      import *

import numbers, itertools
from decimal import Decimal, Context#, localcontext 
#mis modulos
import itertools_recipes

from .errores             import NoEsNumeroNatural, RequiereNumeroNaturalDesdeUno
from .generales           import isqrt, contruirNumeroCiclico, productoria, log
from .generales           import nthroot, revertir_numero
from .factorizacion       import factorizacion_ds, factorizacion, factoresPropios, factores
from .generadores_primos  import primos_hasta


__exclude_from_all__=set(dir())

from .primalidad_test      import esPrimo, esPseudoprimoFuerte 
from .aritmetica_modular   import sonCoprimos, esPrimitiveRoot
from .generales            import esNatural, esCuadradoPerfecto, esPar, esImpar


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
        n = sum( x**e for x in map(int,str(n))  )
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
        return d == s
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
        #a = isqrt(n)
        a = esCuadradoPerfecto(n,valor=True)
        if a is not None:
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
        if S>1 and any( p in N for p in "2357") :
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
        #discriminate = 8*Tn +1
        #temp = isqrt(discriminate)
        temp = esCuadradoPerfecto( 8*Tn +1, valor=True )
        if temp is not None:
            if (temp-1)%2 == 0:
                return (temp-1)//2 if valor else True
    return None if valor else False

def esPentagonalNumber(Pn:int,*,valor=False) -> bool:
    """Dice si Pn es un número Pentagonal.
       Estos son los números de la forma (3n^2 -n)/2 para algun n>0
       Si valor es cierto regresa en cambio este n si exite.
       https://en.wikipedia.org/wiki/Pentagonal_number"""
    if esNatural(Pn) and Pn >0:
        #discriminate = 24*Pn +1
        #temp = isqrt(discriminate)
        temp = esCuadradoPerfecto( 24*Pn +1 , valor=True )
        if temp is not None: #temp**2 == discriminate:
            if (temp+1)%6 == 0:
                return (temp+1)//6 if valor else True
    return None if valor else False

def esHexagonalNumber(Hn:int,*,valor=False) -> bool:
    """Dice si Hn es un número Hexagonal.
       Estos son los números de la forma (5n^2 -3n)/2 para algun n>0
       Si valor es cierto regresa en cambio este n si exite.
       https://en.wikipedia.org/wiki/Hexagonal_number"""
    if esNatural(Hn) and Hn >0:
        #discriminate = 8*Hn +1
        #temp = isqrt(discriminate)
        temp = esCuadradoPerfecto( 8*Hn +1 , valor=True )
        if temp is not None: #temp**2 == discriminate:
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
        #discriminate = 8*(S-2)*Pn + (S-4)**2
        #temp = isqrt(discriminate)
        temp = esCuadradoPerfecto( 8*(S-2)*Pn + (S-4)**2 , valor=True )
        if temp is not None: #temp**2 == discriminate:
            temp += S-4
            if temp % (2*(S-2)) == 0:
                return (temp // (2*(S-2))) if valor else True
    return None if valor else False

def sonGemelos(a:int,b:int) -> bool:
    """Dice si dos números son primos gemelos
       Un número es Gemelo si ambos son primos
       y uno es 2 unidades menor o mayor que el otro"""
    return (a==b+2 or a==b-2) and esPrimo(a) and esPrimo(b)

def sonPrimosN(a:int,b:int,n:int=2):
    """Dice si a y b estan separados n unidades y son primos ambos"""
    return (a==b+n or a==b-n) and esPrimo(a) and esPrimo(b)






__all__ = list( x for x in dir() if not (x.startswith("_") or x in __exclude_from_all__))
del __exclude_from_all__