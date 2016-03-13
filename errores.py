""" 
Módulo de Números Naturales, submodulo que define las excepcione
"""


class NaturalError(Exception):
    """Error del modulo de números naturales"""
    pass

class NoEsNumeroNatural(ValueError):
    """El objeto no representa un número natural"""
    pass

class RequiereNumeroNaturalDesdeUno(ValueError):
    """Esta función sólo acepta números naturales mayores o iguales a 1"""
    pass
