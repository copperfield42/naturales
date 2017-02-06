"""
Módulo de Números Naturales, submodulo de clasificaciones de los numeros

"""

if __name__ == "__main__" and not __package__:
    from relative_import_helper import relative_import_helper
    __package__ = relative_import_helper(__file__,1)
    del relative_import_helper
    print("idle trick")




import itertools
from decimal import Decimal, Context
#mis modulos
import itertools_recipes

from .natural_typing      import Union, Tuple, List
from .errores             import NoEsNumeroNatural, RequiereNumeroNaturalDesdeUno, NoEsAntiPrimoError
from .generales           import isqrt, contruirNumeroCiclico, productoria, log, num_dig, icbrt
from .generales           import inthroot, revertir_numero, explote_on_none, num_len, num_from_dig
from .factorizacion       import factorizacion_ds, factorizacion, factoresPropios, factores, factoresPrimos
from .generadores_primos  import primos_hasta, primos


__exclude_from_all__=set(dir())

from .primalidad_test      import esPrimo, esPseudoprimoFuerte
from .aritmetica_modular   import sonCoprimos, esPrimitiveRoot
from .generales            import esNatural, esCuadradoPerfecto, esPar, esImpar


def esUnaPotencia(n:int, *, valor:bool=False, verbose:bool=False, size:int=100) -> Union[bool,Tuple[int,int]]:
    """Dice si n = a^b para algun a y b naturales con b>1 (si n!=0)
       Si valor es true, regresa en cambio (a,b) si existen, tal que b es minimo,
       excepto si n es una potencia de 2 en cullo caso se regresa (2,b).

       Si verbose es cierto se mostrara cual es el b que se esta considerando.
       En el modo verbose, el valor 'a' calculado para un momento dado
       se mostrara su valor real si la cantidad de digitos en el mismo
       es menor o igual al parametro 'size' sino se mostrara una aproxiamación."""
    if n<0:
        n *= -1
    #if n == 0:
    #    return (0,1) if valor else True
    if n>3:
        if (n & (n-1) ) == 0:
            #es una potencia de 2
            if verbose:print("es una potencia de 2")
            return (2, n.bit_length()-1 ) if valor else True
        for b in primos_hasta( n.bit_length() ) : #1+round( log(2,n) )
            #solo examino raices primas, pues si no es de una de estas tampoco sera
            #de un número compuesto
            a = inthroot(n,b)
            if verbose:
                print("b=",b,"a=", +Decimal(a,Context(prec=size)) )
            if a**b == n:
                return (a,b) if valor else True
    if verbose:
        print("No esa una potencia")
    if valor:
        raise ValueError("No es una potencia.")
    return False

def esUnaPotenciaDe2(n:int, *, valor:bool=False) -> Union[bool,int]:
    """Dice si n es la forma: 2^k
       Si valor es cierto, regresa el k si existe"""
    if n>0 and n&(n-1) == 0:
        return ( n.bit_length()-1 ) if valor else True
    if valor:
        raise ValueError("No es una potencia de 2")
    return False

def esMersenneNumber(n:int,*,valor:bool=False) -> Union[bool,int]:
    """Dice si es un número de Mersenne.
       Eston son los números de la forma 2^m -1
       Si valor es True, regresa el m si existe"""
    try:
        return esUnaPotenciaDe2(n+1, valor=valor)
    except ValueError:
        pass
    if valor:
        raise ValueError("No es un número de Mersenne")
    return False

def esSemiprime(n:int, *, valor:bool=False) -> Union[bool, Tuple[int,int]]:
    """Dice si el número es la forma N = pq con p y q números primos.
       Si valor es cierto, regresa (p,q) si existen

       https://en.wikipedia.org/wiki/Semiprime"""
    root = isqrt(n)
    if root**2 == n:
        if esPrimo(root):
            return (root,root) if valor else True
        if valor:
            raise ValueError("No es un número Semiprimo, pero es un cuadrado perfecto")
        return False
    for p in primos_hasta( root+1 ):
        if n%p == 0:
            q = n//p
            if esPrimo(q):
                return (p,q) if valor else True
            else:
                break
    if valor:
        raise ValueError("No es un número Semiprimo")
    return False


def esPerfecto(n:int) -> bool:
    """Dice si un número es perfecto.
       Un número n es perfecto si la suma de todos sus factores propios es igual a n """
    if n >= 0:
        return n==sum(factoresPropios(n)) if n>0 else False
    else:
        raise NoEsNumeroNatural("El objeto no representa un número natural")

def esAbundante(n:int) -> bool:
    """Dice si un número es Abundante.
       Un número n es Abundante si la suma de sus factores propios es mayor n """
    if n >= 0 :
        if n>0:
            return n<sum(factoresPropios(n))
        else:
            raise RequiereNumeroNaturalDesdeUno("Esta función sólo acepta números naturales mayores o iguales a 1")
    else:
        raise NoEsNumeroNatural("El objeto no representa un número natural")

def esDeficiente(n:int) -> bool:
    """Dice si un número es Deficiente.
       Un número n es Deficiente si la suma de sus factores propios es menor que n """
    if n >= 0 :
        if n>0:
            return n>sum(factoresPropios(n))
        else:
            raise RequiereNumeroNaturalDesdeUno("Esta función sólo acepta números naturales mayores o iguales a 1")
    else:
        raise NoEsNumeroNatural("El objeto no representa un número natural")

def esLibreDeCuadrados(n:int) -> bool:
    """Dice si el número n es libre de cuadrados.
       Un número n es libre de cuadrados si no existe un número primo p tal que p^2 divide a n.
       Esto quiere decir que los factores primos de n son todos distintos."""
    if n>0:
        return all( m==1 for _,m in factorizacion(n) )
    return False

def esPerfectDigitalInvariant(n:int, e:int) -> bool:
    """Dice si un número es Perfect Digital Invariant (PDI).
       N es PDI si la suma cada digito en el número elevado a
       la e es igual a N."""
    if esNatural(n):
        return n == sum( pow(x,e) for x in num_dig(n) )
    else:
        raise NoEsNumeroNatural("El objeto no representa un número natural")

def esNarcisista(n:int) -> bool:
    """Dice si un número es narcisista.
       N es narcisista si la suma cada digito en el número elevado a
       la cantidad de digitos del mismo es igual a N.
       https://www.youtube.com/watch?v=4aMtJ-V26Z4"""
    return esPerfectDigitalInvariant(n, num_len(n))

def esCiclico(n:int,*,base:int=10) -> bool:
    """Dice si el número es ciclico en la base espesificada.
       www.youtube.com/watch?v=WUlaUalgxqI
       en.wikipedia.org/wiki/Cyclic_number"""
    if not esNatural(n):
        raise NoEsNumeroNatural("El objeto no representa un número natural")
    long = num_len(n)
    for i in 0,1:
        long += i
        if n *(long+1) == int("9"*long):
            try:
                return n == contruirNumeroCiclico(long+1,base)
            except (ValueError,RuntimeError):
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
        n = sum( x**e for x in num_dig(n)  )
        if verbose:
            print(n)
        if n == 1:
            return True
        if n in recuerdo:
            return False
        else:
            recuerdo.add(n)

def esMelancolico(n:int,*,e:int=2,verbose=False) -> bool:
    """Un número es melancolico si no es un número feliz"""
    return not esHappy(n,e=e,verbose=verbose)

@explote_on_none(msj="El número no es un Vampiro")
def esVampiro(n:int,*,valor:bool=False) -> Union[ bool, Tuple[Tuple[int,int],...] ]:
    """Dice si un número es un vampiro.
       Si valor es True, regresa los colmillos del vampiro si existen.
       www.youtube.com/watch?v=3ZMnVd4ivKQ
       en.wikipedia.org/wiki/Vampire_number"""
    if n<1000:
        return False if not valor else None
    nstr = sorted(num_dig(n))# type: List[int]
    if len(nstr)%2==0:
        factor_len = len(nstr) // 2
        temp1 = ( x for x in factores(n) if factor_len == num_len(x) ) # type: Iterable[int]
        temp2 = ( c for c in itertools.combinations(temp1,2)           # temp2 type: Iterable[ Tuple[int,int] ]
                  if n == productoria( c )
                  and 1 >= sum( not z%10 for z in c )
                  and nstr == sorted( itertools.chain.from_iterable(map(num_dig,c) ) )
                 )
        if valor:
            result = tuple(temp2)
            return result if result else None
        return bool(next(temp2,False))
    if not valor:
        return False

def esExtraño(n:int) -> int:
    """Dice si un número es extraño.
       Los números extraños son números abundantes, tales
       que ningun subconjuto de los divisores propios de n
       sume igual a n

       https://en.wikipedia.org/wiki/Weird_number"""
    fact = tuple(factoresPropios(n))
    if n<sum(fact):
        return not any( n == sum(sub) for sub in itertools_recipes.powerset(fact) )
    else:
        return False

def esProthNumber(n:int,*,valor:bool=False) -> Union[bool,Tuple[int,int] ]:
    """Dice si es un número de Proth.
       Estos son los números de la forma:
       k*2^m +1 donde k es impar y 0<k<2^m

       Si valor es True, regresa una tupla con (k,m) si existen

       en.wikipedia.org/wiki/Proth_number"""
    if n&1 and n>1:
        k,m = factorizacion_ds(n)
        if k<2**m:
            return (k,m) if valor else True
    if valor:
        raise ValueError("No es un n+umero de Proth.")
    return False

@explote_on_none(msj="No es un número de Cullen")
def esCullenNumber(n:int,*,valor:bool=False) -> Union[bool,int]:
    """Dice si es número de Cullen.
       Estos son los números de la forma:
       m*2^m +1  para algun m natural

       Si valor es True, regresa el m si existe

       en.wikipedia.org/wiki/Cullen_number"""
    if esImpar(n):
        d,s = factorizacion_ds(n)
        if valor:
            return d if d==s else None
        return d == s
    else:
        return None if valor else False

def esFermatNumber(n:int,*,valor:bool=False) -> Union[bool,int]:
    """Dice si es un número de Fermat.
       Estos son los números de la forma
       2^(2^m) +1 para algun m natural.

       Si valor es True, regresa el m si existe"""
    if n>2 and esImpar(n):
        try:
            return esUnaPotenciaDe2(esUnaPotenciaDe2(n-1,valor=True),valor=valor)
        except ValueError:
            pass
    if valor:
        raise ValueError("No es un número de Fermat")
    return False

def esSphenicNumber(n:int,*,valor:bool=False) -> Union[bool,Tuple[int,int,int] ]:
    """Dice si es un número de Sphenic.
       Estos son los números tales que tienen exactamente 3 factores primos distintos
       con multiplicidad 1 cada uno.

       Si valor es True, regresa una tupla con esos factores si existen

       https://en.wikipedia.org/wiki/Sphenic_number"""
    facto = tuple(factorizacion(n))
    if len(facto) == 3:
        if all( m == 1 for p,m in facto):
            return tuple( p for p,m in facto) if valor else True
    if valor:
        raise ValueError("No es un número de Sphenio")
    return False

__golden_ratio = Decimal("1.61803398874989484820458683436563811772030917980576286213544862270526046281890244970720720418939113748475")
#https://oeis.org/A001622

def esFibonacciNumber(n:int,*,valor:bool=False) -> Union[bool,int]:
    """Dice si n es número de la secuencia de Fibbocci.
       Si valor es True, regresa el indice de ese número en la secuencia
       si él mismo pertenece a ella"""
    #en.wikipedia.org/wiki/Fibonacci_number#Recognizing_Fibonacci_numbers
    temp = 5*(n**2)
    if valor:
        sig = None
        if esCuadradoPerfecto( temp +4 ):
            sig =  1
        elif esCuadradoPerfecto( temp -4 ):
            sig = -1
        if sig:
            return round(log( (n*Decimal(5).sqrt() + Decimal(5*n**2 +sig*4).sqrt())/2, __golden_ratio) )
        else:
            raise ValueError("No es un número de Fibonacci")
    else:
        return esCuadradoPerfecto( temp +4 ) or esCuadradoPerfecto( temp-4 )

def esCuboPerfecto(n:int,*,valor:bool=False) -> Union[bool,int]:
    """Dice si un número es un cubo perfecto.
       N es cubo perfecto si existe un natural M tal que M^3==N

       Si valor es True, regresa el M si existe sino arroja ValueError"""
    if valor:
        raiz = icbrt(n)
        if n == raiz**3:
            return raiz
        raise ValueError("No es cubo perfecto")
    return n == icbrt(n)**3

def esPotenciaPerfecta(x:int, n:int,*,valor:bool=False) -> Union[int,bool]:
    """Dice si un número x es una potencia perfecta de n.
       X es una potencia perfecta de N si existe un natural M tal que M^N==X

       Si valor es True, regresa el M si existe sino arroja ValueError"""
    if valor:
        raiz = inthroot(x,n)
        if raiz**n == x:
            return raiz
        raise ValueError("No es un potencia perfecta de {}".format(n))
    return inthroot(x,n)**n == x



def esThabitNumber(n,*,valor=False) -> Union[bool,int]:
    """Dice si n es un número de Thabit.
       Los números de Thabit son los números
       de la forma 3*2^k -1 para algun k>=0
       Si valor es True, regresa ese k si existe
       sino regresa None.

       https://en.wikipedia.org/wiki/Thabit_number"""
    if n == 2:
        return 0 if valor else True
    elif esImpar(n) and n>2:
        d,s = factorizacion_ds(n+1)
        if d == 3:
            return s if valor else True
    if valor:
        raise ValueError("No es un número de Thabit")
    return False


def esDeletablePrime(n,*,valor=False) -> Union[bool, Tuple[ Tuple[int,...] ] ]:
    """Dice si el número es un Deletable Prime.
       Un deletable prime es un número tal que si
       eliminando 1 digito cualquiera del mismo
       el resultado es primo, y esto se mantiene
       hasta llegar a un primo de un solo dijito.

       Si valor es True, regresa una tupla con todos
       los posibles caminos que cumplan la condición
       o una tupla vacia sino exite tal camino o no es
       primo"""
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

def esGlitchNumber(n,base=10,*,valor=False,verbose=False) -> Union[bool,Tuple[int,int]]:
    """Son números de la forma b^k -b^m -1 con k>m>0
       estos número tiene la caracteristica de que
       por ejemplo en base 10, todos sus digitos son 9
       excepto por uno de ellos que es 8

       Si valor es True, regresa una tupla con (k,m) si existen

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
    if valor:
        raise ValueError("No es un Glitch number")
    return False

def esPalindromo(n:int,base:int=10) -> bool:
    """Dice si el número dado es palindromo en la base dada"""
    return n == revertir_numero(n,base)

def esPalindromoAlado(n:int,base:int=10) -> bool:
    """Un palindromo alado es un número palindromo de esta forma
       xxxxxMxxxxx con M y x diferentes"""
    if esPalindromo(n):
        num = str(n)
        tam = len(num)
        if tam%2==1 and len(set(num)) == 2:
            middle = num[tam//2]
            if 1 == num.count(middle):
                return True #len( set( num.replace( num[tam//2], "" ) ) ) == 1
    return False

def esTriangularNumber(Tn:int,*,valor:bool=False) -> Union[bool,int]:
    """Dice si Tn es un número Triangular.
       Estos son los números de la forma (n(n+1))/2 para algun n>=0

       Si valor es True, regresa el n si existe

       https://en.wikipedia.org/wiki/Triangular_number"""
    if esNatural(Tn) :
        #discriminate = 8*Tn +1
        #temp = isqrt(discriminate)
        try:
            temp = esCuadradoPerfecto( 8*Tn +1, valor=True ) - 1
            if temp%2 == 0:
                return (temp//2) if valor else True
        except ValueError:
            pass
    if valor:
        raise ValueError("No es un número Triangular")
    return False

def esPentagonalNumber(Pn:int,*,valor:bool=False) -> Union[bool,int]:
    """Dice si Pn es un número Pentagonal.
       Estos son los números de la forma (3n^2 -n)/2 para algun n>=0

       Si valor es True, regresa el n si existe

       https://en.wikipedia.org/wiki/Pentagonal_number"""
    if esNatural(Pn):# and Pn >0:
        if Pn == 0:
            return 0 if valor else True
        #discriminate = 24*Pn +1
        #temp = isqrt(discriminate)
        try:
            temp = esCuadradoPerfecto( 24*Pn +1 , valor=True )
            if (temp+1)%6 == 0:
                return (temp+1)//6 if valor else True
        except ValueError:
            pass
    if valor:
        raise ValueError("No es un número Pentagonal")
    return False

def esHexagonalNumber(Hn:int,*,valor:bool=False) -> Union[bool,int]:
    """Dice si Hn es un número Hexagonal.
       Estos son los números de la forma (5n^2 -3n)/2 para algun n>=0

       Si valor es True, regresa el n si existe

       https://en.wikipedia.org/wiki/Hexagonal_number"""
    if esNatural(Hn):
        if Hn == 0:
            return 0 if valor else True
        #discriminate = 8*Hn +1
        #temp = isqrt(discriminate)
        try:
            temp = esCuadradoPerfecto( 8*Hn +1 , valor=True ) + 1
            if temp%4==0:
                return (temp//4) if valor else True
        except ValueError:
            pass
    if valor:
        raise ValueError("No es un número Hexagonal")
    return False

def esPolygonalNumber(Pn:int,S:int,*,valor:bool=False) -> Union[bool,int]:
    """Dice si Pn es un S-gonal númber.
       Pn es un S-gonal númber si se puede poner esa cantidad
       de puntos formando un poligono regular de S lados.

       Si valor es True, regresa el indice de ese número en la
       secuencias de numeros S-gonales si existe

       https://en.wikipedia.org/wiki/Polygonal_number"""
    if not (esNatural(S) and S>2):
        raise ValueError("El número de lados del poligono debe ser mayor o igual a 3")
    if esNatural(Pn):
        if Pn == 0:
            return 0 if valor else True
        #discriminate = 8*(S-2)*Pn + (S-4)**2
        #temp = isqrt(discriminate)
        try:
            temp = esCuadradoPerfecto( 8*(S-2)*Pn + (S-4)**2 , valor=True )
            temp += S-4
            if temp % (2*(S-2)) == 0:
                return ( temp // (2*(S-2)) ) if valor else True
        except ValueError:
            pass
    if valor:
        raise ValueError("No es un numero S-gonal")
    return False


def esCandidatoAntiPrime(n:int,*,valor:bool=False) -> Union[bool, List[Tuple[int,int]] ]:
    """Dice si el número es candidato a anti-primo.
       Si valor es True, se regresa una lista con la factorización
       de n y se verifica que cumpla las condiciones de un número
       anti-primo, y si no los las cumple arroja NoEsAntiPrimoError

       Los números anti-primos tiene las siguientes propiedades
       en relación a su factorizacion:
       1)su factorización es de primos consecutivos
       2)las multiplicidades de los primos en su factorización
         es decreciente (desde el menor primo)
       3)la multiplicidad del ultimo/mayor primo es 1, excepto por
         los numeros 4 y 36

       https://en.wikipedia.org/wiki/Highly_composite_numbers
       https://www.youtube.com/watch?v=2JM2oImb9Qg  """
    if n in {4,36}:
        if not valor:
            return True
        return [(2,2)] if n==4 else [(2,2),(3,2)]
    fac = None
    for p in primos():
        if n%p == 0:
            m = 0
            while n%p == 0:
                m += 1
                n //= p
            if fac:
                if fac[-1][-1] >= m:
                    fac.append( (p,m) )
                else:
                    if valor:
                        raise NoEsAntiPrimoError
                    return False
            else:
                fac = [(p,m)]
        else:
            if valor:
                raise NoEsAntiPrimoError
            return False
        if n==1:
            if 1 == fac[-1][-1]:
                return fac if valor else bool(fac)
            else:
                if valor:
                    raise NoEsAntiPrimoError
                return False


def esKaprekarNumber(X:int,base:int=10,*,valor:bool=False) -> Union[bool,Tuple[int,int,int] ] :
    """Dice si un número X en la base dada es un número de Kaprekar.
       X es un número de Kaplekar en la base b si existen números
       n,A y B  que satisfacen:

       X^2 = Ab^n + B donde 0 < B < b^n
       X   = A+B

       Si valor es True, regresa en cambio (n,A,B) si existen

       https://en.wikipedia.org/wiki/Kaprekar_number"""
    if X>0:
        if X==1:
            if valor:
                return (0,0,1)
            return True
        dig = tuple( num_dig(X**2, base=base) )
        for i in range(1,len(dig)):
            A = num_from_dig(dig[i:], base=base)
            B = num_from_dig(dig[:i], base=base)
            if A and B and X==A+B:
                if valor:
                    #print("calculando valor")
                    bn,n = divmod((X**2 - B),A)
                    if not n and 0<B<bn:
                        while not bn%base:
                            n+=1
                            bn //= base
                        if bn>1:
                            #print("no salio a la primera")
                            continue
                        return n,A,B
                return True
    if valor:
        raise ValueError("No es un número de Kaprekar en la base {}".format(base))
    return False


def esSmithNumber(n:int) -> bool:
    """Dice si es un número de Smith.
       Los números de Smith son los números compuestos tales que la suma de sus digitos
       es igual a la suma de los digitos sus factores primos

       https://www.youtube.com/watch?v=mlqAvhjxAjo
       https://en.wikipedia.org/wiki/Smith_number
       """
    if n>0 and not esPrimo(n):
        return sum(num_dig(n)) == sum( m*sum(num_dig(p)) for p,m in factorizacion(n))
    return False

def esHarshadNumber(n:int, base:int=10) -> bool:
    """Dice si n es un número de Harshad en la base dada.
       Los números de Harshad son aquellos que son divisible por
       la suma de sus digitos.

       https://en.wikipedia.org/wiki/Harshad_number
       https://www.youtube.com/watch?v=D6tINlNluuY
       """
    return n%sum(num_dig(n,base)) == 0

def esPrimaryPseudoperfectNumber(n:int) -> bool:
    """Dice si el número es un Primario Pseudo Perfecto.
       Estos son los números tales que las suma del inverso
       del mismo con sus factores primos es 1

       https://en.wikipedia.org/wiki/Primary_pseudoperfect_number
       https://www.youtube.com/watch?v=D6tINlNluuY """
    if n>1:
        from fractions import Fraction as F
        return 1 == F(1,n) + sum( F(1,p) for p in factoresPrimos(n) )
    return False

def esPronicNumber(pr:int, *, valor:bool=False) -> Union[bool,Tuple[int,int]]:
    """Dice si el número es un numero de Pronic.
       Estos son los números tales que son el producto de dos
       números consecutivos, es decir es de la forma n(n+1)
       para algún n.
       Si valor es cierto regresa (n,n+1) si existen

       https://en.wikipedia.org/wiki/Pronic_number
       https://www.youtube.com/watch?v=D6tINlNluuY"""
    if valor:
        if pr%2==0:
            try:
                a = esTriangularNumber(pr//2, valor=True)
                return a, a+1
            except ValueError:
                pass
        raise ValueError("No es un número de Pronic")
    return esTriangularNumber(pr//2) if pr%2==0 else False

def esFactorial(F:int, *, valor:bool=False) -> Union[bool, int]:
    """Dice si F es de la forma F = n! para algun n.
       Si valor es True, regresa el n si existe."""
    if F>0:
        if F in {1,2}:
            return F if valor else True
        if F%2 == 0:
            for n in itertools.count(2):
                if F%n == 0:
                    F //= n
                    if F==1:
                        return n if valor else True
                else:
                    break
    if valor:
        raise ValueError("No es un Factorial")
    return False

def esKeithNumber(n:int, base:int=10) -> bool:
    """https://www.youtube.com/watch?v=uuMwz47LV_w
       https://en.wikipedia.org/wiki/Keith_number"""
    if n>base:
        from .secuencias import repfigit_sequence
        return n in itertools.takewhile(lambda x: x<=n, repfigit_sequence(n,base))
    return False
    

def sonGemelos(a:int,b:int) -> bool:
    """Dice si dos números son primos gemelos
       Un número es Gemelo si ambos son primos
       y uno es 2 unidades menor o mayor que el otro"""
    return (a==b+2 or a==b-2) and esPrimo(a) and esPrimo(b)

def sonPrimosN(a:int,b:int,n:int=2) -> bool:
    """Dice si a y b estan separados n unidades y son primos ambos"""
    return (a==b+n or a==b-n) and esPrimo(a) and esPrimo(b)

def sonAmigables(a:int, b:int) -> bool:
    """Dice si los números son amigables
       Dos números son amigables si la suma de sus factores propios
       es igual al otro número
       https://www.youtube.com/watch?v=fUSZBVYZdKY"""
    return a==sum(factoresPropios(b)) and b==sum(factoresPropios(a))

def _aplicarTodas(n:int):
    func = [name for name in __all__ if name.startswith("es")]
    glob = globals()
    for fun in func:
        #print(fun, glob[fun])
        try:
            if glob[fun](n):
                print(fun)
        except TypeError:
            pass

__all__ = [ x for x in dir() if not (x.startswith("_") or x in __exclude_from_all__) ]
del __exclude_from_all__
