# -*- coding: utf-8 -*-
u"""
Implementación de los recipes de Itertools compatible con python 2.7 y 3.5
Además para versiones anteriores de python, pone a disposición los equivalentes
de las funciones disponibles en itertools en python 3.5 eso incluye 'ifilter', 
'izip', 'ifilterfalse', 'izip_longest', 'imap' con sus nombres como en python 3
'filter', 'zip', 'filterfalse', 'zip_longest', 'map'"""


import operator as _op, collections as _co, random as _ran
import sys as _sys, numbers as _num
from functools import partial as _par

version="2.1"

#comunes a 2.7 y 3.5
##from itertools import chain, combinations, combinations_with_replacement, \
##                      compress, count, cycle, dropwhile, groupby, islice, \
##                      permutations, product, repeat, starmap, takewhile, tee \
##                      

from itertools import chain, count, cycle, dropwhile, repeat, takewhile

try:#python 2
    from itertools import ifilter as filter, ifilterfalse as filterfalse, \
                          imap as map, izip as zip #, izip_longest as zip_longest
except ImportError:
    #python 3
    from itertools import filterfalse #, zip_longest

try:#python 2
    range = xrange
except NameError:
    #python 3
    pass    


###posible fallos de importacion en python anteriores son:
##accumulate new in 3.2 agregado func in 3.3
##combinations_with_replacement new in 3.1 and 2.7
##compress new in 3.1 and 2.7
##count añadido el step in 3.1 and 2.7
##chain.from_iterable new in 2.6
##combinations new in 2.6
#groupby new in 2.4 
##islice Changed in version 2.5: accept None values for default start and step.
#izip Changed in version 2.4 When no iterables are specified, 
#     returns a zero length iterator instead of raising a TypeError exception.
##izip_longest new in 2.6
##permutations new in 2.6
##product new in 2.6
##starmap Changed in version 2.6: Previously, starmap() required the function arguments to be tuples. 
#        Now, any iterable is allowed
##tee new in 2.4


    
try: #python 3
    from itertools import accumulate 
    accumulate([1,2,3],_op.add) #3.1
except (ImportError,TypeError):
    #python 2 o anterior a 3.2
    def accumulate(iterable, func=_op.add):
        u"""Return series of accumulated sums (or other binary function results).
           accumulate([1,2,3,4,5]) --> 1 3 6 10 15
           accumulate([1,2,3,4,5], operator.mul) --> 1 2 6 24 120"""
        it = iter(iterable)
        try:
            total = next(it)
        except StopIteration:
            return
        yield total
        for element in it:
            total = func(total, element)
            yield total

try:
    chain.from_iterable
except AttributeError:
    #python 2.5-
    _chain = chain 
    class chain(_chain):
        
        @classmethod
        def from_iterable(cls,iterables):
            u"""chain.from_iterable(['ABC', 'DEF']) --> A B C D E F"""
            for it in iterables:
                for element in it:
                    yield element

    del _chain

try:
    from itertools import combinations
except ImportError:
    def combinations(iterable, r):
        u"""combinations('ABCD', 2) --> AB AC AD BC BD CD
           combinations(range(4), 3) --> 012 013 023 123"""
        pool = tuple(iterable)
        n = len(pool)
        for indices in permutations(range(n), r):
            if all( x<=y for x,y in pairwise(indices) ):  #sorted(indices) == list(indices):
                yield tuple(pool[i] for i in indices)

try:
    from itertools import combinations_with_replacement
except ImportError:
    def combinations_with_replacement(iterable, r):
        u"""Return successive r-length combinations of elements in the iterable
            allowing individual elements to have successive repeats.
            combinations_with_replacement('ABC', 2) --> AA AB AC BB BC CC"""
        pool = tuple(iterable)
        n = len(pool)
        for indices in product(range(n), repeat=r):
            if all( x<=y for x,y in pairwise(indices) ): #sorted(indices) == list(indices):
                yield tuple(pool[i] for i in indices)

try:
    from itertools import compress
except ImportError:
    #python 2.6- o 3.0
    def compress(data, selectors):
        u"""compress('ABCDEF', [1,0,1,0,1,1]) --> A C E F"""
        return (d for d, s in zip(data, selectors) if s)
            
try:
    count(0,2)
except TypeError:
    #python 2.6- o 3.1-
    def count(start=0, step=1):
        u"""count(10) --> 10 11 12 13 14 ...
           count(2.5, 0.5) -> 2.5 3.0 3.5 ..."""
        n = start
        while True:
            yield n
            n += step

try:
    from itertools import groupby
except ImportError:
    class groupby(object):
        u"""[k for k, g in groupby('AAAABBBCCDAABBB')] --> A B C D A B
           [list(g) for k, g in groupby('AAAABBBCCD')] --> AAAA BBB CC D"""
           
        def __init__(self, iterable, key=None):
            if key is None:
                key = lambda x: x
            self.keyfunc = key
            self.it = iter(iterable)
            self.tgtkey = self.currkey = self.currvalue = object()
            
        def __iter__(self):
            return self
            
        def __next__(self):
            while self.currkey == self.tgtkey:
                self.currvalue = next(self.it)    # Exit on StopIteration
                self.currkey = self.keyfunc(self.currvalue)
            self.tgtkey = self.currkey
            return (self.currkey, self._grouper(self.tgtkey))
        
        next = __next__ # para versiones anteriores 
        
        def _grouper(self, tgtkey):
            while self.currkey == tgtkey:
                yield self.currvalue
                try:
                    self.currvalue = next(self.it)
                except StopIteration:
                    return
                self.currkey = self.keyfunc(self.currvalue)
        
        


try:
    from itertools import islice
except ImportError:
    def islice(iterable, *args):
        u"""islice('ABCDEFG', 2) --> A B
            islice('ABCDEFG', 2, 4) --> C D
            islice('ABCDEFG', 2, None) --> C D E F G
            islice('ABCDEFG', 0, None, 2) --> A C E G"""
        s = slice(*args)
        it = iter(range(s.start or 0, s.stop or sys.maxsize, s.step or 1))
        try:
            nexti = next(it)
        except StopIteration:
            return
        for i, element in enumerate(iterable):
            if i == nexti:
                yield element
                nexti = next(it)


try:
    from itertools import permutations
except ImportError:
    def permutations(iterable, r=None):
        u"""permutations('ABCD', 2) --> AB AC AD BA BC BD CA CB CD DA DB DC
            permutations(range(3)) --> 012 021 102 120 201 210 """
        pool = tuple(iterable)
        n = len(pool)
        r = n if r is None else r
        for indices in product(range(n), repeat=r):
            if len(set(indices)) == r:
                yield tuple(pool[i] for i in indices)



try:
    from itertools import product
except ImportError:
    def product(*args, **kwds):
        u"""product('ABCD', 'xy') --> Ax Ay Bx By Cx Cy Dx Dy
            product(range(2), repeat=3) --> 000 001 010 011 100 101 110 111"""
        pools = [tuple(pool) for pool in args] * kwds.get('repeat', 1)
        result = [[]]
        for pool in pools:
            result = [x+[y] for x in result for y in pool]
        for prod in result:
            yield tuple(prod)


try:
    from itertools import starmap
except ImportError:
    def starmap(function, iterable):
        u"""starmap(pow, [(2,5), (3,2), (10,3)]) --> 32 9 1000"""
        for args in iterable:
            yield function(*args)


try:
    from itertools import tee
except ImportError:
    def tee(iterable, n=2):
        u"""tee(iterable, n=2) --> tuple of n independent iterators."""
        it = iter(iterable)
        deques = [_co.deque() for i in range(n)]
        def gen(mydeque):
            while True:
                if not mydeque:             # when the local deque is empty
                    try:
                        newval = next(it)   # fetch a new value and
                    except StopIteration:
                        return
                    for d in deques:        # load it to all the deques
                        d.append(newval)
                yield mydeque.popleft()
        return tuple(gen(d) for d in deques)


try: #python 2
    from itertools import izip_longest as zip_longest
except ImportError:
    try:
        from itertools import zip_longest 
    except ImportError:
        #python 2.5-
        class ZipExhausted(Exception):
            pass

        def zip_longest(*args, **kwds):
            u"""zip_longest('ABCD', 'xy', fillvalue='-') --> Ax By C- D-"""
            fillvalue = kwds.get('fillvalue')
            counter = [len(args) - 1]
            def sentinel():
                #nonlocal counter
                if not counter[0]:
                    raise ZipExhausted
                counter[0] -= 1
                yield fillvalue
            fillers = repeat(fillvalue)
            iterators = [chain(it, sentinel(), fillers) for it in args]
            try:
                while iterators:
                    yield tuple(map(next, iterators))
            except ZipExhausted:
                pass
        
    
            



            

############ Mis recipes ##################

def take(n, iterable, **karg):
    u"""Regresa los primeros n elementos del iterable como una tupla.
        Se puede espesificar el contenedor con el paramero key-only
        'container' en cuyo caso, los elementos son guardados en
        una instancia del mismo.

        take(3,"ABCDEFGHI") --> A B C"""
    container = karg.get("container",tuple)
    return container(islice(iterable, n))

def advance(n,iterable,**karg):
    u"""Regresa un iterador con los datos agrupados en bloques de a lo
        sumo n elementos del iterable. 
        Ejemplo:
        >>> ej=[1,2,3,4,5,6,7,8,9]
        >>> list(advance(4,ej))
        [(1, 2, 3, 4), (5, 6, 7, 8), (9,)]

        Se puede espesificar el contenedor con el paramero key-only
        'container' en cuyo caso, los elementos son guardados en
        una instancia del mismo."""
    return takewhile( bool, repeatfunc(_par(take,**karg),None,n,iter(iterable)) )

def _len_range(ran):
    #http://stackoverflow.com/questions/14754877/pre-compute-lenrangestart-stop-step
    if isinstance(ran,range):
        try:
            return len(ran)
        except OverflowError:
            pass
        start,stop,step = 0, 0, 1 
        if all( hasattr(ran,x) for x in {"start","stop","step"} ):
            start,stop,step =  ran.start, ran.stop, ran.step
        else:
            elem = list(map(int,repr(ran).replace("xrange(","").replace(")","").split(",")))
            if len(elem) == 1:
                stop = elem[0]
            elif len(elem) == 2:
                start,stop = elem
            else:
                start,stop,step = ran
        return max(0, (stop - start) // step + bool((stop - start) % step))
    else:
        raise ValueError("Se esperaba una instancia de range or xrange")
    
def ilen(iterable,ignore_overflow=True) :
    u"""Dice la cantidad de elementos del iterable iterando sobre el mismo si es necesario."""
    if isinstance(iterable, _co.Sized):
        #print("sized")
        try:
            return len(iterable)
        except OverflowError as oe:
            #print("over")
            if not ignore_overflow:
                raise oe
            elif isinstance(iterable,range):
                #print("range")
                return _len_range(iterable)
    tam = 0
    for tam,_ in enumerate(iterable,1):pass
    return tam
       

try: #python 2
    _basestring = basestring
except NameError:
    #python 3
    _basestring = (str,bytes)
    
def flatten_total(iterable, flattype=_co.Iterable, ignoretype=_basestring):
    u"""Flatten all level of nesting of a arbitrary iterable"""
    #http://stackoverflow.com/questions/2158395/flatten-an-irregular-list-of-lists-in-python
    #unutbu version
    remanente = iter(iterable)
    while True:
        elem = next(remanente)
        if isinstance(elem,flattype) and not isinstance(elem,ignoretype):
            remanente = chain( elem, remanente )
        else:
            yield elem
            
def flatten_level(iterable,nivel=1,flattype=_co.Iterable, ignoretype=_basestring):
    u"""Flatten N levels of nesting of a arbitrary iterable"""
    #http://stackoverflow.com/questions/2158395/flatten-an-irregular-list-of-lists-in-python
    #Cristian version modificada
    if nivel < 0:
        yield iterable
        return
    for elem in iterable:
        if isinstance(elem,flattype) and not isinstance(elem,ignoretype):
            for sub in flatten_level(elem,nivel-1,flattype,ignoretype):
                yield sub
        else:
            yield elem

def irange(start,stop,step=1):
    u"""Simple iterador para producir valores en [start,stop)""" 
    return takewhile(lambda x: x<stop, count(start,step))

def groupwise(n,iterable):
    u"""s -> (s0,s1,...,sn), (s1,s2,...,sn+1), (s2, s3,...,sn+2), ..."""
    grupo = tee(iterable,n)
    for i,e in enumerate(grupo):
        consume(e,i)
    return zip( *grupo )

def tail(iterable,n=None):
    u"""Return an iterator over the last n items,
        if n is none return a iterator over all
        elemens in iterable save the first

        tail('ABCDEFG',3) --> E F G
        tail('ABCDEFG')   --> B C D E F G """
    if n is None:
        resul = iter(iterable)
        next(resul,None)
        return resul
    return iter(_co.deque(iterable, maxlen=n))

def ida_y_vuelta(iterable):
    u"""s-> s0,s1,s2,...,sn-2,sn-1,sn,sn-1,sn-2,...,s2,s1,s0"""
    try:
        ida = iter(iterable)
        vue = reversed(iterable)
        next(vue,None)
        for x in chain(ida,vue):
            yield x
    except TypeError:
        vue = list()
        for x in iterable:
            yield x
            vue.append(x)
        if vue:
            vue.pop()
        for x in reversed(vue):
            yield x

def powerset(iterable,ini=0,fin=None):
    u"""Da todas las posibles combinaciones de entre ini y fin elementos del iterable
        Si fin no es otorgado default a la cantidad de elementos del iterable

        powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
        powerset([1,2,3],2) -->  (1,2) (1,3) (2,3) (1,2,3)
        powerset([1,2,3],0,2) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) """
    if ini<0 or (fin is not None and fin<0):
        raise ValueError("El rango de combinaciones debe ser no negativo")
    elem = list(iterable)
    if fin is None:
        fin = len(elem)
    return chain.from_iterable( combinations(elem, r) for r in range(ini,fin+1) )

def iteratefunc(func,start,times=None,iter_while=None):
    u"""Generador de relaciones de recurrencia de primer order:
        F0 = start
        Fn = func( F(n-1) )

        iteratefunc(func,start)   -> F0 F1 F2 ...
        iteratefunc(func,start,n) -> F0 F1 F2 ... Fn

        func: función de 1 argumento cuyo resultado es usado para
              producir el siguiente elemento de secuencia en la
              siguiente llamada.
        start: elemento inicial de la secuencia.
        times: cantidad de elemtos que se desea generar de la
               secuencia, si es None se crea una secuencia infinita.
        iter_while: si es otorgado se producen elementos de la secuencia
                    mientras estos cumplan con esta condición. """
    if times is None:
        seq = repeat(start)
    else:
        seq = repeat(start,times)
    if iter_while:
        return takewhile(iter_while,accumulate(seq,lambda x,_:func(x)))
    return accumulate(seq,lambda x,_:func(x))



##def lookahead(iterable, i=0):
##    u"""Inspect the i-th upcomping value from a iterable object
##        while leaving the iterable object at its current position.
##
##        Raise an IndexError if the underlying iterator doesn't
##        have enough values."""
##    for value in islice(_dcopy(iterable), i, None):
##        return value
##    raise IndexError(i)


########### Itertools recipes #############   

def repeatfunc(func, times=None, *args):
    u"""Repeat calls to func with specified arguments.

        Example:  repeatfunc(random.random)"""
    if times is None:
        return starmap(func, repeat(args))
    return starmap(func, repeat(args, times))

def grouper(iterable, n, fillvalue=None):
    u"""Collect data into fixed-length chunks or blocks
        grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"""
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

def tabulate(function, start=0):
    u"""Return function(0), function(1), ..."""
    return map(function, count(start))

def consume(iterator,n=None):
    u"""Advance the iterator n-steps ahead. If n is none, consume entirely."""
    # Use functions that consume iterators at C speed.
    if n is None:
        # feed the entire iterator into a zero-length deque
        _co.deque(iterator, maxlen=0)
    else:
        # advance to the empty slice starting at position n
        next(islice(iterator, n, n), None)

def nth(iterable, n, default=None):
    u"""Returns the nth item or a default value"""
    return next(islice(iterable, n, None), default)

def quantify(iterable, pred=bool):
    u"""Count how many times the predicate is true"""
    return sum(map(pred, iterable))

def padnone(iterable):
    u"""Returns the sequence elements and then returns None indefinitely.

        Useful for emulating the behavior of the built-in map() function."""
    return chain(iterable, repeat(None))

def ncycles(iterable, n):
    u"""Returns the sequence elements n times

        ncycles("XYZ",3) --> X Y Z X Y Z X Y Z"""
    return chain.from_iterable(repeat(tuple(iterable), n))

def dotproduct(vec1, vec2, sum=sum, map=map, mul=_op.mul):
    u"""sum(map(mul, vec1, vec2))"""
    return sum(map(mul, vec1, vec2))

def flatten(listOfLists):
    u"""Flatten one level of nesting"""
    return chain.from_iterable(listOfLists)

def pairwise(iterable):
    u"""s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

def roundrobin(*iterables):
    u"""roundrobin('ABC', 'D', 'EF') --> A D E B F C"""
    # Recipe credited to George Sakkis
    pending = len(iterables)
    nexts = cycle(iter(it).__next__ for it in iterables)
    while pending:
        try:
            for next in nexts:
                yield next()
        except StopIteration:
            pending -= 1
            nexts = cycle(islice(nexts, pending))

def partition(pred, iterable):
    u"""Use a predicate to partition entries into false entries and true entries
        partition(is_odd, range(10)) --> 0 2 4 6 8  and  1 3 5 7 9"""
    t1, t2 = tee(iterable)
    return filterfalse(pred, t1), filter(pred, t2)

def unique_everseen(iterable, key=None):
    u"""List unique elements, preserving order. Remember all elements ever seen.
        unique_everseen('AAAABBBCCDAABBB') --> A B C D
        unique_everseen('ABBCcAD', str.lower) --> A B C D"""
    seen = set()
    seen_add = seen.add
    if key is None:
        for element in filterfalse(seen.__contains__, iterable):
            seen_add(element)
            yield element
    else:
        for element in iterable:
            k = key(element)
            if k not in seen:
                seen_add(k)
                yield element

def unique_justseen(iterable, key=None):
    u"""List unique elements, preserving order. Remember only the element just seen.
        unique_justseen('AAAABBBCCDAABBB') --> A B C D A B
        unique_justseen('ABBCcAD', str.lower) --> A B C A D"""
    return map(next, map(_op.itemgetter(1), groupby(iterable, key)))
    

def iter_except(func, exception, first=None):
    u"""Call a function repeatedly until an exception is raised.

        Converts a call-until-exception interface to an iterator interface.
        Like __builtin__.iter(func, sentinel) but uses an exception instead
        of a sentinel to end the loop.

        Examples:
            iter_except(functools.partial(heappop, h), IndexError)   # priority queue iterator
            iter_except(d.popitem, KeyError)                         # non-blocking dict iterator
            iter_except(d.popleft, IndexError)                       # non-blocking deque iterator
            iter_except(q.get_nowait, Queue.Empty)                   # loop over a producer Queue
            iter_except(s.pop, KeyError)                             # non-blocking set iterator"""
    try:
        if first is not None:
            yield first()  # For database APIs needing an initial cast to db.first()
        while True:
            yield func()
    except exception:
        pass

def first_true(iterable, default=False, pred=None):
    u"""Returns the first true value in the iterable.

        If no true value is found, returns *default*

        If *pred* is not None, returns the first item
        for which pred(item) is true.

        
        first_true([a,b,c], x) --> a or b or c or x
        first_true([a,b], x, f) --> a if f(a) else b if f(b) else x """
    return next(filter(pred, iterable), default)


#def random_product(*args, repeat=1):
#    u"""Random selection from itertools.product(*args, **kwds)"""
#    pools = [tuple(pool) for pool in args] * repeat
#    return tuple(_ran.choice(pool) for pool in pools)
    
def random_product(*args, **kwds):
    u"""Random selection from itertools.product(*args, **kwds)"""
    pools = list(map(tuple, args)) * kwds.get('repeat', 1)
    return tuple(_ran.choice(pool) for pool in pools)
    

def random_permutation(iterable, r=None):
    u"""Random selection from itertools.permutations(iterable, r)"""
    pool = tuple(iterable)
    r = len(pool) if r is None else r
    return tuple(_ran.sample(pool, r))

def random_combination(iterable, r):
    u"""Random selection from itertools.combinations(iterable, r)"""
    pool = tuple(iterable)
    n = len(pool)
    indices = sorted(_ran.sample(range(n), r))
    return tuple(pool[i] for i in indices)

def random_combination_with_replacement(iterable, r):
    u"""Random selection from itertools.combinations_with_replacement(iterable, r)"""
    pool = tuple(iterable)
    n = len(pool)
    indices = sorted(_ran.randrange(n) for i in range(r))
    return tuple(pool[i] for i in indices)


