""" 
Módulo de Números Naturales, submodulo de matriz y vector 
"""

import numbers,  collections

__exclude_from_all__=set(dir())


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




__all__ = list( x for x in dir() if not (x.startswith("_") or x in __exclude_from_all__))
del __exclude_from_all__
