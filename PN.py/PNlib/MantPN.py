# -*- coding: utf-8 -*-
"""
MantPN class
============

Fixed-Point Arithmetic of Polynomial Numbers PN
We assume 1 digits before PN radix point:      
                                               
     (~a_0 ~, a_1 ~ a_2 ~  ...~)

Mantissa of Polynomial Number is constant length polynomial: 
a: a[0] * p**(0) + a[1] * p**(-1) + ... +a[M] * p**(-M),

Values a[n] for high n may be inaccurate due to rounding errors. 

MantPN is only supeclass for Polynomial Number class.
"""
from __future__ import division
__all__ = ['MantPN']


from itertools import zip_longest

if __name__ == '__main__' or __name__ == 'MantPN': 
    #standalone tests: MantPN -> rundocs(), doctest
    import PolyNumConf
    import digitPN
else: #relative package import    #print(f'''__nm__ = {__name__}''')
    from . import PolyNumConf
    # importing separately `PolyNumConf` in your app 
    # some config param. can be changed prior to import `digitPN`.
    from . import digitPN


#################### CONST ############################################

_powersOfTwo = [1]
while _powersOfTwo[-1] < PolyNumConf.max_N:
    _powersOfTwo += [2 * _powersOfTwo[-1]]
_powersOfTwo = tuple(_powersOfTwo)  # (1, 2, 4, 8, 16, 32, 64, 128)

#######################################################################

class MantPN(object):
    """
    A mantissa of Polynomial Number (PN) class
    ==========================================
    MantPN is only supeclass for Polynomial Number class.

    Fixed-Point Arithmetic of Polynomial Numbers PN
    We assume 1 digits before PN radix point:      
                                                   
         (~a_0 ~, a_1 ~ a_2 ~  ...~)
    
    Mantissa of Polynomial Number is constant length polynomial: 
    a: a[0] * p**(0) + a[1] * p**(-1) + ... +a[M] * p**(-M),
    
    Values a[n] for high n may be inaccurate due to rounding errors. 
    
    Attributes:
    ----------
        mantissa: 
            the Polynomial Number **(PN)** "digits", in decreasing (negative)
            powers, starting from power 0. List of _max_N elements, filled
            with zeros of type as first element.
    
    Parameters
    ----------
    mant:
        the Polynomial Number's coefficients (mantissa), in decreasing (negative)
        powers, starting from power 0. 
    
    Const. fixed as class attr.
    ---------------------------
    _max_N = PolyNumConf.max_N

    Examples
    --------
    - zero
    >>> print(MantPN()) # MantPN() got MantPN([mpf('0.0')])
    MantPN([0.0])
    
    - non-zero
    >>> MantPN([1.,2,3])
    MantPN([1.0, 2, 3, 0.0])
    >>> MantPN([1,2,3])
    MantPN([1, 2, 3, 0])
    >>> MantPN([1,2.0,3])
    MantPN([1, 2.0, 3, 0])
    >>> print( MantPN([3+digitPN.zeroPNdig,2,digitPN.onePNdig]) )
    MantPN([3.0, 2, 1.0, 0.0])
    
    - other object, not dtype:
    >>> from fractions import Fraction
    >>> MantPN([Fraction(1/2),Fraction(5,9),6])
    MantPN([Fraction(1, 2), Fraction(5, 9), 6, Fraction(0, 1)])
    
    """
    __hash__ = None
    
    _max_N = PolyNumConf.max_N #num. of mantissa items

    @property
    def mantissa(self):
        """ A copy of the coefficients"""
        return self._mantissa[:] #or  deepcopy ?

    # alias attributes
    m = mantissa

    def __init__(self, mant=None):
        """
        default init: [0.0, 0.0, ...] zeros of type digitPN.zeroPNdig
        """
        if isinstance(mant, MantPN):
            self._mantissa = mant.mantissa
            return
        
        #if not mant: #numpy ValueError: The truth value of an array with more than one element is ambiguous.
        if (mant is None) or not len(mant):
            mant = [digitPN.zeroPNdig] #type is determined in digitPN, rather not [0.0] 
        self._mantissa = list(mant[:self._max_N])
        self._fillZerosProc()
#        mant = atleast_1d(mant) #objects as Fraction should work...
#        if mant > 1:
#            raise ValueError("Mantissa of Polynomial Number must be 1d only.")
#todo np.isscalar(3.1) - after chceck if numpy is imported
#but generally numpy is not needed here
# import numpy as np
# if isinstance(P, (list, tuple, np.ndarray))

    def _fillZerosProc(self):
        assert self._mantissa, "At least one element must exist, to add zeroes of the same type!"
        if len(self._mantissa) < self._max_N:
            zero = 0 * self._mantissa[0]
            self._mantissa += [zero for __ in range(self._max_N-len(self._mantissa))]
        
            
    def _shrMantProc(self, r):
        zero = 0 * self._mantissa[0]
        if r > self._max_N:
            r = self._max_N
        zeros = [zero for __ in range(r)]
        self._mantissa = zeros + self._mantissa[:(self._max_N - r)]
            
#    def __array__(self, t=None):
#        if t:
#            return NX.asarray(self._mantissa, t)
#        else:
#            return NX.asarray(self._mantissa)

    def __repr__(self):
        '''
        preserve last 0 (or something else leads to False)
        
        Examples
        --------
        MantPN([0.0])
        MantPN([1, 2, 3, 0])
        MantPN([1.0, 2, 3, 0.0])
        >>> from mpmath import mp, mpf
        >>> MantPN([mpf('3.0'), 2, mpf('1.0'), mpf('0.0')])
        MantPN([mpf('3.0'), 2, mpf('1.0'), mpf('0.0')])
        '''
        last = len(self.mantissa)
        for d in self.mantissa[::-1]:
            if d:
                break
            else:
                last = last - 1
        return 'MantPN('+repr(self._mantissa[:last+1])+')' #preserve last 0 (and only one 0)
    
    def __str__(self):
        '''
        like __repr__, but uses str() internally

        >>> from mpmath import mp, mpf
        >>> print(MantPN([mpf('3.0'), 2, mpf('1.0'), mpf('0.0')]))
        MantPN([3.0, 2, 1.0, 0.0])
        '''
        last = len(self.mantissa)
        for d in self.mantissa[::-1]:
            if d:
                break
            else:
                last = last - 1
        return 'MantPN(['+', '.join([str(d) for d in self._mantissa[:last+1]])+'])' #preserve last 0 (and only one 0)
    
    
    def __format__(self, format_spec):
        s = self.__str__()
        return s.__format__(format_spec)

    def __nonzero__(self):
        for d in self._mantissa:
            if d:
                return True
        return False

    def __len__(self):
        return self._max_N

    def __call__(self, val):
        """
        >>> p = MantPN([3.,0,1,2])
        >>> p(5.)  # 3. * 5.**0 + 0 * 5.**(-1)1 + 1 * 5.**(-2) + 2 * 5.**(-3)
        3.056
        >>> p(MantPN([5.]))  # 3. * 5.**0 + 0 * 5.**(-1)1 + 1 * 5.**(-2) + 2 * 5.**(-3)
        MantPN([3.056, 0.0])
        >>> p = MantPN([3+digitPN.zeroPNdig,0,1,2])
        >>> print( p(5+digitPN.zeroPNdig) )  # 3. * 5.**0 + 0 * 5.**(-1)1 + 1 * 5.**(-2) + 2 * 5.**(-3)
        3.056
        """  
        return mantPN_val(self.mantissa, val)
    #todo :trzeba to przemyleć - dla przypadku, gdy val nie jest Float, ale np. PN

    def __neg__(self):
        """
        >>> -MantPN([1.,2,3])
        MantPN([-1.0, -2, -3, -0.0])
        """
        return MantPN([-x for x in self._mantissa])

    def __pos__(self):
        return self

    def __mul__(self, other):
        """
        `other` should be MantPN or something like scalar - which can be 
        muliplicated one-by-one with PN digits
        
        Examples
        --------
        >>> MantPN([1.,2,3]) * 100
        MantPN([100.0, 200, 300, 0.0])
        >>> MantPN([1.,2,3]) * MantPN([0.1,2])
        MantPN([0.1, 2.2, 4.3, 6.0, 0.0])
        >>> MantPN([0.1,2]) * MantPN([1.,2,3])
        MantPN([0.1, 2.2, 4.3, 6.0, 0.0])
        >>> 100 * MantPN([1.,2,3]) #__rmul__ test
        MantPN([100.0, 200, 300, 0.0])
        
        >>> p1 = MantPN([1.,2,3]) #__imul__   test 
        >>> p1 *= MantPN([0.1,2])
        >>> p1     
        MantPN([0.1, 2.2, 4.3, 6.0, 0.0])
        >>> p100 = 100. #__imul__   test 
        >>> p100 *= MantPN([0.1,2])
        >>> p100     
        MantPN([10.0, 200.0, 0.0])
        """
        if isinstance(other, MantPN):
            return MantPN(mantPN_mul(self.mantissa, other.mantissa, self._max_N))
        else:
            return MantPN([x * other for x in self.mantissa])

    def __rmul__(self, other): # case: other * self 
        if not isinstance(other, MantPN):
            return MantPN([other * x for x in self.mantissa])
        #else: done by __mul__


    def __div__(self, other):
        """
        `other` should be MantPN or something like scalar - which can 
        divided one-by-one PN digits
        
        Examples
        --------
        >>> MantPN([1.,2,3]) / 100
        MantPN([0.01, 0.02, 0.03, 0.0])
        
         >>> y2 = ( 1 / MantPN([0.1,2.]) ) * MantPN([0.2,4.])
         >>> y2.mantissa[:25]
         [2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -281474976710656.0, 4503599627370496.0]
         
         #it should be [2.0, 0.0, 0.0,..] but ...
         
#        >>> ( MantPN([1.,2,3]) / MantPN([0.1,2]) ) * MantPN([0.2,4])
#        [0.1, 2.2, 4.3, 6.0, 0.0]
#        >>> MantPN([0.1,2]) / MantPN([1.,2,3])
#        [0.1, 2.2, 4.3, 6.0, 0.0]
#        >>> 100 / MantPN([1.,2,3]) #__rdiv__ test
#        [100.0, 200, 300, 0.0]
#        
#        >>> p1 = MantPN([1.,2,3]) #__idiv__   test 
#        >>> p1 /= MantPN([0.1,2])
#        >>> p1     
#        [0.1, 2.2, 4.3, 6.0, 0.0]
#        >>> p100 = 100. #__idiv__   test 
#        >>> p100 /= MantPN([0.1,2])
#        >>> p100     
#        [10.0, 200.0, 0.0]
        """
        if isinstance(other, MantPN):
            return MantPN(mantPN_mul(
                self.mantissa, 
                mantPN_inv(other.mantissa, self._max_N), self._max_N))
        else:
            return MantPN([x / other for x in self.mantissa])

    __truediv__ = __div__

    def __rdiv__(self, other): # case: other / self 
        if not isinstance(other, MantPN):
            inv = mantPN_inv(self.mantissa, self._max_N)
            if other == 1:
                return MantPN(inv)
            return MantPN([other * x for x in inv])
        #else: done by __div__

    __rtruediv__ = __rdiv__


    def __add__(self, other):
        """
        >>> MantPN([1.,2,3]) + MantPN([5,6,6]) 
        MantPN([6.0, 8, 9, 0.0])
        >>> MantPN([3.,0,1,2]) + 12
        MantPN([15.0, 0, 1, 2, 0.0])
        """
        if isinstance(other, MantPN):
            return MantPN([a + b for (a,b) in 
                zip_longest(self.mantissa, other.mantissa, fillvalue=0)])
        else:
            return MantPN([self._mantissa[0] + other] + self._mantissa[1:]) 
                                            # + i.e. concatenate lists

    def __radd__(self, other): # case: other + self 
        """
        >>> 200 + MantPN([3.,0,1,2])
        MantPN([203.0, 0, 1, 2, 0.0])
        """
        if not isinstance(other, MantPN):
            return MantPN([other + self._mantissa[0]] + self._mantissa[1:])
        #else: done by __add__

    def __sub__(self, other):
        """
        >>> MantPN([1.,2,3]) - MantPN([5,6,6]) 
        MantPN([-4.0, -4, -3, 0.0])
        >>> MantPN([3.,0,1,2]) - 12
        MantPN([-9.0, 0, 1, 2, 0.0])
        """
        if isinstance(other, MantPN):
            return MantPN([a - b for (a,b) in 
                           zip_longest(self.mantissa, other.mantissa, fillvalue=0)])
        else:
            return MantPN([self._mantissa[0] - other] + self._mantissa[1:])

    def __rsub__(self, other): # case: other - self 
        """
        >>> 12 - MantPN([3.,0,1,2])
        MantPN([9.0, 0, -1, -2, -0.0])
        """
        return MantPN([other - self._mantissa[0]] + [-x for x in self._mantissa[1:]])
    
    def _MantPN_isclose(self, other, rel_tol=digitPN.epsilonPNdig*128, abs_tol=digitPN.epsilonPNdig*128): 
        """
        Return :
        True if True for all pair digits a,b from self and others:
        if a - b == 0 or |a - b| <= abs_tol: True 
        else:
            if (|a-b| and rel_tol) are compatybile type: 
                |a-b| <= rel_tol*max(|a|,|b|)
            else: 
                raise NotImplementedError 
        """
        if not isinstance(other, MantPN):
            return NotImplemented
        for a, b in zip(self.mantissa, other.mantissa):
            if not digitPN.PNdig_isclose(a, b, rel_tol, abs_tol): # a != b:
                return False
        return True

    
    def __eq__(self, other):
        """
        #>>> MantPN([3.1,0,1,2]) == MantPN([3.,0,1,2])
        #Traceback (most recent call last):
        #...
        #NotImplementedError
        >>> MantPN([3,0,1,2]) == MantPN([3,0,1,2])
        True
        >>> MantPN([1+digitPN.epsilonPNdig*128,0,1,2]) == MantPN([1-digitPN.epsilonPNdig,0,1,2])
        False
        >>> MantPN([1+digitPN.epsilonPNdig*128,0,1,2]) == MantPN([1+digitPN.epsilonPNdig,0,1,2])
        True
        """
        return self._MantPN_isclose(other)
        #return (self.mantissa == other.mantissa).all()

    def __ne__(self, other):
        """
        >>> MantPN([3,0,1,2]) != MantPN([3,0,1,2])
        False
        """
        if not isinstance(other, MantPN):
            return NotImplemented
        return not self.__eq__(other)
    
    def __abs__(self):
        """
        | self |
        see a concept of partially ordered Mikusinski space
        """
        return MantPN([abs(x) for x in self.mantissa])

    def _isnonnegative(self):
        """
        self >= 0
        see a concept of partially ordered Mikusinski space
        """
        for x in self.mantissa:
            if not x >= 0:
                return False
        return True

# =============================================================================
#     def __getitem__(self, key):
#         return self.mantissa[key]
# 
#     def __setitem__(self, key, val):
#         self._mantissa[key] = val
#         return
# 
#     def __iter__(self):
#         return iter(self.mantissa)
# =============================================================================
    
    def __pow__(self, a):
        return mantPN_power_real(self.mantissa, a, self._max_N)

    def inv(self):
        return mantPN_inv(self.mantissa, self._max_N)

    def sqrt(self):
        return mantPN_sqrt(self.mantissa, self._max_N)

    def exp(self):
        return mantPN_exp(self.mantissa, self._max_N)

    def ln(self):
        return mantPN_ln(self.mantissa, self._max_N)

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

def mantPN_val(p, x):
    """
    Evaluate (Horner's scheme) a MantPN `p` at specific value `x` - scalar 
    or other objcets. Type of x is very important. x can be MantPN

    Examples
    --------
    >>> mantPN_val([3.0,0,1,2], 5.0)  # 3 * 5**0 + 0 * 5**(-1)1 + 1 * 5**(-2) + 2 * 5**(-3)
    3.056
    >>> mantPN_val([3,0,1,2], 5)
    3.056
    >>> from fractions import Fraction
    >>> mantPN_val([3,0,1], Fraction(1,3))
    Fraction(12, 1)

    """
    x_1 = 1/x
    y = p[-1]
    pp = p[::-1]
    for p1 in pp[1:]:
        y = y * x_1 + p1
    return y

def mantPN_mul(x, h, N):
    """
    Find the product of two mantPN.

    Parameters
    ----------
    x, h : mantPN objects, both must have N elements!

    Returns
    -------
    out : (x * h)[:N]

    Examples
    --------
    >>> mantPN_mul([1, 2, 3], [9, 5, 1], 3)
    [9, 23, 38]

    >>> mantPN_mul([1, 2, 3], [9., 5, 1], 3)
    [9.0, 23.0, 38.0]

    dtype=object
    >>> from fractions import Fraction
    >>> p12 = [Fraction('1/2'), 10, 2]
    >>> p12
    [Fraction(1, 2), 10, 2]
    >>> p13 = [Fraction('1/3'), 100, 0]
    >>> p13
    [Fraction(1, 3), 100, 0]
    >>> mantPN_mul(p12, p13, 3)
    [Fraction(1, 6), Fraction(160, 3), Fraction(3002, 3)]

    >>> mantPN_mul([Fraction('1/2'), 10, 2.], [Fraction('1/3'), 100, 0], 3)
    [Fraction(1, 6), Fraction(160, 3), 1000.6666666666666]

    """
    zero = (x[0]+h[0])*0 # zero of common-type of x and y
    y = [zero for __ in range(N)]     # y = [zero]*N
    for k in range(N):
      for j in range(k+1):
        y[k] = y[k] + x[k-j]*h[j]
    return y
    
    #y = NX.convolve(x, h, mode='full') #'same' - max(M, N);  'full' - M+N-1
    #return y[:N]


def mantPN_inv(x, N):
    """
    Find an inversion of mantPN.

    Parameters
    ----------
    x : mantPN object, must have N elements!

    Returns
    -------
    y :  
        (1 / x)[:N]

    Examples
    --------
    >>> x = [0.5, 7, 0, 0, 0, 0, 0, 0]
    >>> y = mantPN_inv(x, 8)
    >>> print(y[:6])
    [2.0, -28.0, 392.0, -5488.0, 76832.0, -1075648.0]
    >>> print(mantPN_mul(x, y, 8))
    [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    
    """
    zero = x[0] * 0
    LoN = 0
    while _powersOfTwo[LoN] < N:
        LoN += 1 # 2**LoN >= N
    #print(f'''N={N}, 2**   {_powersOfTwo[LoN]} -- {_powersOfTwo}''')
    v = [zero for __ in range(_powersOfTwo[LoN])]   # v = [zero] * _powersOfTwo[LoN]
    y = v[:]
    if len(x) < len(v): # case if N != _powersOfTwo[LoN]
        x = (x + v)[:len(v)]
    y[0] = 1 / x[0] #x[0]**(-1), despite of x[0] type
    for w in range(LoN):
        nw = _powersOfTwo[w]
        for k in range(nw):
            v[k] = zero # unnecessary?
            for j in range(nw):
                v[k] = v[k] + y[j] * x[k+nw-j]
        for k in range(nw):
            y[k+nw] = zero # unnecessary?
            for j in range(k+1):
                y[k+nw] = y[k+nw] - y[k-j] * v[j]
                #? if abs(y[k+nw]) >= sqrt(MaxFloat): y[k+nw] = sqrt(MaxFloat) ?
    return y[:N]

def mantPN_sqrt(x, N):
    """
    sqrt(x)[:N]
    =====
    
    Examples
    --------
    >>> xx = [0.1,2.,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0]
    >>> y0 = mantPN_sqrt(xx, 32)
    >>> print(', '.join([digitPN.strF(y) for y in y0[:7]])) #     0.316227766, 3.16227766, -15.8113883, 158.113883, -1976.42354, 27669.9295, -415048.943, 6522197.67
    0.316227766, 3.16227766, -15.8113883, 158.113883, -1976.42354, 27669.9295, -415048.943
    >>> print(', '.join([digitPN.strF(y) for y in mantPN_mul(y0, y0, 32)[:5]])) # 0.1, 2.0, -9.40395481e-38, -1.88079096e-36, -1.50463277e-35, -5.77778983e-34, -1.00148357e-32, 3.08148791e-32
    0.1, 2.0, 0.0, 0.0, 0.0
    """
    if x[0] <= 0:
        raise ValueError("{sqrt(x)} 1st digit of x is not positive: {}".format(x[0]))
    zero = x[0] * 0
    LoN = 1
    while _powersOfTwo[LoN] < N:
        LoN += 1 # 2**LoN >= N
    y = [zero for __ in range(_powersOfTwo[LoN])]   # [zero] * _powersOfTwo[LoN]
    odwr = y[:]
    outp = y[:]
    if len(x) < len(y): # case if N != _powersOfTwo[LoN]
        x = (x + y)[:len(y)]
    outp[0] = digitPN.sqrt(x[0])
    for w in range(1, LoN+1):
        odwr = mantPN_inv(outp, _powersOfTwo[w])
        y = mantPN_mul(odwr, x, _powersOfTwo[w]) #mantPN_div(outp,x,_powersOfTwo[w])
        for j in range(_powersOfTwo[w-1]):
            outp[j] = (outp[j] + y[j]) / 2 # 1/2 despite of () type 
        for j in range(_powersOfTwo[w-1], _powersOfTwo[w]):
            outp[j] = y[j] / 2
    return outp[:N]
    
def mantPN_power_real(x, a, N):
    """
    self **a
    ========
    where exists self[0] **a (a is rather float, fract or int)
    
    Examples
    --------
    >>> xx = [0.1,2.,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 
    ... 0,0,0,0]
    >>> y0 = mantPN_inv(xx, 32)
    >>> print(y0[:4])
    [10.0, -200.0, 4000.0, -80000.0]
    >>> y1 = mantPN_power_real(xx, -1, 32)
    >>> print(y1[:6])
    [10.0, -200.0, 4000.0, -80000.0, 1600000.0, -32000000.0]
    >>> print('-- 1 ----------')
    -- 1 ----------
    >>> print(mantPN_mul(y0, xx, 32)[:25])
    [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -140737488355328.0, 2251799813685248.0]
    >>> print(mantPN_mul(y1, xx, 32)[:32])
    [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2251799813685248.0, 0.0, 0.0, 1.8446744073709552e+19, 0.0, 0.0, 0.0, 0.0]
    
    >>> y05 = mantPN_power_real(xx, 0.5, 32)
    >>> y05[:4]
    [0.31622776601683794, 3.162277660168379, -15.811388300841895, 158.11388300841892]
    >>> mantPN_power_real(y05, 2, 23)
    [0.1, 2.0, 0.0, -1.1234667099445442e-14, 0.0, 0.0, 0.0, -7.362751430292565e-10, 0.0, 1.8848643661548967e-07, 0.0, 4.8252527773565355e-05, 0.0, 0.0, -0.3952847075210474, 6.324555320336758, -101.19288512538813, 0.0, 25905.37859209936, 0.0, 0.0, 0.0, 0.0]

    """
    zero = x[0] * 0
    outp = [zero for __ in range(N)]     # y = [zero]*N
    outp[0] = x[0] **a
    a += 1
    for k in range(1, N):
        for j in range(1, k+1):
            outp[k] = outp[k] + x[j] * outp[k-j] * (a*j/k - 1)
        outp[k] = outp[k] / x[0]
    return outp
    
def mantPN_exp(x, N):
    """
    exp(x)
    ======
    >>> xx = [0]*32
    >>> xx[0:2] = [digitPN.flt('0.1'),digitPN.flt('2.')]
    >>> y0 = mantPN_exp(xx, 32)
    >>> print(', '.join([digitPN.strF(y) for y in y0[:4]]))
    1.10517092, 2.21034184, 2.21034184, 1.47356122
    >>> print(', '.join([digitPN.strF(y) for y in mantPN_ln(y0,32)[:4]]))
    0.1, 2.0, 0.0, 0.0
    """
    zero = x[0]*0 
    exp_x0 = digitPN.exp(x[0])
    outp = [exp_x0 * x1 for x1 in x]
    outp[0] = exp_x0
    for k in range(1, N):
        #outp[k] = exp_x0 * x[k]
        for j in range(1, k):
            outp[k] += x[k-j] * outp[j] * (1 - (zero + j)/k)
    return outp

def mantPN_ln(x, N):
    """
    ln(x)
    =====
    """
    zero = x[0]*0 
    ln_x0 = digitPN.log(x[0])
    outp = x[:]
    outp[0] = ln_x0
    for k in range(1, N):
        #outp[k] = x[k]
        for j in range(1, k):
            outp[k] -= x[j] * outp[k-j] * (1 - (zero + j)/k)
        outp[k] = outp[k] / x[0]
    return outp
    
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

if __name__ == "__main__":
    #p(MantPN([5.,0]))
    #print(p(5.))  # 3. * 5.**0 + 0 * 5.**(-1)1 + 1 * 5.**(-2)
    #mantPN_val([3.0,0,1,2], 5)
    
    #xx = [0.1,2.,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0]
    #y0 = mantPN_inv(xx, 32); print(y0); y1 = mantPN_power_real(xx, -1, 32); print(y1)
    #print('-- 1 ----------')
    #print(mantPN_mul(y0, xx, 32)) #print(mantPN_mul(y1, xx, 32))
    
    #x = [0.5, 7, 0, 0, 0, 0, 0, 0];  y = mantPN_inv(x, 8); print(y); print(mantPN_mul(x, y, 8))
    #p123 = MantPN([1.,2,3]); p100 = p123 * 100; print(p100)
    #print(mantPN_mul([1, 2, 3], [9, 5, 1], 3))#PolyNumConf.max_N)
    
#    from numpy.testing import (
#        run_module_suite, assert_, assert_equal, assert_array_equal,
#        assert_almost_equal, assert_array_almost_equal, assert_raises, 
#        rundocs
#        )
#    rundocs(); print('OK.')

    import doctest
    doctest.testmod(); print('OK.')
