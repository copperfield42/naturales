"""
Módulo de Números Naturales, submodulo de matriz y vector
"""

import numbers, collections
from numbers import Number

__all__ = ["Vector2", "Matrix2x2"]


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
        if isinstance(otro, Number):
            x,y = self
            return self.__class__(x*otro,y*otro)
        if isinstance(otro, self.__class__):#producto punto
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

    @classmethod
    def identidad(cls):
        """Regresa la matriz identidad"""
        return cls(1,0,0,1)

    def __add__(self,otro):
        if isinstance(otro,self.__class__):
            #x,y,z,w = self
            #a,b,c,d = otro
            return self.__class__(*map(sum,self,otro))  #(x+a, y+b, z+c, w+d)
        else:
            return NotImplemented

    def __mul__(self,otro):
        if isinstance(otro,self.__class__):
            x,y,z,w = self
            a,b,c,d = otro
            return self.__class__( x*a+y*c , x*b+y*d, z*a+w*c, z*b+w*d )
        if isinstance(otro,Number):
            #x,y,z,w = self
            return self.__class__( *(e*otro for e in self) )   #(x*otro, y*otro, z*otro, w*otro)
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


    def __pow__(self, n:int, M:int=None):
        #https://en.wikipedia.org/wiki/Exponentiation_by_squaring
        if not isinstance(n, numbers.Integral):
            return NotImplemented
        if n<0:
            raise NotImplementedError("No se ha implementado el calculo de inversa de esta matriz")
        #n = int(n)
        if M is not None and not M:
            raise ZeroDivisionError
        if n==0:
            I = self.identidad()
            return (I%M) if M else I
        if n==1:
            return (self%M) if M else self
        x = (self%M) if M else self
        y = self.identidad()
        while n>1:
            if n&1: #if n es impar
                y = y*x
                if M: y = y%M
            x = x*x
            if M:
                x = x%M
            n >>= 1
        x = x*y
        return (x%M) if M else x

    def __mod__(self,mod:int):
        #x,y,z,w = self
        return self.__class__( *(e%mod for e in self) )   #(x%mod, y%mod, z%mod, w%mod)

    def __bool__(self):
        return any(self)

    def determinante(self):
        a,b,c,d = self
        return a*d - b*c

    def __str__(self):
        return "|{} {}|\n|{} {}|".format(*self)


