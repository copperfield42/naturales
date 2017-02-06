# -*- coding: utf-8 -*-
"""Módulo de Números Naturales


Este módulo ofrece unas series de funciones que están defenidas sobre los
números Naturales (0,1,2,3,...) como lo son pruebas de primalidad y otras
clasificaciones como números perfectos, variedad de suceciones como la de
Fibonacci y Lucas, aritmetica modular incluyendo el calculo de inversa,
máximos y minimos común divisor y multiplos, factorización en números
primos y funciones que dependen de ello como la indicatris de Euler (totient) y
el radical, factoriales y números combinatorios y de Stirling, funciones
más especialisadas como la Moebius, Carmichael, Liouville."""

version = 12

from . import errores
#from . import natural_typing
#from . import matriz_vector
#from . import numeroFactorizado
#from . import _secuencias
from . import generales
from . import combinatoria
from . import generadores_primos
from . import aritmetica_modular
from . import factorizacion
from . import primalidad_test
from . import clasificaciones
from . import primalidad_test_otros
from . import primos
from . import secuencias
from . import funciones
from .generadores_primos_sieve import sieve
from .clasificaciones import esPrimo

################################################################################
# version 4:
# -esPrimo es mas efeciente chequeando solo numero impares y descartando casos triviales
# -como resultado el calculo de números perfectos que en la version 3 que era rápido solo 7,
#  ahora es rapido hasta 8
# -factores mucho más efeciente y rapido con el uso de itertools
#
# version 5:
# -factorizacion más eficiente abandonando los itertools por una implementacion más simple
#  y más eficiente
#
# version 6:
# -esPrimo regresa a ser puramente booleano y la parte que regresaba un numero se separo
#  en la funcion primer_primo
#
# version 7:
# -Añadido el Lucas–Lehmer primality test, que permite una rapida identificación de
#  Mersenne Primes, con lo cual el calculo de numeros perfectos se aumenta hasta 15
#  en un tiempo rasonable.
# -Añadido Miller–Rabin primality test. Exacto hasta 3.317e23
#
# version 8:
# -Añadidas secuencias de Lucas de primera y segunda especie con calculo en modulo N
#  para su uso en pruebas de primalidad, y redefinidas otras secuencias en base a estas
#  para los casos que aplica como los números de Fibonnaci y Lucas
# -Miller–Rabin primality test. Exacto hasta 1.543e33
#
# version 9:
# -agregada funcion para calcular raices enesimas, logaritmos
# -Añadido PSW primality test.
# -Añadida una limitada interface de linea de comando
#
# version 10:
# -separacion en submodulos
#
# version 11:
# -añadido submodulo natural_typing para todo lo relacionado con las
#  firmas de las funciones, y actualisadas todas las firmas de funciones
#  usando este modulo
# -funciones en el submodulo de clasificaciones con parametro "valor" ahora
#  arrojan ValueError en lugar de None cuando dicho valor no existe
#
# version 12
# -añadido calculo de raices n-esimas solo con aritmetica entera
#
#
################################################################################


#__exclude_from_all__=set(dir())



        
#__all__ = [ x for x in dir() if not (x.startswith("_") or x in __exclude_from_all__) ]
#del __exclude_from_all__

##gerarquia="""
##
##
##if __name__ == "__main__" and not __package__:
##    print("idle trick")
##    from relative_import_helper import relative_import_helper
##    __package__ = relative_import_helper(__file__,1)
##    del relative_import_helper
##
##matriz_vector 
##    _secuencias
##natural_typing    
##errores 
##    _secuencias
##        primalidad_test, primalidad_test_otros
##            primos
##                secuencias
##    generales
##        combinatoria
##            primalidad_test, primalidad_test_otros
##                primos
##                    secuencias
##        generadores_primos
##            aritmetica_modular, factorizacion 
##                primalidad_test
##                    clasificaciones
##                        primalidad_test_otros
##                            primos
##                                secuencias
##                                funciones
##
##            
##-------------------------------------------------    
###aritmetica_modular.py
###combinatoria.py
###errores.py
###factorizacion.py
###generadores_primos.py
###generales.py
###matriz_vector.py
###_secuencias.py
###clasificaciones
###primalidad_test
###primalidad_test_otros
###primos.py
###secuencias.py
###funciones.py
##
##numeros.py
##
##_Naturales.py
##
##
##"""

