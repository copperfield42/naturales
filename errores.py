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
        
class NoInversaModularError(ZeroDivisionError):
    """El número no tiene inversa modular"""
    pass

class NoEsAntiPrimoError(ValueError):
    """El número no cumple con las condiciones de anti-primo"""
    pass
