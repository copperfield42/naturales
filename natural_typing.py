"""
módulo dedicados a los tipos usados en las documentaciones de este módulo
"""

import typing, enum
from typing import Iterator, Iterable, Union, Tuple, List, TypeVar, Callable

class EnumMetaValues(type(enum.Enum)):
    def __repr__(cls):
        return "<{}: {{{}}}>".format(cls.__name__,", ".join( repr(x.value) for x in cls ) )

@enum.unique
class IntEnumValues(enum.IntEnum, metaclass=EnumMetaValues):
    """Clase para representar los valores de retorno de funciones
       que solo regresan una limitada y espesifica cantidad de valores"""
    pass

def values(*val) -> IntEnumValues  :
    """Función que crea un Enum con los valores dados"""
    name = "Values"
    know = {-1:"neg",0:"zero",1:"pos"}
    if set(val) <= {-1,0,1}:
        return IntEnumValues(name, ((know[x],x) for x in val) )
    else:
        factory = IntEnumValues if all( isinstance(x,int) for x in val ) else enum.Enum
        return factory(name,( ("val_{}".format(x),x) for x in val ) )

NumOrGen  = Union[int,Iterator[int]]
Matrix3x3 = TypeVar("Matrix3x3")
Un = TypeVar("Un(p,q)",int,int)
Vn = TypeVar("Vn(p,q)",int,int)
Vn1= TypeVar("Vn(p,1)",int,int)
