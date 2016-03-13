""" Módulo de Números Naturales

submodulo de numer especiales

"""

if __name__ == "__main__" and not __package__:
    print("idle trick")
    from relative_import_helper import relative_import_helper
    __package__ = relative_import_helper(__file__,1)
    del relative_import_helper
    
    
import numbers, collections, itertools
from functools import total_ordering


__exclude_from_all__=set(dir())

from .clasificaciones    import esPrimo, esNatural
from .generales          import productoria
from .factorizacion      import factorizacion




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


