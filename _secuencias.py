"""
Módulo de Números Naturales, submodulo de secuencias de números de Lucas
"""

if __name__ == "__main__" and not __package__:
    from relative_import_helper import relative_import_helper
    __package__ = relative_import_helper(__file__,1)
    del relative_import_helper
    print("idle trick")


from .natural_typing      import Iterator, Tuple, Union, Un, Vn, Vn1, NumOrGen
from .matriz_vector       import Matrix2x2, Vector2
from .errores             import NoEsNumeroNatural, RequiereNumeroNaturalDesdeUno

__exclude_from_all__=set(dir())

################################################################################
### --------------------- Sucesión de números de Lucas -------------------------
################################################################################
#https://en.wikipedia.org/wiki/Lucas_sequence

def sucesion_de_Lucas_Generalizada(a:int,b:int,P:int,
                                   Q:int,M:int=None) -> Iterator[int]:
    """Generador de la sucesión de Lucas generalizada con casos base a y b y
       parametros P y Q.
       Si M es suministrado calcula LG(n) mod M para todo n
       La sucesiones de Lucas generalizada se define como sigue:
       LG(0) = a
       LG(1) = b
       LG(n) = P*LG(n-1) - Q*LG(n-2)

       en.wikipedia.org/wiki/Lucas_sequence"""
    Ln    = a
    Lnext = b
    if M: Ln,Lnext = Ln % M, Lnext % M
    while True:
        yield Ln
        Ln,Lnext = Lnext, (P*Lnext -Q*Ln) if not M else (P*Lnext -Q*Ln) % M

def sucesion_de_Lucas_Generalizada_n(n:int, a:int, b:int,
                                     P:int, Q:int, M:int=None) -> int:
    """Calcula el n-esimo elemento de la sucesión de Lucas generalizada
       con casos base a y b y parametros P y Q.
       Si M es suministrado calcula LG(n) mod M
       La sucesiones de Lucas generalizada se define como sigue:
       LG(0) = a
       LG(1) = b
       LG(n) = P*LG(n-1) - Q*LG(n-2)

       en.wikipedia.org/wiki/Lucas_sequence"""
    #en.wikipedia.org/wiki/Recurrence_relation#Solving_via_linear_algebra
    if M:
        a,b = a % M, b % M
    resul = ( pow(Matrix2x2(P,-Q,1,0),n,M) * Vector2(b,a) )[1]
    return resul if not M else (resul%M)

def lucas_sequence_gen(n:int=None, mod:int=None, *,
                       bases:Tuple[int,int], param:Tuple[int,int]
                       ) -> NumOrGen:
    """LSG([n][,mod],*,bases:(a, b),param:(P, Q)) -> Union[int, Iterator[int]]
       Calcula los elementos de la Secuencia de lucas generalisada con casos
       bases a y b y parametros P y Q.
       Si n es suministrado se calcula el n-esimo elemento de la secuencia.
       Si mod es nuministrado calcula: LSG(n) modulo mod

       La secuencia de Lucas Generalizada se define como:

       LSG(0) = a
       LSG(1) = b
       LSG(n) = P*LSG(n-1) - Q*LSG(n-2)

       en.wikipedia.org/wiki/Lucas_sequence
       """
    a,b = bases
    P,Q = param
    if n is None:
        return sucesion_de_Lucas_Generalizada(a,b,P,Q,mod)
    return sucesion_de_Lucas_Generalizada_n(n,a,b,P,Q,mod)

def lucas_sequences_n(n:int, P:int, Q:int, M:int=None,
                    *,darQ:bool=False) -> Union[Tuple[Un,Vn],Tuple[Un,Vn,int]]:
    """Calcula el n-esimo elemento de las sucesiones de Lucas de primer
       y segundo tipo.
       Si M es suministrado calcula: Un mod M y Vn mod M
       Si darQ es cierto, regresa en cambio ( Un(p,q), Vn(p,q), Q^n )
       que estaran en modulo si M es suministrado

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
        while control:
            if n & control:
                Uk1, Uk  = P*pow(Uk1,2,M) -2*Q*Uk1*Uk , pow(Uk1,2,M) - Q*pow(Uk,2,M) # U2k+2, U2k+1
                Vk = 2*Uk1 - P*Uk                                                    #        V2k+1
                Qk = pow(Qk,2,M)*Q                                                   #        Q^(2k+1)
            else:
                Uk1, Uk  = pow(Uk1,2,M) -Q*pow(Uk,2,M) , 2*Uk1*Uk -P*pow(Uk,2,M)     # U2k+1, U2k
                Vk = pow(Vk,2,M) -2*Qk                                               #        V2k
                Qk = pow(Qk,2,M)                                                     #        Q^2k
            if M: Uk, Uk1, Vk, Qk = Uk % M , Uk1 % M, Vk % M, Qk % M
            control >>= 1
        if darQ:
            return Uk,Vk,Qk
        return Uk,Vk

sucesiones_de_Lucas = lucas_sequences_n

def lucas_sequences(n:int=None, mod:int=None, *, param:Tuple[int,int]) -> Union[ Tuple[Un,Vn], Iterator[Tuple[Un,Vn]] ] :
    """LS([n][,mod],*,param:(P, Q))
       Calcula los elemento de las sucesiones de Lucas de primer y segundo tipo.
       Si n es suministrado calcula el n-esimo elemento de la secuencia.
       Si mod es suministrado calcula: Un(p,q) modulo mod, Vn(p,q) modulo mod


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
    p = param[0]
    if n is None:
        return zip( lucas_sequence_gen(mod=mod, bases=(0,1), param=param),
                    lucas_sequence_gen(mod=mod, bases=(2,p), param=param)
                    )
    return lucas_sequences_n(n=n, M=mod, P=p, Q=param[1] )


def lucas_sequence1n(n:int, P:int, Q:int, M:int=None) -> Un:
    """Un(p,q) Da el n-esimo elemento de la sucesión de Lucas de primer tipo.
       Si M es otorgado calcula: Un(P,Q) mod M
       Esta sucesiones se define como sigue:

       U0(p,q) = 0
       U1(p,q) = 1
       Un(p,q) = p*Un-1(p,q) - q*Un-2(p,q) para todo n>1

       en.wikipedia.org/wiki/Lucas_sequence"""
    if n<0 :
        raise NoEsNumeroNatural("El objeto no representa un número natural")
    if n==0:
        return 0
    Uk  = 1  # U1 Uk
    Uk1 = P  # U2 Uk+1
    if M: Uk, Uk1, P = Uk % M , Uk1 % M, P % M
    control = 2**(n.bit_length()-1) >>1
    while control:
        if n & control:
            Uk1, Uk  = P*pow(Uk1,2,M) -2*Q*Uk1*Uk , pow(Uk1,2,M) - Q*pow(Uk,2,M) # U2k+2, U2k+1
        else:
            Uk1, Uk  = pow(Uk1,2,M) - Q*pow(Uk,2,M) , 2*Uk1*Uk - P*pow(Uk,2,M)   # U2k+1, U2k
        if M: Uk, Uk1 = Uk % M , Uk1 % M
        control >>= 1
    return Uk

sucesion_de_lucas_primer_tipo = lucas_sequence1n

def lucas_sequence1(n:int=None, mod:int=None,*, param:Tuple[int,int]) -> Union[Un, Iterator[Un]]:
    """Un(p,q) Calcula los elementos de la secuancia de lucas de primer tipo.
       Si n es suministrado calcula el n-esimo elemento de la secuencia.
       Si mod es otorgado calcula: Un(P,Q) modulo mod.
       param debe ser una tupla de la forma (p,q).

       Esta sucesiones se define como sigue:

       U0(p,q) = 0
       U1(p,q) = 1
       Un(p,q) = p*Un-1(p,q) - q*Un-2(p,q) para todo n>1

       en.wikipedia.org/wiki/Lucas_sequence"""
    if n is None:
        return lucas_sequence_gen(mod=mod, bases=(0,1), param=param)
    P,Q=param
    return lucas_sequence1n(n=n, P=P, Q=Q, M=mod)




def lucas_sequence2n(n:int,P:int,Q:int,M:int=None,*,darQ:bool=False) -> Vn:
    """Vn(p,q) Da el n-esimo elemento de la sucesión de Lucas de segundo tipo.
       Si M es otorgado calcula: Vn(P,Q) mod M
       Si darQ es cierto, regresa en cambio ( Vn(p,q), Q^n )
       que estaran en modulo si M es suministrado.

       Esta sucesión se define como sigue:

       V0(p,q) = 2
       V1(p,q) = p
       Vn(p,q) = p*Vn-1(p,q) - q*Vn-2(p,q) para todo n>1

       en.wikipedia.org/wiki/Lucas_sequence"""
    if n<0:
        raise NoEsNumeroNatural("El objeto no representa un número natural")
    if n==0:
        return 2 if not M else 2%M
    Vk  = P                  #V1  Vk
    Qk  = Q                  #Q^1 Q^k
    Vk1 = pow(P,2,M) -2*Qk   #V2  V2k
    if M: Vk, Vk1, Qk, P = Vk % M ,Vk1 % M , Qk % M, P % M
    control = 2**(n.bit_length()-1) >>1
    while control:
        if n & control:
            Vk  = Vk1*Vk - Qk*P         # V2k+1
            Vk1 = pow(Vk1,2,M) -2*Qk*Q  # V2k+2
            Qk  = pow(Qk,2,M)*Q         # Q^(2k+1)
        else:
            Vk1 = Vk1*Vk - Qk*P         # V2k+1
            Vk  = pow(Vk,2,M) -2*Qk     # V2k
            Qk  = pow(Qk,2,M)           # Q^2k
        if M: Vk,Vk1,Qk= Vk % M ,Vk1 % M , Qk % M
        control >>= 1
    if darQ:
        return Vk,Qk
    return Vk

sucesion_de_lucas_segundo_tipo = lucas_sequence2n

def lucas_sequence2(n:int=None, mod:int=None, *, param:Tuple[int,int]) -> Union[ Vn, Iterator[Vn]]:
    """Vn(p,q) Calcula los elementos de la secuancia de lucas de segundo tipo.
       Si n es suministrado calcula el n-esimo elemento de la secuencia.
       Si mod es otorgado calcula: Vn(P,Q) modulo mod.
       param debe ser una tupla de la forma (p,q).

       Esta sucesiones se define como sigue:

       V0(p,q) = 2
       V1(p,q) = p
       Vn(p,q) = p*Vn-1(p,q) - q*Vn-2(p,q) para todo n>1

       en.wikipedia.org/wiki/Lucas_sequence"""
    P,Q=param
    if n is None:
        return lucas_sequence_gen(mod=mod, bases=(2,P), param=param)
    return lucas_sequence2n(n=n, P=P, Q=Q, M=mod)

def lucas_sequence2q1n(n:int,P:int,M:int=None) -> Vn1:
    """Calcula el n-esimo elemento de la secuenci de Lucas de segunda especie
       con parametro P y Q=1: Vn(P,1).
       Si M es otorgado calcula: Vn(P,1) mod M

       Esta sucesión se definen como sigue:
       V0(p) = 2
       V1(p) = p
       Vn(p) = p*Vn-1(p) - Vn-2(p) para todo n>1

       en.wikipedia.org/wiki/Lucas_sequence"""
    if n<0:
        raise NoEsNumeroNatural("El objeto no representa un número natural")
    if n==0:
        return 2 if not M else 2%M
    Vk  = P             #V1 Vk
    Vk1 = pow(P,2,M) -2 #V2 V2k
    if M: Vk, Vk1, P = Vk % M ,Vk1 % M, P % M
    control = 2**(n.bit_length()-1) >>1
    while control:
        if n & control:
            Vk  = Vk*Vk1 - P       #V2k+1
            Vk1 = pow(Vk1,2,M) - 2 #V2k+2
        else:
            Vk1 = Vk*Vk1 - P       #V2k+1
            Vk  = pow(Vk,2,M)  - 2 #V2k
        if M: Vk,Vk1 = Vk % M ,Vk1 % M
        control >>= 1
    return Vk

sucesion_de_lucas_segundo_tipo_Q1 = lucas_sequence2q1n


def lucas_sequence2q1(*argv, n:int=None, P:int=None, mod:int=None) -> Union[ Vn1, Iterator[Vn1] ] :
    """L2q1(P:int[,*,mod:int]) -> Iterator[Vn(p,1)]
       L2q1(n:int, P:int[,mod:int]) -> Vn(p,1)
       Vn(p,1) Calcula los elementos de la secuancia de lucas de segundo tipo.
       Si n es suministrado calcula el n-esimo elemento de la secuencia.
       Si mod es otorgado calcula: Vn(P,1) modulo mod.

       Estas sucesión se definen como sigue:
       V0(p) = 2
       V1(p) = p
       Vn(p) = p*Vn-1(p) - Vn-2(p) para todo n>1

       (los argumentos pasados como claves tienen precedencia sobre
       los argumentos posicionales)

       en.wikipedia.org/wiki/Lucas_sequence"""
    conf=slice(*argv)
    n = conf.start if n is None else n
    p = conf.stop  if P is None else P
    m = conf.step  if mod is None else mod
    if p is None:
        raise TypeError("parametro P es requerido")
    if n is None:
        return lucas_sequence2(mod=m, param=(p,1))
    return lucas_sequence2q1n(n=n, P=p, M=m)



################################################################################
### ------------------- Sucesión de números de Mersenne ------------------------
################################################################################

def mersenne(n:int=None, m:int=None) -> NumOrGen :
    """Secuencia de los números de Mersenne.
       Estos son los números de la forma: 2^n -1 para algun n natural.
       Si n es suministrado, calcula el n-esimo número de Mersenne.
       Si m es suministrado calcula: 2^n-1 mod m para todo n

       """
    if n is not None and n>=0:
        if m:
            return (pow(2,n,m)-1)%m  #sucesion_de_lucas_primer_tipo(n,3,2,m)
        return pow(2,n)-1
    return sucesion_de_Lucas_Generalizada(a=0,b=1,P=3,Q=2,M=m)



__all__ = [ x for x in dir() if not (x.startswith("_") or x in __exclude_from_all__) ]
del __exclude_from_all__
