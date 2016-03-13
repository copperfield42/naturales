""" 
Módulo de Números Naturales, submodulo de secuencias de numeros Lucas
"""

if __name__ == "__main__" and not __package__:
    print("idle trick")
    from relative_import_helper import relative_import_helper
    __package__ = relative_import_helper(__file__,1)
    del relative_import_helper


from .matriz_vector       import Matrix2x2, Vector2
from .errores             import NoEsNumeroNatural, RequiereNumeroNaturalDesdeUno

__exclude_from_all__=set(dir())

################################################################################
### --------------------- Sucesión de números de Lucas -------------------------
################################################################################
#https://en.wikipedia.org/wiki/Lucas_sequence

def sucesion_de_Lucas_Generalizada(a,b,P,Q,M=None):
    """Generador de la sucesión de Lucas generalizada con casos base a y b y parametros P y Q.
       Si M es suministrado calcula LG(n) mod M para todo n
       La sucesiones de Lucas generalizada se define como sigue:
       LG(0) = a
       LG(1) = b
       LG(n) = P*LG(n-1) - Q*LG(n-2)"""
    Ln    = a
    Lnext = b
    if M: Ln,Lnext = Ln % M, Lnext % M
    while True:
        yield Ln
        Ln,Lnext = Lnext, P*Lnext -Q*Ln if not M else (P*Lnext -Q*Ln) % M

def sucesion_de_Lucas_Generalizada_n(n,a,b,P,Q,M=None) -> int:
    """Calcula el n-esimo elemento de la sucesión de Lucas generalizada
       con casos base a y b y parametros P y Q.
       Si M es suministrado calcula LG(n) mod M
       La sucesiones de Lucas generalizada se define como sigue:
       LG(0) = a
       LG(1) = b
       LG(n) = P*LG(n-1) - Q*LG(n-2)"""
    #en.wikipedia.org/wiki/Recurrence_relation#Solving_via_linear_algebra
    if M:
        a,b = a % M, b % M
    resul = ( pow(Matrix2x2(P,-Q,1,0),n,M) * Vector2(b,a) )[1]
    return resul if not M else (resul%M)

def sucesiones_de_Lucas(n:int,P:int,Q:int,M:int=None,*,darQ=False) -> "( Un(p,q), Vn(p,q) )":
    """Calcula el n-esimo elemento de las sucesiones de Lucas de primer y segundo tipo.
       Si M es suministrado calcula: Un mod M y Vn mod M
       Si darQ es cierto, regresa en cambio ( Un(p,q), Vn(p,q), Q^n )
       que estara en modulo si M es suministrado

       Estas sucesiones se definen como sigue:
       Primer tipo
       U0(p,q) = 0
       U1(p,q) = 1
       Un(p,q) = p*Un-1(p,q) - q*Un-2(p,q) para todo n>1

       Segundo tipo
       V0(p,q) = 2
       V1(p,q) = p
       Vn(p,q) = p*Vn-1(p,q) - q*Vn-2(p,q) para todo n>1

       en.wikipedia.org/wiki/Lucas_sequence"""
    if n<0:
        raise NoEsNumeroNatural("El objeto no representa un número natural")
    if n==0:
        return (0,2) if not M else (0 , 2 % M)
    else:
        Uk  = 1  # U1  Uk
        Uk1 = P  # U2  Uk+1
        Vk  = P  # V1  Vk
        Qk  = Q  # Q^1 Q^k
        if M: Uk, Uk1, Vk, Qk = Uk % M , Uk1 % M, Vk % M, Qk % M
        control = 2**(n.bit_length()-1) >>1
        while control >0:
            if n & control == control:
                Uk1, Uk  = P*Uk1**2 -2*Q*Uk1*Uk , Uk1**2 - Q*Uk**2 # U2k+2, U2k+1
                Vk = 2*Uk1 - P*Uk                                  #        V2k+1
                Qk = Qk*Qk*Q                                       #        Q^(2k+1)
            else:
                Uk1, Uk  = Uk1**2 -Q*Uk**2 , 2*Uk1*Uk -P*Uk**2     # U2k+1, U2k
                Vk = Vk**2 -2*Qk                                   #        V2k
                Qk = Qk*Qk                                         #        Q^2k
            if M: Uk, Uk1, Vk, Qk = Uk % M , Uk1 % M, Vk % M, Qk % M
            control >>= 1
        if darQ:
            return Uk,Vk,Qk
        return Uk,Vk

def sucesion_de_lucas_primer_tipo(n:int,P:int,Q:int,M:int=None) -> "Un(p,q)":
    """Un(p,q) Da el n-esimo elemento de la sucesión de Lucas de primer tipo.
       Si M es otorgado calcula: Un(P,Q) mod M
       Esta sucesiones se define como sigue:

       U0(p,q) = 0
       U1(p,q) = 1
       Un(p,q) = p*Un-1(p,q) - q*Un-2(p,q) para todo n>1"""
    if n<0 :
        raise NoEsNumeroNatural("El objeto no representa un número natural")
    if n==0:
        return 0
    Uk  = 1  # U1 Uk
    Uk1 = P  # U2 Uk+1
    if M: Uk, Uk1 = Uk % M , Uk1 % M
    control = 2**(n.bit_length()-1) >>1
    while control >0:
        if n & control == control:
            Uk1, Uk  = P*Uk1**2 -2*Q*Uk1*Uk , Uk1**2 - Q*Uk**2 # U2k+2, U2k+1
        else:
            Uk1, Uk  = Uk1**2 -Q*Uk**2 , 2*Uk1*Uk -P*Uk**2     # U2k+1, U2k
        if M: Uk, Uk1 = Uk % M , Uk1 % M
        control >>= 1
    return Uk

def sucesion_de_lucas_segundo_tipo(n:int,P:int,Q:int,M:int=None,*,darQ=False) -> "Vn(p,q)":
    """Vn(p,q) Da el n-esimo elemento de la sucesión de Lucas de segundo tipo.
       Si M es otorgado calcula: Vn(P,Q) mod M
       Si darQ es cierto, regresa en cambio ( Vn(p,q), Q^n )
       que estaran en modulo si M es suministrado.

       Esta sucesión se define como sigue:

       V0(p,q) = 2
       V1(p,q) = p
       Vn(p,q) = p*Vn-1(p,q) - q*Vn-2(p,q) para todo n>1"""
    if n<0:
        raise NoEsNumeroNatural("El objeto no representa un número natural")
    if n==0:
        return 2 if not M else 2%M
    Vk  = P           #V1  Vk
    Qk  = Q           #Q^1 Q^k
    Vk1 = P*P -Q*2    #V2  Vk+1
    if M: Vk,Vk1,Qk = Vk % M ,Vk1 % M , Qk % M
    control = 2**(n.bit_length()-1) >>1
    while control > 0:
        if n & control == control:
            Vk  = Vk1*Vk - Qk*P   # V2k+1
            Vk1 = Vk1**2 -2*Qk*Q  # V2k+2
            Qk  = Qk*Qk*Q         # Q^(2k+1)
        else:
            Vk1 = Vk1*Vk - Qk*P   # V2k+1
            Vk  = Vk**2 -2*Qk     # V2k
            Qk  = Qk*Qk           # Q^2k
        if M: Vk,Vk1,Qk= Vk % M ,Vk1 % M , Qk % M
        control >>= 1
    if darQ:
        return Vk,Qk
    return Vk

def sucesion_de_lucas_segundo_tipo_Q1(n:int,P:int,M:int=None) -> "Vn(P,1)":
    """Calcula la sucesión de Lucas de segunda especie con parametro Q=1: Vn(P,1).
       Si M es otorgado calcula: Vn(P,1) mod M

       Estas sucesión se definen como sigue:
       V0(p,q) = 2
       V1(p,q) = p
       Vn(p,q) = p*Vn-1(p,q) - q*Vn-2(p,q) para todo n>1"""
    if n<0:
        raise NoEsNumeroNatural("El objeto no representa un número natural")
    if n==0:
        return 2 if not M else 2%M
    Vk = P        #V1 Vk
    Vk1 = P**2 -2 #V2 Vk+1
    if M: Vk,Vk1 = Vk % M ,Vk1 % M
    control = 2**(n.bit_length()-1) >>1
    while control > 0:
        if n & control == control:
            Vk  = Vk*Vk1 - P #V2k+1
            Vk1 = Vk1**2 - 2 #V2k+2
        else:
            Vk1 = Vk*Vk1 - P #V2k+1
            Vk  = Vk**2  - 2 #V2k
        if M: Vk,Vk1 = Vk % M ,Vk1 % M
        control >>= 1
    return Vk


################################################################################
### ------------------- Sucesión de números de Mersenne ------------------------
################################################################################    
    
def mersenne(n:int=None,m:int=None):
    """Secuencia de los números de Mersenne.
       Estos son los números de la forma 2^n -1
       para algun n natural.
       Si n es suministrado, calcula el n-esimo
       número de Mersenne.
       Si m es suministrado calcula el modulo de
       ese número o de toda la secuencia segun
       sea el caso"""
    if n is not None and n>=0:
        if m:
            return (pow(2,n,m)-1)%m  #sucesion_de_lucas_primer_tipo(n,3,2,m)
        return pow(2,n)-1
    return sucesion_de_Lucas_Generalizada(0,1,3,2,m)



__all__ = list( x for x in dir() if not (x.startswith("_") or x in __exclude_from_all__))
del __exclude_from_all__
