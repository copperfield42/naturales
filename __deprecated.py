"""Deprecated funtions of Natural Module
conservadas por acedemic reasons
"""
def primos(*,W=30,buffer=100):
    """Generador infinito de números primos. Eficiente en memoria"""
    #Se emplea sieves segmentados para calcular los primos en
    #intervalos de tamaño W*buffer y para calcular cada intervalo
    #se emplea buffer de memoria, por lo que el uso de memoria
    #es < buffer*(W+1) este sobre estimado se puede mejorar a
    #<= pi(W*buffer)+buffer con pi(n) la función que cuenta la
    #cantidad de primos menores que n, ya que los números primos
    #se distancian cada vez más conforme nos aproximamos al infinito,
    #la cantidad de primos en un intervalo dado sera menor que en el
    #primer intervalo
    for L in itertools.count(0,buffer):
        yield from sorted(sieve_wheel_N_LB(L,buffer,W))

def primos1():
    """ """
    #http://stackoverflow.com/questions/2211990/how-to-implement-an-efficient-infinite-generator-of-prime-numbers-in-python/10733621#10733621
    #erat3
    yield from (2,3,5)
    MASK    = 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0,
    MODULOS = frozenset( (1, 7, 11, 13, 17, 19, 23, 29) )
    Compuestos = dict()
    for num in itertools.compress( itertools.count(7,2),itertools.cycle(MASK) ):
        p = Compuestos.pop(num,None)
        if p is None:
            temp=sorted(Compuestos.values())
            #print(num,len(temp), temp,"\n")
            yield num
            Compuestos[ num**2 ] = num
        else:
            x = num + 2*p
            while x in Compuestos or (x%30) not in MODULOS :
                x += 2*p
            Compuestos[x] = p
        #print(num, sorted(Compuestos.values()))

def sieve_euler(n:int):
    """Generador que implemta el sieve de Euler para encontrar números primos
       menores que n"""
    if n >= 0 :
        if n<=2:
            raise StopIteration()
        if 2<n:
            yield 2
        candidatos = list(range(3,n,2))
        limite = isqrt( n )
        while candidatos:
            primo = candidatos.pop(0)
            yield primo
            if primo>limite:
                break
            else:
                for e in [x for x in candidatos if x%primo==0 ]:
                    candidatos.remove(e)
        yield from candidatos
    else:
        raise EX_NO_NATURAL


#super terrible
def _sieve_sundaram(n:int):
    """Implementación del sieve de Sudaram para encontrar números primos
       menores que 2n+2"""
    if n >= 0:
        if n==0:
            raise StopIteration()
        resul = [True]*(n+1)
        resul[0] = False
        for j in range(1,n+1):
            for i in range(1,j+1):
                d = i+j+2*i*j
                if d <= n :
                    resul[d]=False
        yield 2
        for x in range(1,n+1):
            if resul[x]:
                yield 1+2*x
    else:
        raise EX_NO_NATURAL


def _sundaram_sieve(n:int) -> bool:
    return all((n - i) % (2*i + 1) > 0 for i in range(1, (n + 1) // 2))


def _sundaram(iterable):
    return (2*n + 1 for n in iterable if _sundaram_sieve(n))

def sieve_sundaram(n:int) -> [int]:
    """Implementación del sieve de Sudaram para encontrar números primos
       menores que 2n+2"""
    #https://www.reddit.com/r/dailyprogrammer/comments/q2mwu/2232012_challenge_14_intermediate/
    if n >= 0:
        if n < 1:
            raise StopIteration
        else:
            yield 2
            yield from _sundaram( range(1,n+1) )
##        if n < 2:
##            return []
##        return [2]+list(_sundaram( range(1,n+1) ))
    else:
        raise EX_NO_NATURAL



def sieve_atkin(n:int):
    """Implementación del sieve de Euler para encontrar números primos
       menores que n

       version 1
       https://es.wikipedia.org/wiki/Criba_de_Atkin

       https://en.wikipedia.org/wiki/Sieve_of_Atkin"""
    if n >= 0:
        if n<2:
            raise StopIteration()
        if 2<n:
            yield 2
        if 3<n:
            yield 3
        if 5<n:
            yield 5
            resul = [False]*(n+1)#[2,3,5]
            limite = isqrt(n)+1
            for x,y in itertools.product(range(1,limite),range(1,limite)):
                num = 4*(x**2) + (y**2)
                if num < n and num%12 in {1,5}:
                    resul[num] = not resul[num]
                num = 3*(x**2) + (y**2)
                if num < n and num%12 == 7 :
                    resul[num] = not resul[num]
                if x>y:
                    num = 3*(x**2) - (y**2)
                    if num < n and num%12 == 11 :
                        resul[num] = not resul[num]
            for num in range(5,limite):
                if resul[num]:
                    for x in range(num*num,n,num):
                        resul[x]=False
            for p in range(7,n,2):
                if resul[p]:
                    yield p
    else:
        raise EX_NO_NATURAL



def __aks_find_r_lineal(n,ini,fin,cota,*,verbose=False,ies=1,reverse=False):
    if ini>=fin:
        raise ValueError("Rango vacio")
    if verbose: i=0
    for r in (reversed(range(ini,fin)) if reverse else range(ini,fin)):
        if __aks_multiplicative_order(n,r,cota):
            return r
        elif verbose:
            i+=1
            if i%ies==0:
                print(i,r)   
##el r de fermat_number(13) esta en algun lugar entre:
##Buscando r en [ 2, 36893488147419103233 ] cota= 67108865
##pero se puede reducir a
##ini=2,      fin=67108844,  maxr=134217689+1
##ini=180980, fin=379714650, maxr=759306433
##ini=11,     fin=189812539, maxr=379625069
##ini=18,     fin=94906275,  maxr=189812533
##ini=143,    fin=47453146,  maxr=94906151
## r is in [210.979, 94.906.151]

def _mul(x,n,m=None):
    if n==0:
        return 1 if not m else 1%m
    if n==1:
        return x if not m else x%m
    if n==2:
        return x*x if not m else (x*x)%m
    if n&1:
        return x*(_mul(x,n//2)**2)  if not m else ( x*(_mul(x,n//2)**2) )%m
    else:
        return _mul(x,n//2)**2  if not m else ( _mul(x,n//2)**2 )%m



def _pitagorian_triple_primitive(cota:int=10) -> (int,int,int):
    """Generedor de tripletas con números pitagoricos (a,b,c).
       Estos son los números naturales mayores que cero tales:

       a^2 + b^2 = c^2 con a<b y a,b,c coprimos"""
    for n in range(1,cota):
        for m in range(n+1,cota):
            if sonCoprimos(n,m) and esImpar(m-n):
                a = m**2 - n**2
                b = 2*m*n
                c = m**2 + n**2
                a,b = min(a,b),max(a,b)
                yield a,b,c
                #yield k*a,k*b,k*c
                
def _pitagorian_triple(tope=100, primitivos=True):
    for a in range(1,tope):
        for b in range(a,tope):
            if primitivos and not sonCoprimos(a,b):
                continue
            c2 = a**2 + b**2
            c  = isqrt(c2)
            if c<tope:
                if c**2 == c2:
                    yield a,b,c
            else:
                break

def __primalidad_Test_Trial_Division_extend(n:int) -> bool:
    """Dice si un numero es primo: 2,3,5,7,11...

       Un número es primo si y sólo si es divisible exactamente por sigomismo
       y el 1(uno). Para comprobar esto se usa el metodo de Eratostenes con el
       criterio de Ibn-Al Banna al-Murrakushi para el calculo"""
    if n >= 0 :
        if n<2:
            return False
        elif n<4:
            return True
        elif not n&1 or n%3==0:
            return False
        else:
            return not any( n%i==0 or n%(i+2)==0 for i in range(5,1+isqrt(n),6) )
    else:
        raise EX_NO_NATURAL


def __primalidad_Test_Trial_Division_mod30(n:int)-> bool:
    if n >= 0 :
        if n<2:
            return False
        primos30 = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        if n in primos30:
            return True
        if any( n%x==0 for x in primos30 ):
            return False
        if n >= 30:
            return not any( n%i==0 or n%(i+2)==0 for i in range(29,1+isqrt(n),6) )
        else:
            return False
    else:
        raise EX_NO_NATURAL



def __aks_find_r2(n:int,log_of_n=None,*,verbose=False,ies=1) -> int:
    """Encuentra el r>=2 más pequeño tal que el orden multiplicativo de n modulo r
       sea mayor que el cuadrado del logaritmo de n.
       multiplicative_order(n,r) > log2(n)**2"""
    if not log_of_n:
        log_of_n = log(2,n)
    maxr = max(3,round(log_of_n**5))  #lema 4.3 del paper
    cota = round(log_of_n**2)+1
    if verbose :
        print("Buscando r en [ 2,",maxr,"]","cota=",cota)
    ini = 2
    fin = round(log_of_n ** Decimal("2.5"))
    resul = None
    rever = True
    swicth = True
    old_fin = fin
    i=0
    intercambio = round(log_of_n)
    if verbose:
        print("Iniciando busqueda en:")
        print("ini={}, fin={}, maxr={}, alternando cada {}".format(ini,fin,maxr,intercambio))
    while ini < maxr:
        if swicth:
            if __aks_multiplicative_order(n,ini,cota):
                return ini
            else:
                ini += 1
        else:
            #swicth = not swicth
            if __aks_multiplicative_order(n,fin,cota):
                if ini==fin:
                    return fin
                resul = fin
                maxr  = fin
                fin = (ini+fin-1)//2
                old_fin = fin
                if verbose:
                    print("encontrado un r=",resul)
                    print("--> ini={}, fin={}, maxr={}, iteraciones={}".format(ini,fin,maxr,i+1))
            else:
                fin -= 1
        if ini > fin:
            fin = (maxr -1 ) if resul else maxr
            ini = old_fin+1
            old_fin = fin
        i += 1
        if i % intercambio == 0:
            swicth = not swicth
        if verbose and i%ies==0:
            print(i,"ini={}, fin={}, maxr={}".format(ini,fin,maxr))
##        r = __aks_find_r_lineal(n,ini,fin,cota,verbose=verbose,ies=ies,reverse=rever)
##        if r:
##            resul = r
##            maxr = r
##            r2 = r//2
##            fin = r2 if ini <= r2 else (ini+r)//2
##            if not rever:
##                return resul
##            if verbose :
##                print("encontrado un r=",resul)
##                print("ini={}, fin={}, maxr={}".format(ini,fin,maxr))
##        else:
##            ini = fin
##            fin = maxr
##            rever = False
##            if verbose :
##                print("no se encontro otro r")
##                print("ini={}, fin={}, maxr={}".format(ini,fin,maxr))
        
                
    if resul:
        return resul
    else:
        raise RuntimeError("Falla al encontrar el r")


def __esUnaPotencia(n,*,valor=False,verbose=False) -> bool:
    """Dice si n = a^b para algun a y b con b>1
       Si valor es true, regresa en cambio (a,b) si existen None sino."""
    if n>3:
        a = isqrt(n)
        if a**2 == n:
            if verbose: print("Es cuadrado perfecto")
            return True if not valor else (a,2)
        else:
            if verbose: print("No es cuadrado perfecto")
        nd = Decimal(n)
        magnitud = int( nd.adjusted() + 10 ) #cantidad de digitos del números
        error = Decimal("1E-{}".format( min(42,magnitud) ) )
        log2n = round( nd.ln()/Decimal(2).ln() )
        with localcontext() as ctx:
            ctx.prec = min(max(42,magnitud), MAX_PREC) #para total presicion
            if verbose:
                print("limite de busqueda",log2n,"con prec",ctx.prec,"nivel de error",error)
            espacio_busqueda = sieve_eratosthenes( log2n+1 )
            next(espacio_busqueda)
            for b in espacio_busqueda: 
                a = nd**(Decimal(1)/Decimal(b))
                ar = round(a)
                resul = abs(a - ar)
                if verbose:
                    tam = a.adjusted()+1
                    print("b=",b,"a-int(a)=",float(resul), "digitos de a=",tam, "a=%d"%ar if tam<20 else "")
                if resul <= error:
                    assert ar**b == n , "Error fatal, no es una potencia de los valores encontrados"
                    if valor:
                        return ar,b
                    return True
                    #else: if verbose: print("falso positivo a=",float(ar))
    if verbose: print("No esa una potencia")
    return False if not valor else None

def esUnaPotencia(n:int, *, valor:bool=False, verbose:bool=False, size:int=100) -> Union[bool,Tuple[int,int]]:
    """Dice si n = a^b para algun a y b con b>1
       Si valor es true, regresa en cambio (a,b) si existen, tal que b es minimo.
       Si verbose es cierto se mostrara cual es el b que se esta considerando.
       En el modo verbose, el valor 'a' calculado para un momento dado
       se mostrara su valor real si la cantidad de digitos en el mismo
       es menor o igual al parametro 'size' sino se mostrara una aproxiamación.  """
    if n>3:
        try:
            a = esCuadradoPerfecto(n,valor=True)
            if verbose: print("Es cuadrado perfecto")
            return True if not valor else (a,2)
        except ValueError:
            if verbose :
                #print("No es cuadrado perfecto")
                print("b= 2 a=", +Decimal(n**.5,Context(prec=size)) )
        DN = Decimal(n)
        espacio_busqueda = primos_hasta( 1+round( log(2,DN) ) )
        #solo examino raices primas, pues si no es de una de estas tampoco sera
        #de un número compuesto
        next(espacio_busqueda) #elimino 2, pues ya lo examine
        for b in espacio_busqueda:
            a = nthroot(b,DN,decimales=0)
            if verbose:
                print("b=",b,"a=", +Decimal(a,Context(prec=size)) )
            a = round(a)
            if a**b == n:
                return (a,b) if valor else True
    if verbose: print("No esa una potencia")
    if valor:
        raise ValueError("No es una potencia.")
    return False    
    

def _primalidad_Test_AKS_inocente(n:int,*,verbose=False,pascal=True,ies=1) -> bool:
    """https://en.wikipedia.org/wiki/AKS_primality_test
       version binomial"""
    if n >= 0 :
        if verbose:
            print("probando casos bases")
        if n<2:
            return False
        elif n<4:
            return True
        elif not n&1 or n%3==0:
            return False
        else:
            if pascal:
                if verbose:
                    print("probando la fila de pascal")
                    for k,x in enumerate(itertools.islice( fila_pascal(n) ,2,(n//2)+1),2 ):
                        if x%n != 0:
                            print("falla en k=",k,"con valor=",x)
                            return False
                        elif k%ies==0:
                            print(k)
                    return True
                return all( x%n == 0 for x in itertools.islice( fila_pascal(n) ,2,(n//2)+1) )
            if verbose:
                print("probando la existencia de inversas modulares")
            for k in range(1,(n//2)+1):
                try:
                    mod_inv(k,n)
                    if k%ies==0:
                        print(k)
                except ZeroDivisionError:
                    if verbose:
                        print("falla en k=",k)
                    return False
            return True
    else:
        raise EX_NO_NATURAL

def _factores(n:int) -> [int]:
    """Da todos los factores o divisores de n ordenados de menor a mayor

       Equibalente a: [m for m in range(1,n+1) if n%m==0]
       pero más rápido y eficiente si n es grande."""
    if n >= 0:
        if n==0:
            return []
        resul={1}
        for p in descompocion_en_primos(n,repeticion=True):
            resul.update( [ x*p for x in resul] )
        return sorted( resul )
    else:
        raise NoEsNumeroNatural("El objeto no representa un número natural")

if __name__=="__main__" and __debug__:

    import  timeit,cProfile
  
    def __test_sieve(n,cantidad=1):
        sep ="from __main__ import sieve_eratosthenes , sieve_euler , sieve_filter, sieve_sundaram "
        for test in "sieve_eratosthenes(%d) sieve_euler(%d) sieve_filter(%d) sieve_sundaram((%d-2)//2) ".split():
            print( timeit.timeit(stmt=test%n, setup=sep,number=cantidad),"=",test%n )

    
    def __test_factores(n,cantidad=1):
        sep = "from __main__ import factores"
        for test in ["factores(%d)"%n,"[m for m in range(1,x+1) if x%m==0]".replace("x",str(n))]:
            print( timeit.timeit(stmt=test, setup=sep,number=cantidad),"=",test )

    
    def __test_Trial_Division(n,cantidad=1,repetir=3):
        sep = "from __main__ import "\
              "primalidad_Test_Trial_Division, "\
              "primalidad_Test_Trial_Division_extend, "\
              "primalidad_Test_Trial_Division_mod30 "
              #"primalidad_Test_Trial_Division_primordial, "\
              #"primalidad_Test_Trial_Division_mod30v2"

        funs=["primalidad_Test_Trial_Division(x)",
              "primalidad_Test_Trial_Division_extend(x)",
              "primalidad_Test_Trial_Division_mod30(x)",
              #"primalidad_Test_Trial_Division_primordial(%d)"%n,
              #"primalidad_Test_Trial_Division_mod30v2(%d)"%n,
              ]
        extend="for x in range(%d):"%n
        print("probando con",n,"con",cantidad,"intentos y repitiendola",repetir)
        resultados=dict()
        for test in funs:
            resul = timeit.repeat(stmt=extend+test, setup=sep,number=cantidad,repeat=repetir)
            resultados[extend+test]=sum(resul)/repetir
        #print()
        informe = sorted(resultados.items(),key=lambda x: x[1])
        #print("Informe")
        print("",*map(lambda x: " = ".join(map(str,x))+"\n", informe))
        ##2305843009213693951
        #[3, 7, 31, 127, 8191, 131071, 524287, 2147483647, 2305843009213693951, 618970019642690137449562111]


def descompocion_en_primos_sieve(n,*,repeticion=True,verbose=False,buffer=1000,W=30):
    if isinstance(n,NumeroFactorizado):
        yield from n.descompocion_en_primos(repeticion)
        return
        #raise StopIteration
    if n >= 0:
        if n<2:
            return
            #raise StopIteration
        if esPar(n):
            n,s = factorizacion_ds(n)
            if repeticion:
                yield from ( 2 for x in range(s) )
            else:
                yield 2
        if esPrimo(n):
            yield n
            return 
            #raise StopIteration
        cota = 0
        if verbose:
            i=0
        while n!=1:
            if verbose:
                print("ciclo",i,"rango de busqueda",W*cota,W*(cota+buffer) )
                i += 1
            for p in sieve_wheel_N_LB(cota,buffer,W):
                if n%p == 0:
                    if verbose: print("encontrado factor",p)
                    yield p
                    n //= p
                    while n%p == 0:
                        n //= p
                        if repeticion:
                            yield p
                    if esPrimo(n):
                        if verbose: print("el remanente es primo",n)
                        yield n
                        return
                        #raise StopIteration
            cota += buffer
    else:
        raise NoEsNumeroNatural("El objeto no representa un número natural")

		
def primer_primo(n:int) -> int:
    """Regresa el primer número primo que divida exactamente
       al número n, que de ser primo sera él mismo."""
    if n >= 0:
        if n<2:
            raise ValueError("No exite número primo menor que "+str(n))
        elif not n&1: #si es par
            return 2
        elif esPrimo(n):
            return n
        else:
            mid = 1+isqrt(n)
            i = 3
            while(i<mid and not n%i==0):
                i += 2
            if i >= mid:
                return n
            else:
                return i
    else:
        raise NoEsNumeroNatural("El objeto no representa un número natural")
		
        
        
        
def legendre_simbol(a:int,n:int) -> "-1,0,1":
    """Símbolo de Legendre
       https://en.wikipedia.org/wiki/Legendre_symbol"""
    #raise NotImplementedError
    if esPrimo(n):
        return jacobi_simbol(a,n)
    else:
        raise ValueError("El argumento n debe ser un número primo")

def factorizacion_fermat_number(n) -> [int]:
    """Factoriza el número de fermat dado"""
    #raise NotImplementedError
    k = esFermatNumber(n,valor=True)
    if k is not None:
        dos = 2**(k+2)
        resul = list()
        while n!=1:
            for x,f in enumerate(itertools.count(dos+1,dos),1):
                #f = x*dos +1
                if n%f == 0:
                    resul.append(f)
                    print("n=",n,"tiene con x=",x,", factor de x*2^(%d+2)+1 ="%k,f)
                    n //= f
                    break
        return resul
    else:
        raise ValueError("No es un numero de Fermat")



def pseudoFiboForever(a:int,b:int,m:int=None):
    """Generador de una sucecion como la de Fibonacci con casos bases a y b
       Si m es suministrado, calcula: PF(n) mod m para todo n

       La sucesion de PseudoFibonacci se define como sigue:
       PF(0) = a
       PF(1) = b
       PF(n) = PF(n-1) + PF(n-2), para todo n>=2"""
    return sucesion_de_Lucas_Generalizada(a,b,1,-1,m)


def pseudoFibo(n:int,a:int,b:int,m:int=None) -> int:
    """N-esimo elemento de una sucecion como la de Fibonacci con casos bases a y b
       Si m es suministrado, calcula: PF(n) mod m

       La sucesion de PseudoFibonacci se define como sigue:
       PF(0) = a
       PF(1) = b
       PF(n) = PF(n-1) + PF(n-2), para todo n>=2"""
    if n >= 0:
        return sucesion_de_Lucas_Generalizada_n(n,a,b,1,-1,m)
    else:
        raise NoEsNumeroNatural("El objeto no representa un número natural")
        


def _esLucasProbablePrime(n:int,P:int,Q:int) -> bool:
    raise NotImplementedError()
    if P>0 and esImpar(n):
        D = P*P -4*Q
        index = n - jacobi_simbol(D,n)
        return sucesion_de_lucas_primer_tipo(index,P,Q,n) == 0
    else:
        raise ValueError()



def _esLucasPseudoprimo(n:int,P:int,Q:int) -> bool:
    raise NotImplementedError()
    if P>0 and esImpar(n):
        D = P*P -4*Q
        if jacobi_simbol(D,n) == -1:
            return sucesion_de_lucas_primer_tipo(n+1,P,Q,n) == 0
        return False
    else:
        raise ValueError()




def _esLucasPseudoprimoFuerte(n:int,P:int,Q:int) -> bool:
    raise NotImplementedError()
    if P>0 :
        if esImpar(n):
            D = P*P -4*Q
            if sonCoprimos(n,D):
                index = n - jacobi_simbol(D,n)
                d,s = factorizacion_ds(index)
                if sucesion_de_lucas_primer_tipo(d,P,Q,n) == 0:
                    return True
                for r in range(s):
                    if sucesion_de_lucas_segundo_tipo(d*(2**r),P,Q,n) == 0:
                        return True
                return False
            return False
        else:
            return False
    else:
        raise ValueError()


def _esLucasPseudoprimoFuerteP(n:int,*,verbose=False) -> bool:
    """Dice si el número es un Pseudo Primo Fuerte de Lucas para alguna base P.
       Estos son los números tales que:
       Sea d,s números tales que d*2^s = n+1 y sean Q=1 y
       P perteneciente a [1,2,3,4,5,6...] tal que con D = P^2 -4Q
       el simbolo de Jacobi es (D/n)==-1 cumplen alguna de las
       siquientes ondiciones:

       Ud(P,Q) = 0 (mod n) y Vd(P,Q) =+-2 (mod n)
       o
       V(d*2^r)(P,Q) = 0 (mod n) para algun 0 <= r < s-1


       en.wikipedia.org/wiki/Lucas_pseudoprime#Strong_Lucas_pseudoprimes"""
    raise NotImplementedError()
    if n>=0:
        if n<2:
            return False
        if n<4:
            return True
        if not n&1 or n%3==0 or esCuadradoPerfecto(n):
            return False
        pass
        return False
    else:
        raise NoEsNumeroNatural("El objeto no representa un número natural")


__PERFECT_NUMBER_LIMIT = 15 #limitite hasta el cual el calculo de números perfectos es "instantaneo"

def perfectos(n:int,*,verbose=True,continuar="") -> [int]:
    """Da una lista con los primeros n números perfectos"""
    if n>0:
        if n>__PERFECT_NUMBER_LIMIT and continuar!="si":
            print( "Ha solicitado", n, "números perfectos, esta operación puede tomar mucho tiempo.")
            print( "¿¿Desea continuar??")
            print( "Escriba \"si\" para proceder con el calculo solicitado tome el tiempo que tome.")
            print( "Escriba \"cota\" para entregara una lista con los primeros",
                    __PERFECT_NUMBER_LIMIT,"números perfectos")
            print( "Si no desea continuar, presione enter para salir" )
            respuesta = input("Eligio: ")
            if respuesta=="cota":
                n = __PERFECT_NUMBER_LIMIT
            elif respuesta!="si":
                return []
        res=[]
        for i,x in enumerate( itertools.islice(mersenne_prime_base(),n) ,1 ):
            z = ((2**(x-1))*(2**x-1))
            res.append(z)
            if verbose:
                print( i,"-->",z)#,"raiz",x,"Mersenne prime (2**%d)-1="%x,(2**x)-1)
        if verbose:
            print("\n\n")
        return res
    else:
        if n==0:
            raise RequiereNumeroNaturalDesdeUno("Esta función sólo acepta números naturales mayores o iguales a 1")
        raise NoEsNumeroNatural("El objeto no representa un número natural")






















        