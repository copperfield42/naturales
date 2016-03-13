""" 
Módulo de Números Naturales, submodulo de funciones de teoria combinatoria y de conjuntos
"""

if __name__ == "__main__" and not __package__:
    print("idle trick")
    from relative_import_helper import relative_import_helper
    __package__ = relative_import_helper(__file__,1)
    del relative_import_helper

import itertools
    
from .errores   import NoEsNumeroNatural, RequiereNumeroNaturalDesdeUno
from .generales import productoria


__exclude_from_all__=set(dir())


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

        
def _fila_pascal(n:int):
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

def triangulo_pascal(n:int=None):
    """Regresa un generador cuyos elementos son generadores de las filas la n-esima
       fila del triangulo de pascal
       
       Si n es dado regresa un generador con la n-esima fila del triangulo de pascal"""
    if n is not None:
        return _fila_pascal(n) 
    return ( _fila_pascal(n) for n in itertools.count(0) )  
        
        
        
        
        
__all__ = list( x for x in dir() if not (x.startswith("_") or x in __exclude_from_all__))
del __exclude_from_all__
