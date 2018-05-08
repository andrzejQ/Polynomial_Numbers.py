# -*- coding: utf-8 -*-
"""
PolyNum class 
============
(Polynomial Number class)
    
    =========================
    Floating point arithmetic for "numbers" with digit like real number or items
    from any arbitrary field, allow solving of differential or difference 
    problems using Mikusinski's or Bellert's approach.
    http://www.pei.prz.edu.pl/%7Ekubaszek/index_en.html
    
    We assume PN in form:                                  
                                            c             
            (~m ~, m ~ m ~  ...~) · (~1~0~)               
               0    1   2                                 
    where: m - PN mantissa         c - characteristic (chrtic)
    
    
    
todo:
    invTr1LaplPN() calculates the inverse Lpn transform in a point t, assuming 
        s = (~1~0~)
    invTr05LaplPN()   sqrt(S) = (~1~0~)  i.e. s = (~1~0~0~)
    invTr05exp_b0_LaplPN

    exp if self.exponent > 0

"""
from __future__ import division, absolute_import, print_function
#but tested only in python 3.6+
from six import string_types #if isinstance(value, six.string_types):

__all__ = ['PolyNum']

import numbers #isinstance(x, numbers.Integral)

if __name__ == '__main__' or __name__ == 'PolyNum':
    #standalone tests: PolyNum -> rundocs(), doctest
    import PolyNumConf
    import digitPN
    from MantPN import MantPN
else: #relative package import    #print(f'''__nm__ = {__name__}''')
    from . import PolyNumConf
    # importing separately `PolyNumConf` in your app 
    # some config param. can be changed prior to import `digitPN` `MantPN`.
    from . import digitPN
    from .MantPN import MantPN

class PolyNum(MantPN):
    """
    A Polynomial Number class
    =========================
    Floating point arithmetic for "numbers" with digit like real number or items
    from any arbitrary field, allow solving of differential or difference 
    problems using Mikusinski's or Bellert's approach.
    http://www.pei.prz.edu.pl/%7Ekubaszek/index_en.html
    
    Attributes:
    ----------
        mantissa: 
            the Polynomial Number **(PN)** "digits", in decreasing (negative)
            powers, starting from power 0.
            - see MantPN.py

        exponent:
            int
    
    Parameters
    ----------
    mantissa_or_pN_or_str : 
        if array_like: 
            the Polynomial Number's coefficients, in decreasing (negative)
            powers, starting from power 0. (see class attr. self._max_N)
        if PN: 
            input PN to copy, adding exponentAdd to exponent
        if string: 
            '<mantissa>*(~1~0~)**(<exponent>)'
            where <exponent> is integer, <mantissa> is '(~<d0>~,~<d1>~...~)'
            <d0>,... - real numbers, '~,' or '~,~' denotes "floating point dot"
            (see class attr. self._sep = '~')
    exponentAdd:
        value added to 0 or original PN exponent (if exists)
        
    #attr `_strPN_cut` (int) could be added to istance, to show first `_strPN_cut` 
        digits in str() and repr().

    Examples
    --------
    - PN zero
    >>> PolyNum()
    PolyNum('(~0.0~)')
    
    - PN from string:
    >>> PolyNum('(~1.2~,2.5~-0.3~)*(~1~0~)**(-2)')
    PolyNum('(~1.2~,2.5~-0.3~)*(~1~0~)**(-2)')
    >>> PolyNum('(~1.2~)')
    PolyNum('(~1.2~)')
    >>> PolyNum('(~0~,2.5~-0.3~)')
    PolyNum('(~2.5~,-0.3~)*(~1~0~)**(-1)')
    >>> PolyNum('(~,2.5~-0.3~)')
    PolyNum('(~2.5~,-0.3~)*(~1~0~)**(-1)')
    >>> PolyNum('(~-1.1~2.2~,-3.3~)')
    PolyNum('(~-1.1~,2.2~-3.3~)*(~1~0~)**(1)')

    - PN const from string:
    >>> # p_trap(h) == (2/h) * (~1~-1~) / (~1~1~) == (1/h) * (~2~,-4~4~-4~4~...~)
    >>> y1=PolyNum('const:(~2~,-4~4~-4~4~...~)'); y1._strPN_cut = 7;  y1
    PolyNum('(~2~,-4~4~-4~4~-4~4~...~)')
    >>> # flat samples ready to multiply by (a/2):
    >>> y2=PolyNum('const:(~1~,2~2~2~2~...~)'); y2._strPN_cut = 7;  y2
    PolyNum('(~1~,2~2~2~2~2~2~...~)')
    
    - PN matissa and exponent
    >>> p1 = PolyNum([1.1,2,3],-2); p1
    PolyNum('(~1.1~,2~3~)*(~1~0~)**(-2)')
    >>> p2 = PolyNum(p1, 12); p2
    PolyNum('(~1.1~,2~3~)*(~1~0~)**(10)')
    >>> pM0 = PolyNum(MantPN([1.1,2,3])); pM0
    PolyNum('(~1.1~,2~3~)')
    """
    __hash__ = None
    
    _sep = PolyNumConf.sep #'~' # in str() and repr()
    
    #property `mantissa` in MantPN and
    @property
    def exponent(self):
        """ The exponent of the Polynomial Number """
        if hasattr(self, '_exponent'): # ?
            return self._exponent
        else:
            return 0

    def __init__(self, mantissa_or_pN_or_str=None, exponentAdd=0):
        """First digit non-zero or zero PN (with mantissa fill of zeroes)"""
        if isinstance(mantissa_or_pN_or_str, PolyNum):
            super(PolyNum,self).__init__(mantissa_or_pN_or_str.mantissa)
            self._exponent = exponentAdd
            if hasattr(self,'exponent'):
                self._exponent = mantissa_or_pN_or_str.exponent + exponentAdd
            return
        
        if mantissa_or_pN_or_str is None:
            mantissa_or_pN_or_str = []
        elif isinstance(mantissa_or_pN_or_str, string_types): # six.string_types
            mantissa_or_pN_or_str, exponent1 = \
                getMantissaExponent_fromStr(mantissa_or_pN_or_str, self._sep, self._max_N)
            exponentAdd += exponent1
        else: #mantissa_or_pN_or_str should be array_like
            if isinstance(mantissa_or_pN_or_str, numbers.Number):
                mantissa_or_pN_or_str = [mantissa_or_pN_or_str]

        super(PolyNum,self).__init__(mantissa_or_pN_or_str)
        self._exponent = exponentAdd
        self._normalize0() #case: PolyNum('(~0~,2.~-0.3~)'), 100

    def _normalize0(self): #return None
        """First digit non-zero or zero PN - to use in init"""
        if self._mantissa[0]: #nothing to do
            return self
        first = 0
        m0 = self._mantissa[0]
        for d in self._mantissa:
            if d: #d!= 0
                break
            else:
                first += 1
                self._exponent  -= 1
        if first == len(self._mantissa):
            self._mantissa = [m0] #preserve first 0.0 - to get type of mant[0]
        else:
            self._mantissa = self._mantissa[first:]
        self._fillZerosProc() # fill right zeros
        
#-----------------------------------------------------------
        
    def _normalize(self): 
        """
        return PolyNum copy with first digit non-zero or zero PN 
        if actions with mantissa/exponent was performed. 
        If first digit is nonzero return self reference (not a copy).
        - To use after add, sub, div
        """
        if self._mantissa[0]: #nothing to do
            return self
        y = PolyNum(self) #copy of mantissa, because it will be shifted
        y._normalize0()
        return y
    
    def asList(self):
        '''
        List normalized to exponent=0 for exponent <= 0
        
        '''
        if not self.__nonzero__:
            mantissaE0 = [self._mantissa[0] for __ in range(self._max_N)] #[0.,0.,0.,...]
        else:
            ex = -self.exponent 
            if ex == 0:
                mantissaE0 = self.mantissa
            elif ex < 0:
                raise ValueError(
                    'PN exponent = {}. Can not convert to array if PN exponent > 0'\
                    .format(-ex))
            else: #(-self.exponent) > 0
                zero = 0 * self._mantissa[0]
                mantissaE0 = [zero for __ in range(ex)] + self._mantissa 
            return mantissaE0 #return NX.asarray(mantissaE0)
    # def __array__(self): return NX.asarray(self.asList)

    def __str__(self):
        '''
        Examples
        --------
        >>> for s in [s.strip() for s in PolyNum.__str__.__doc__.splitlines()]: 
        ...     if s and s[0] == '(': print(PolyNum(s)) # identity test
        (~1.2~,2.5~-0.3~)*(~1~0~)**(-2)
        (~1.2~,2.5~-0.3~)*(~1~0~)**(2)
        (~1.2~,2.5~-0.3~)
        (~1.2~)
        '''
        return self._strPN(digitPN.strF)
    
    def __repr__(self):
        return "PolyNum('"+self._strPN(digitPN.reprF)+"')"
    
    def _strPN(self, digToStr):
        """
        digToStr = digitPN.strF
        """
        cutedStr = hasattr(self, '_strPN_cut') and self._strPN_cut < self._max_N
        ma = self.mantissa
        ex = self.exponent
        # r = '({0}{1}{0}'.format(self._sep, ma[0]) # (~{}~
        try:
            r1 = digToStr(ma[0])
        except ValueError: #try without formatting (i.e. for int)
            r1 = str(ma[0])
        r = '('+self._sep + r1 + self._sep #~
            
        if ma[0]: #non-zero PN
            ma = ma[1:]
            #ma = trim_zeros(ma, trim='b') #'b' to trim from back
            last = len(ma)
            for d in ma[::-1]:
                if d:
                    break
                else:
                    last = last - 1
            ma = ma[:last]
            if cutedStr and (len(ma) < self._strPN_cut-1):
               cutedStr = False 
            if cutedStr:
                ma = ma[:self._strPN_cut-1]
            if len(ma):
                r += ','
                for m in ma:
                    r += digToStr(m) + self._sep #~
                    
        if cutedStr:
            r += '...~'
        r += ')'
        if ex and self.__nonzero__():
            r += '*({0}1{0}0{0})**({1})'.format(self._sep, ex) #*(~1~0~)**({})
        return r
        
    def chop(self, tol=digitPN.epsilonPNdig*1024*1024): #1024*1024 = 1e6
        """
        Converts PN digits close to zero to exact zeros. Normalize at the end.
        todo: tol can grow with digit index
        
        >>> PolyNum('(~0.1~,2e-38~4.3~6.1e-10~)').chop()
        PolyNum('(~0.1~,0.0~4.3~6.1e-10~)')
        >>> PolyNum('(~1e-36~,2e-38~4.3~6.0~)').chop()
        PolyNum('(~4.3~,6.0~)*(~1~0~)**(-2)')
        """
        zero = self.mantissa[0] * 0
        ma = [digitPN.chop( d, tol, zero ) for d in self.mantissa]
        x = PolyNum(ma, self.exponent)
        return x._normalize0()

    def __format__(self, format_spec):
        s = self.__str__()
        return s.__format__(format_spec)
    
    def __nonzero__(self): #different then in MantPN !
        return self._mantissa[0]

    def __len__(self):
        return self._max_N

    def __call__(self, val):
        """
        >>> p = PolyNum([3.,0,1,2])
        >>> p(5.)  # 3. * 5.**0 + 0 * 5.**(-1)1 + 1 * 5.**(-2) + 2 * 5.**(-3)
        3.056
        >>> p1 = PolyNum([3.,0,1,2],-2)
        >>> p1(5.)
        0.12224
        
        >>> p(PolyNum([5.]))  # 3. * 5.**0 + 0 * 5.**(-1)1 + 1 * 5.**(-2) + 2 * 5.**(-3)
        PolyNum('(~3.056~)')
        
        """  
        if not self.__nonzero__():
            return val * 0 # zero of val type
        y = super(PolyNum,self).__call__(val)
        res = 1
        if self.exponent:
            res = val #val **self.exponent
            for _ in range(abs(self.exponent)-1): res *= val
        if self.exponent < 0:
            return y / res
        else:
            return y * res

    def __neg__(self):
        return PolyNum([-x for x in self._mantissa], self.exponent)

    def __pos__(self):
        return self

    def __mul__(self, other):
        """
        Examples
        --------
        >>> PolyNum([1.,2,3],-2) * 100
        PolyNum('(~100.0~,200~300~)*(~1~0~)**(-2)')
        >>> PolyNum([1.,2,3],-2) * PolyNum([0.1,2],-5)
        PolyNum('(~0.1~,2.2~4.3~6.0~)*(~1~0~)**(-7)')
        >>> PolyNum([0.1,2],-5) * PolyNum([1.,2,3],-2)
        PolyNum('(~0.1~,2.2~4.3~6.0~)*(~1~0~)**(-7)')
        >>> 100 * PolyNum([1.,2,3],-2) #__rmul__ test
        PolyNum('(~100.0~,200~300~)*(~1~0~)**(-2)')
        
        >>> p1 = PolyNum([1.,2,3],-2) #__imul__   test 
        >>> p1 *= PolyNum([0.1,2],-5)
        >>> p1     
        PolyNum('(~0.1~,2.2~4.3~6.0~)*(~1~0~)**(-7)')
        >>> p100 = 100. #__imul__   test 
        >>> p100 *= PolyNum([0.1,2],-5)
        >>> p100     
        PolyNum('(~10.0~,200.0~)*(~1~0~)**(-5)')
        """
        if not self.__nonzero__():
            return PolyNum(self) #PolyNum() - copy of mantissa
        if not other:
            return PolyNum([0 * self._mantissa[0]])
        y = super(PolyNum,self).__mul__(other)
        expoOther = 0
        if hasattr(other, 'exponent'):
            expoOther = other.exponent
        return PolyNum(y, self.exponent + expoOther)

    def __rmul__(self, other): # case: other * self 
        if not self.__nonzero__():
            return PolyNum(self)
        if not other:
            return PolyNum([0 * self._mantissa[0]])
        y = super(PolyNum,self).__mul__(other)
        expoOther = 0 #f.ex. int, real, MantPN
        if hasattr(other, 'exponent'): #this is rather __mul__ case
            expoOther = other.exponent
        return PolyNum(y, self.exponent + expoOther)

    def __div__(self, other): #self / other
        """
        Examples
        --------
        >>> y1 = PolyNum([1.,0.2,0.3],-2) / PolyNum([0.1,0.2],-5)
        >>> y1._strPN_cut = 7; str(y1)
        '(~10.0~,-18.0~39.0~-78.0~156.0~-312.0~624.0~...~)*(~1~0~)**(3)'
        >>> y2 = PolyNum('(~0.1~,0.2~)',-5) / PolyNum('(~1.~,0.2~0.4~)',-2)
        >>> y2._strPN_cut = 7; str(y2)
        '(~0.1~,0.18~-0.076~-0.0568~0.04176~0.014368~-0.0195776~...~)*(~1~0~)**(-3)'
        >>> PolyNum([1.,0.2,0.3],-2) / 100
        PolyNum('(~0.01~,0.002~0.003~)*(~1~0~)**(-2)')
        >>> y3 = 100 / PolyNum('(~1.~,0.2~0.3~)',-2) #__rdiv__ test
        >>> y3._strPN_cut = 7; y3
        PolyNum('(~100.0~,-20.0~-26.0~11.2~5.56~-4.472~-0.7736~...~)*(~1~0~)**(2)')
        
        >>> p1 = PolyNum([1.,0.2,0.3],-2) #__idiv__   test 
        >>> p1 /= PolyNum([0.1,0.2],-5)
        >>> p1._strPN_cut = 7; p1     
        PolyNum('(~10.0~,-18.0~39.0~-78.0~156.0~-312.0~624.0~...~)*(~1~0~)**(3)')
        >>> p100 = 100. #__idiv__   test 
        >>> p100 /= PolyNum([0.1,0.2],-5)
        >>> p100._strPN_cut = 7; p100     
        PolyNum('(~1000.0~,-2000.0~4000.0~-8000.0~16000.0~-32000.0~64000.0~...~)*(~1~0~)**(5)')
        
        """
        if not self.__nonzero__():
            return PolyNum(self) #PolyNum() - copy of mantissa
        y = super(PolyNum,self).__div__(other)
        expoOther = 0
        if hasattr(other, 'exponent'):
            expoOther = other.exponent
        return PolyNum(y, self.exponent - expoOther)

    __truediv__ = __div__

    def __rdiv__(self, other): # case: other / self 
        if not other:
            return PolyNum([0 * self._mantissa[0]])
        y = super(PolyNum,self).__rdiv__(other)
        expoOther = 0 #f.ex. int, real, MantPN
        if hasattr(other, 'exponent'): #this is rather __mul__ case
            expoOther = other.exponent
        return PolyNum(y, expoOther - self.exponent)

    __rtruediv__ = __rdiv__

    def __add__(self, other):
        """
        >>> PolyNum('(~1~,2~3~)') + PolyNum('(~10~,20~30~)')
        PolyNum('(~11.0~,22.0~33.0~)')
        >>> PolyNum('(~1~,2~3~)*(~1~0~)**(-3)') + PolyNum('(~10~,20~30~)*(~1~0~)**(-1)')
        PolyNum('(~10.0~,20.0~31.0~2.0~3.0~)*(~1~0~)**(-1)')
        >>> PolyNum('(~1~,2~3~)*(~1~0~)**(-3)') + 100
        PolyNum('(~100.0~,0.0~0.0~1.0~2.0~3.0~)')
        >>> PolyNum('(~1~2~3~)') + 100
        PolyNum('(~1.0~,2.0~103.0~)*(~1~0~)**(2)')
        
        >>> 100 + PolyNum([1.,2,3],-2) #__radd__ test
        PolyNum('(~100.0~,0.0~1.0~2~3~)')
        
        >>> p1 = PolyNum([1.,2,3],-2) #__iadd__   test 
        >>> p1 += PolyNum([0.1,5],-4)
        >>> p1     
        PolyNum('(~1.0~,2.0~3.1~5.0~)*(~1~0~)**(-2)')
        >>> p100 = 100. #__iadd__   test 
        >>> p100 += PolyNum([0.1,2],-4)
        >>> p100     
        PolyNum('(~100.0~,0.0~0.0~0.0~0.1~2.0~)')

        """
        if not other:
            return PolyNum(self) #PolyNum() - copy of mantissa
        otherPN = PolyNum(other)
        if not self.__nonzero__():
            return PolyNum(otherPN)
        if otherPN.exponent <= self.exponent:
            a1, a2 = self, otherPN
        else:
            a1, a2 = otherPN, self
        if a2.exponent < a1.exponent - self._max_N:
            return PolyNum(a1)
        if a2.exponent == a1.exponent: #it will be a common case - do not shrMant()
            y = super(PolyNum,a1).__add__(a2)
        else:
            a2 = PolyNum(a2) #copy of a2 mantissa, which will be shifted
            a2._shrMantProc(a1.exponent - a2.exponent) 
            #because of leading zero a2 is treating as (~0~) PolynNum in debugger, 
            #but i.e. a2.mantissa == [0.0, 0.0, 1.0, 2, 3, 0.0, ... 
            y = super(PolyNum,a1).__add__(a2) #y is MantPN()
        return PolyNum(y, a1.exponent)._normalize()

    def __radd__(self, other):
        return self.__add__(PolyNum(other))

    def __sub__(self, other):
        '''
        >>> PolyNum('(~1~,2~3~)') - PolyNum('(~10~,20~30~)')
        PolyNum('(~-9.0~,-18.0~-27.0~)')
        >>> PolyNum('(~1~,2~3~)*(~1~0~)**(-3)') - PolyNum('(~10~,20~30~)*(~1~0~)**(-1)')
        PolyNum('(~-10.0~,-20.0~-29.0~2.0~3.0~)*(~1~0~)**(-1)')
        >>> PolyNum('(~1~,2~3~)*(~1~0~)**(-3)') - 100
        PolyNum('(~-100.0~,0.0~0.0~1.0~2.0~3.0~)')
        >>> PolyNum('(~1~2~3~)') - 100
        PolyNum('(~1.0~,2.0~-97.0~)*(~1~0~)**(2)')
        
        >>> 100 - PolyNum([1.1,2,3],-2) #__radd__ test
        PolyNum('(~100.0~,0.0~-1.1~-2~-3~)')
        
        >>> p1 = PolyNum([1.1,2.5,3],-2) #__iadd__   test 
        >>> p1 -= PolyNum([0.1,5.1],-4)
        >>> p1     
        PolyNum('(~1.1~,2.5~2.9~-5.1~)*(~1~0~)**(-2)')
        >>> p100 = 100. #__iadd__   test 
        >>> p100 -= PolyNum([0.1,2],-4)
        >>> p100     
        PolyNum('(~100.0~,0.0~0.0~0.0~-0.1~-2.0~)')
        '''
        return self.__add__(-PolyNum(other))

    def __rsub__(self, other): # case: other - self 
        selfNeg = -self
        return selfNeg.__radd__(other)
        

    def __pow__(self, a):
        """
        self **a
        ========
        where exists self[0] **a (a is rather float, fract or int)
            
        Examples
        --------
        >>> xx = PolyNum('(~0.1~,2.0~)')
        >>> y0 = 1 / xx
        >>> y0._strPN_cut = 5
        >>> y0
        PolyNum('(~10.0~,-200.0~4000.0~-80000.0~1600000.0~...~)')
        >>> y1 = xx **(-1)
        >>> y1._strPN_cut = 5
        >>> y1
        PolyNum('(~10.0~,-200.0~4000.0~-80000.0~1600000.0~...~)')
        >>> print('-- 1 ----------')
        -- 1 ----------
        >>> y0xx = (y0 * xx); y0xx._strPN_cut = 22; y0xx
        PolyNum('(~1.0~,0.0~0.0~0.0~0.0~0.0~0.0~0.0~0.0~0.0~0.0~0.0~0.0~0.0~0.0~0.0~0.0~0.0~0.0~0.0~0.0~0.0~...~)')
        >>> y1xx = (y1 * xx); y1xx._strPN_cut = 22; y1xx
        PolyNum('(~1.0~,0.0~0.0~0.0~0.0~0.0~0.0~0.0~0.0~0.0~0.0~0.0~0.0~0.0~0.0~0.0~0.0~0.0~0.0~0.0~0.0~0.0~...~)')
        """
        if not a or not self.__nonzero__():  # results of x[0] **0 and 0 **a (rather =1) determined by mantissa[0] **a
            return PolyNum([self._mantissa[0] **a]) # (~1~,0~0~...~)
        if (self.exponent != 0 and not isinstance(a, numbers.Integral)):
            raise ValueError("Power only to int, real, rational by exponent 0 or to int otherwise")
        #if self.exponent == 0 power to int, real, rational allowed
        y = super(PolyNum,self).__pow__(a)
        expo = 0
        if self.exponent != 0:
            expo = self.exponent * a
            assert isinstance(expo, numbers.Integral)
        return PolyNum(y, expo)

        
    def isclose(self, other, rel_tol=digitPN.epsilonPNdig*128, abs_tol=digitPN.epsilonPNdig*128): 
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
        if (not self) and (not other):
            return True
        if isinstance(other, PolyNum):
            otherPN = other
        else:
            otherPN = PolyNum(other)
        if otherPN.exponent <= self.exponent:
            a1, a2 = self, otherPN
        else:
            a1, a2 = otherPN, self
        if a2.exponent != a1.exponent: 
            a2 = PolyNum(a2) #copy of a2 mantissa, which will be shifted
            a2._shrMantProc(a1.exponent - a2.exponent) 
            #because of leading zero a2 is treating as (~0~) PolynNum in debugger, 
            #but i.e. a2.mantissa == [0.0, 0.0, 1.0, 2, 3, 0.0, ... 
        return a1.mantissa._MantPN_isclose(other.mantissa, rel_tol, abs_tol) 

    def __eq__(self, other):
        return self.isclose(other)

    def __ne__(self, other):
        if not isinstance(other, PolyNum):
            return NotImplemented
        return not self.__eq__(other)
        
        
    def __abs__(self):
        """
        | . |
        see a concept of partially ordered Mikusinski space
        
        >>> abs(PolyNum('(~2.4~,-1.1~-8.8~)'))
        PolyNum('(~2.4~,1.1~8.8~)')
        """
        return PolyNum(super(PolyNum,self).__abs__(), self.exponent)
        
    def isnonnegative(self):
        """
        self >= 0
        see a concept of partially ordered Mikusinski space

        >>> x = PolyNum('(~2.4~,-1.1~-8~)')
        >>> x.isnonnegative()
        False
        >>> abs(x).isnonnegative()
        True
        >>> PolyNum(0.0).isnonnegative()
        True
        """
        return not self.__nonzero__() \
            or super(PolyNum,self)._isnonnegative()
            
    def __le__(self, other):
        """
        self <= other
        see a concept of partially ordered Mikusinski space
        some PNs are not comparable, i.e. ~(self <= other) and ~(self >= other)

        >>> x = PolyNum('(~2.4~,-1.1~-8~)')
        >>> x <= x
        True
        >>> x <= abs(x)
        True
        >>> x <= 2*x
        False
        >>> abs(x) <= 2*abs(x)
        True
        """
        other = PolyNum(other)
        return ( other - self ).isnonnegative()

    def __ge__(self, other):
        """
        self >= other
        see a concept of partially ordered Mikusinski space
        some PNs are not comparable, i.e. ~(self >= other) and ~(self <= other)
        
        >>> x = PolyNum([2.4, 1.1])
        >>> x >= x
        True
        >>> -x >= x
        False
        """
        return ( self - other ).isnonnegative()
        
        
########
        
    def sqrt(self):
        """
        sqrt()
        ========
        >>> y05 = PolyNum([0.1,2.5]).sqrt()
        >>> y05._strPN_cut = 4;  print(y05) #a big difference mpf() with float()!
        (~0.316227766~,3.95284708~-24.7052942~308.816178~...~)
        >>> y1 = y05 * y05
        >>> #using **0.5 gives better result:    PolyNum('(~0.1~,2~0~-1.1234667099445442e-14~0~0~0~...~)')
        >>> y1._strPN_cut = 2; print(y1)
        (~0.1~,2.5~...~)
        """
        if self._exponent and (self.exponent % 2): #odd
            raise ValueError("Does not support sqrt() if exponent is odd: {}.format()self.exponent")
        return PolyNum(super(PolyNum,self).sqrt(), self._exponent // 2)

    def exp(self):
        """
        exp()
        ========
        >>> y1 = PolyNum([0.1,2.]).exp()
        >>> y1._strPN_cut = 7;  print(y1)
        (~1.10517092~,2.21034184~2.21034184~1.47356122~0.736780612~0.294712245~0.0982374149~...~)
        >>> y2 = PolyNum([0.1,2.],-2).exp()
        >>> y2._strPN_cut = 7;  print(y2)
        (~1.0~,0.0~0.1~2.0~0.005~0.2~2.00016667~...~)
        >>> y3 = PolyNum('(~1.~2.~0.)').exp()
        Traceback (most recent call last):
        ... 
        ValueError: Todo(?) - case if exponent (== 2) is positive.
        
        """
        if self._exponent > 0: 
            raise ValueError("Todo(?) - case if exponent (== {}) is positive.".format(self.exponent))
            
        if self._exponent == 0: #it will be common case - do not shrMant()
            return PolyNum(super(PolyNum,self).exp())
        else:
            a2 = PolyNum(self) #copy of a2 mantissa, which will be shifted
            a2._shrMantProc(-a2._exponent) 
            # because of leading zero a2 is treating as (~0~), but i.e.
            # a2.mantissa [0.0, 0.0, 1.0, 2, 3, 0.0, ... 
            return PolyNum(super(PolyNum,a2).exp())


####
    def expZ(self, pZ, T0, h):
        """
        returns exp() with shifted samples
        exp(arg+K·h·pZ) * (~1~0~)^(-K)
        where 
            K = floor( T0 / h )
            T0 - expected pure delay time
            h  - sampling interval
            pZ - numerical Heaviside operator, e.g. 2/h * (~1~-1~)/(~1~1~)
            
        >>> from digitPN import flt
        >>> h = flt('0.3')
        >>> pZ = PolyNum('const:(~2~,-4~4~-4~4~...~)') / h  # 2/h * (~1~-1~)/(~1~1~)
        >>> x1 = (flt('-0.7')*pZ + 1).expZ( pZ, flt('0.7'), h )  # exp(-0.7 p + 1)
        >>> x1._strPN_cut = 7;  print(x1)
        (~1.39561243~,1.86081657~-0.620272189~-0.0689191321~0.390541749~-0.479370852~0.432063399~...~)*(~1~0~)**(-2)
        """
        K = int(digitPN.floor( T0 / h ))
        if not K:
            return self.exp()
        else:
            x = self + K*h*pZ
            return PolyNum(x.exp(), -K)
####

    def ln(self):
        if self._exponent: 
            raise ValueError("Does not support ln() if exponent is nonzero: {}.format()self.exponent")
        return PolyNum(super(PolyNum,self).ln(), self._exponent)
        
        
    def __getitem__(self, index):
        """
        index < 0 is not allowed
        index == i + (-exponent)
        exponent > 0 are not allowed
        useful for Z-transform, like mantissa notmalized to exponent==0, 
            where exponent <= 0; exponent > 0 no allowed
        used in matplotlib.pyplot.plot
        
        For tests set MantPN.QUICK_TEST = 1 i.e. MantPN.max_N = 32 
        >>> x = [ 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15,16,\
                 17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32]
        >>> x1 = PolyNum(x)
        >>> x1[0]
        1
        >>> x2 = PolyNum(x,-2)
        >>> x2[31]
        30
        >>> x3 = PolyNum(x,-3)
        >>> (x3[:])[:32]
        [0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
        >>> x4 = PolyNum(x,4)
        >>> x4[:]
        Traceback (most recent call last):
        ... 
        ValueError: if exponent(=4) is positive, PN slicing is not allowed

        """
        if not self.exponent: #the most common case
            return self.mantissa[index]
        if type(index) is slice:
            if self._exponent > 0: 
                raise ValueError("if exponent(={}) is positive, PN slicing is not allowed".format(self._exponent))
            y = ([0 * self._mantissa[0]] * (-self._exponent)) \
                    + self.mantissa[:self._exponent] # [:-(-self._exponent)]
            return y[index]
        else: # int
            if not 0 <= index < len(self._mantissa): raise IndexError()
            i = index + self._exponent
            #if i < 0 : raise IndexError()
            # ^ ValueError: cannot copy sequence with size 32 to array axis with dimension 0
            #if i >= self._max_N: raise IndexError()
            # ^ ValueError: cannot copy sequence with size 32 to array axis with dimension 33
            # ? if exp == 2
            # ValueError: cannot copy sequence with size 32 to array axis with dimension 30
            if i < 0:
                return 0 * self._mantissa[0] # zero of type m[0]
            else:
                return self.mantissa[i]
     
#     def __setitem__(self, index, val):
#         self._mantissa[index] = val
#         return
 
    def __iter__(self):
        """
        if __iter__ is not defined, then __getitem__ is used for list()
        
        For tests set MantPN.QUICK_TEST = 1 i.e. MantPN.max_N = 32 
        >>> x = [ 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15,16,\
                 17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32]
        >>> x1 = PolyNum(x)
        >>> list(x1)[:32]
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]
        >>> x2 = PolyNum(x,-2)
        >>> list(x2)[:32]
        [0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
        >>> x4 = PolyNum(x,4)
        >>> list(x4)
        Traceback (most recent call last):
        ... 
        ValueError: if exponent(=4) is positive, PN __iter__  is not allowed
        """
        if not self.exponent: #the most common case
            return iter(self.mantissa)
        if self._exponent > 0: 
                raise ValueError("if exponent(={}) is positive, PN __iter__  is not allowed".format(self._exponent))
        y = ([0 * self._mantissa[0]] * (-self._exponent)) \
                    + self.mantissa[:self._exponent] # [:-(-self._exponent)]
        return iter(y)
    
    
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

    def invTr1LaplPN (self, t):
        """
        inp: t :float
        otpt: y, err :float
        
        Examples:
        >>> Yerr = PolyNum('(~1~2~)') 
        >>> Yerr.invTr1LaplPN(1)
        Traceback (most recent call last):
        ... 
        ValueError: PN exponent = 1 > 0 - inverese Laplce transform does not exist.
            
        >>> from digitPN import flt
        >>> Y = 1 / PolyNum('(~1~2~)') # Y(p) =   1 / (p + 2); y(t) = 1 * exp(-2*t)
        >>> h = flt('0.07') 
        >>> t = [tk*h for tk in range(len(Y))] #it sould be any length, but for test ...
        >>> y, err = zip( *(Y.invTr1LaplPN(_t) for _t in t) )
        >>> yPN = PolyNum(y)
        >>> errPN = PolyNum(err)
        >>> yPNok = PolyNum([digitPN.exp(-2*_t) for _t in t])
        >>> #yPN
        >>> #yPNok
        >>> #errPN
        >>> #yPNok - yPN
        >>> #plt.plot(y, 'b-', err, 'r--') 
        >>> import matplotlib.pyplot as plt
        >>> _ = plt.plot(y, 'b-', label='y(t)=(1/(~1~2~)).invTr1LaplPN (t)') 
        >>> _ = plt.plot(err, 'r--', label='err(t)') 
        >>> plt.grid(b=True)
        >>> _ = plt.legend()
        >>> plt.show()

        """
        stop = False
        zero = self._mantissa[0] * 0
        one = zero + 1 #1 of type of zero
        if t < 0:
            return zero, zero
        max_a = zero
        
        ex = self._exponent
        if ex >= 0:
            raise ValueError(
                'PN exponent = {} > 0 - inverese Laplce transform does not exist.'\
                .format(ex))
        if t == 0:
            #return self._mantissa[-ex-1], zero
            #rather set t=0+ = eps/int(1e24)
            t = digitPN.epsilonPNdig / 1000000000000000000000000
            
        wk = one
        for k in range(1, -ex-1+1): # (~0~,0~0~0~0
            wk = wk * t/k
        out= self._mantissa[0] * wk
        abs_a = [abs(out),zero,zero] #ring-array of 3 last abs_ak[0..2]
        dk_maxLocal = -1
        k = 0
        while 1:
            wk = wk * t / (k-ex)
            ak = self._mantissa[k+1] * wk
            abs_ak = abs(ak)
            if (abs_ak > max_a):
                max_a = abs_ak
            abs_a[(k+1) % 3] = abs_ak
            if (abs_a[(k+3-1) % 3] < abs_a[k % 3]) \
                and (abs_a[k % 3] >= abs_a[(k+1) % 3]): # local max is here
                if dk_maxLocal < 0: #start
                    maxLocal = abs_a[k % 3]
                    k_maxLocal = k
                    dk_maxLocal = 0
                else:
                    q_maxLocal = abs_a[k % 3]/maxLocal
                    maxLocal = abs_a[k % 3]
                    dk_maxLocal = k-k_maxLocal
                    k_maxLocal = k
                stop = ( (dk_maxLocal > 0) and (q_maxLocal < 1) 
                        and (maxLocal < abs(out)*digitPN.epsilonPNdig) ) \
                    or \
                    ( (k > k_maxLocal + self._max_N // 4) and (abs_ak < abs(out)*digitPN.epsilonPNdig) )
                    #last line - not oscillatory convergent

            out=out + ak
            k += 1
            if (k >= self._max_N-1) or stop:
                break

        if ( (k <= k_maxLocal+self._max_N // 4) and (dk_maxLocal > 0) and (q_maxLocal < 1) ):
            err = maxLocal * q_maxLocal **((k-k_maxLocal)/dk_maxLocal )
        else:
            err = abs_ak
        err = err + (max_a+out) * digitPN.epsilonPNdig;

        return out, err #end def invTr1LaplPN(self, t)
        
        

###    def invTr05LaplPN (self, t):
###        """
###        inp: t :float
###        otpt: y, err :float
###
###        -- not yet tested
###        """
###        stop = False
###        zero = self._mantissa[0] * 0
###        one = zero + 1 #1 of type of zero
###        if t < 0:
###            return zero, zero
###        max_a = zero
###
###        ex = self._exponent
###        if ex >= 0:
###            raise ValueError(
###                'PN exponent = {} > 0 - inverese Laplce transform does not exist.'\
###                .format(ex))
###
###        mc = -ex % 2
###        pi_ = digitPN.pi
###        if mc == 1:
###            nc = (-ex+1) // 2;
###            wk0 = one / (t*pi_).sqrt()  #1 / sqrt(t*pi)
###            wk1 = one
###            for k in range(1, nc-1+1):
###                wk0 = wk0 * t*2/(2*k-1)
###                wk1 = wk1 * t/k
###        else: # mc == 0
###            nc = -ex // 2;
###            wk0 = one
###            wk1 = one / (pi_).sqrt()
###            for k in range(1, nc-1+1):
###                wk0 = wk0 * t/k
###                wk1 = wk1 * 2*t/(2*k-1)
###            wk1 = wk1 * 2*t.sqrt()/(2*nc-1)
###
###        out = self._mantissa[0] * wk0 + self._mantissa[1] * wk1;
###        abs_a = [abs(out),zero,zero] #ring-array of 3 last abs_ak[0..2]
###        dk_maxLocal = -1
###        k = 0
###        while 1:
###            wk0 = wk0 * t * 2/(k-ex)
###            wk1 = wk1 * t * 2/(k+1-ex)
###            ak = self._mantissa[k+2]*wk0 + self._mantissa[k+1+2]*wk1
###            abs_ak = abs(ak)
###            if (abs_ak > max_a): 
###                max_a = abs_ak
###            abs_a[(k+1) % 3] = abs_ak;
###            if (abs_a[(k+3-1) % 3] < abs_a[k % 3]) \
###               and (abs_a[k % 3] >= abs_a[(k+1) % 3]): # local max is here
###                    if dk_maxLocal < 0: #start
###                        maxLocal = abs_a[k % 3]
###                        k_maxLocal = k
###                        dk_maxLocal = 0
###                    else:
###                        q_maxLocal = abs_a[k % 3]/maxLocal
###                        maxLocal = abs_a[k % 3]
###                        dk_maxLocal = k-k_maxLocal
###                        k_maxLocal = k
###                    stop = ( (dk_maxLocal > 0) and (q_maxLocal < 1) 
###                        and (maxLocal < abs(out)*digitPN.epsilonPNdig) ) \
###                        or \
###                            ( (k > k_maxLocal + self._max_N // 4)and(abs_ak < abs(out)*digitPN.epsilonPNdig) )
###                        #last line - not oscillatory convergent 
###
###            out = out + ak
###            k += 2
###            if (k+2 > self._max_N-1) or stop:
###                break
###
###        if ( (k <= k_maxLocal+self._max_N // 4) and (dk_maxLocal > 0) and (q_maxLocal < 1) ):
###            err = maxLocal * q_maxLocal **((k-k_maxLocal)/dk_maxLocal )
###        else:
###            err = abs_ak
###        err = err + (max_a+out) * digitPN.epsilonPNdig 
###        #? perhaps err is over-estimated
###        return out, err #end def invTr05LaplPN(self, t)
###
####

    def invTr05exp_b0_LaplPN (self, t, b0):
        """
        inp: t, b0 :float
        otpt: out, err :float

        Examples:
        >>> Yerr = PolyNum('(~1~2~)') 
        >>> Yerr.invTr05exp_b0_LaplPN(1, 2)
        Traceback (most recent call last):
        ... 
        ValueError: PN exponent = 1 > 0 - inverese Laplce transform does not exist.
            
        >>> from digitPN import flt
        >>> Y = PolyNum('(~0~,10~20~30~)') # 
        >>> h = flt('0.02') 
        >>> b0 = flt('5')
        >>> t = [(tk+1)*h for tk in range(len(Y))] #it sould be any length, but for test ...
        >>> y, err = zip( *(Y.invTr05exp_b0_LaplPN(_t, b0) for _t in t) )
        >>> def y_ok(t):
        ...     return flt('10')/digitPN.sqrt(digitPN.pi*t)*digitPN.exp(-b0*b0/t/4)+ \
                    flt('20')*digitPN.erfc(b0/digitPN.sqrt(t)/2)+ \
                    flt('60')*digitPN.sqrt(t/digitPN.pi)*digitPN.exp(-b0*b0/t/4)- \
                    flt('30')*b0*digitPN.erfc(b0/digitPN.sqrt(t)/2)
        >>> yOK = PolyNum([y_ok(t_) for t_ in t])
        >>> y = PolyNum(y)
        >>> abs( y - yOK ) <= (digitPN.epsilonPNdig*1024*1024) * PolyNum('const:(~1~,2~2~2~2~...~)')
        True
        >>> #plt.plot(y, 'b-', err, 'r--') 
        >>> import matplotlib.pyplot as plt
        >>> _ = plt.plot(y, 'b-', label='y(t) = (~0~,10~20~30~).invTr05exp_b0_LaplPN (t, b0)') 
        >>> _ = plt.plot(err, 'r--', label='err(t)') 
        >>> plt.grid(b=True)
        >>> _ = plt.legend()
        >>> plt.show()
        """
        stop = False
        zero = self._mantissa[0] * 0
        #one = zero + 1 #1 of type of zero
        if t < 0:
            return zero, zero
        max_a = zero
        ex = self._exponent
        if ex >= 0:
            raise ValueError(
                'PN exponent = {} > 0 - inverese Laplce transform does not exist.'\
                .format(ex))

        ce1 = -ex-1
        pi_ = digitPN.pi
        if (t == 0):
            if (b0 != 0):
                return zero, zero
            # b0==0 and t==0:
            if (ex+2 >= 0):
                out = self._mantissa[ex+2]
                err = zero
            else:
                out = zero
                err = zero
        else: # t > 0
            y = [zero,zero] # ring-array of 2 last values[0..1]
            y[0] = digitPN.exp(-(b0*b0)/(4*t)) / digitPN.sqrt(pi_*t)
            y[1] = digitPN.erfc( b0 / digitPN.sqrt(2*t) / digitPN.sqrt(2+zero) )

            for k in range(1, ce1+1):
                y[(k+1) % 2] = (2*t* y[(k-1) % 2] - b0 * y[k % 2]) / k

            k = ce1
            out = self._mantissa[k-ce1] * y[k % 2]
            abs_a = [0,0,0] #ring-array of 3 last abs_ak[0..2]
            abs_a[(ce1+1 -1) % 3] = 0
            abs_a[(ce1+1 +0) % 3] = abs(out)
            dk_maxLocal = -1
            while 1:
                k += 1
                y[(k+1) % 2] = (2*t* y[(k-1) % 2] - b0 * y[k % 2]) / k
                ak = self._mantissa[k-ce1] * y[k % 2]

                abs_ak = abs(ak)
                if (abs_ak > max_a):
                    max_a = abs_ak
                abs_a[(k+1) % 3] = abs_ak
                if (abs_a[(k+3-1) % 3] < abs_a[k % 3]) \
                    and (abs_a[k % 3] >= abs_a[(k+1) % 3]) : # local max is here
                    if dk_maxLocal < 0: #start
                        maxLocal = abs_a[k % 3]
                        k_maxLocal = k
                        dk_maxLocal = 0
                    else:
                        q_maxLocal = abs_a[k % 3]/maxLocal
                        maxLocal = abs_a[k % 3]
                        dk_maxLocal = k-k_maxLocal
                        k_maxLocal = k
                    stop = ( (dk_maxLocal > 0) and (q_maxLocal < 1) 
                        and (maxLocal < abs(out)*digitPN.epsilonPNdig) ) \
                        or \
                        ( (k > k_maxLocal + self._max_N // 4) and (abs_ak < abs(out)*digitPN.epsilonPNdig) )
                        #last line - for not oscillatory convergent case
                out = out + ak

                if (k >= self._max_N-1 + ce1) or stop:
                    break
                
            if ( (k <= k_maxLocal+self._max_N-1 // 4) and (dk_maxLocal > 0) and (q_maxLocal<1) ):
                err = maxLocal * q_maxLocal **((k-k_maxLocal)/dk_maxLocal)
            else:
                err = abs_ak
        err = err + (max_a+out) * digitPN.epsilonPNdig
        return out, err #invTr05exp_b0_LaplPN()

####
    
    def const_Qu(self, n, a):
        """
        Qu_n(a)
        ==========
        returns PN constants connected with Bessel functions I and K;
        k-th digit (k=0,1,...) = Γ(n+k+(1/2)) / (Γ(n-k+(1/2)) * k! * (2*a) **k) 
        n, a - float, although in practice n=0 and n=1
        
        -- not yet tested
        """
        _4nn = 4*n*n
        mant = self._mantissa[:]
        mant[0] = mant[0]*0 + 1 # 1.0 of type of mant[0]
        for k in range(1, self._max_N):
            mant[k] = mant[k-1] * (_4nn -(2*k-1)*(2*k-1)) / (8*a*k)
        return PolyNum(mant, 0)

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    
###def cerf (x):
###    """
###    otpt: cerf(x), err
###    """
###    zero = x * 0
###    one = zero + 1 #1 of type zero
###    if x == 0:
###        return one, zero
###    # x != 0 :
###    max_I = 2 / digitPN.epsilonPNdig #big float
###    #if x < 4.647:# for 80bits longdouble both alg. gives err=3E-20
###                  #                  przy wartosci cerf=4.9693771E-11 (tylko 9 cyfr istotnych)}
###    # try algorithm for small x value first
###    pi_ = digitPN.pi
###    wk0 = -(x*x).exp() * 2 * x / pi_.sqrt()
###    out1 = wk0
###    k = 1
###    while 1:
###        wk0 = wk0 * 2*x.sqr() / (2*k+1)
###        stop = (abs(wk0) * max_I < abs(out1))
###        out1 = out1 + wk0
###        k += 1
###        if stop:   #or (k+2 > max_N)
###            break
###    cerf0 = 1-out1
###    err0 = abs(wk0)
###    if err0/abs(out1) > 10*digitPN.epsilonPNdig:
###        #try for big x value
###        wk0 = -(x*x).exp() / (pi_.sqrt()*x)
###        out = wk0
###        abs_wk0 = abs(wk0)
###        k = 1 
###        while 1:
###            wk0 = wk0 * (2*k-1)/(-2*x*x)
###            stop = (abs(wk0) > abs_wk0)
###            if stop:
###                #neutralize last added item:
###                out = out - wk0 * (-2*x*x)/(2*k-1)
###            else:
###                abs_wk0 = abs(wk0)
###                stop = (abs_wk0 * max_I < abs(out))
###                out = out + wk0
###                k += 1
###            if stop:   #or (k+2 > max_N)
###                break
###        cerf111 = out
###        err111 = abs_wk0
###        if err111 < err0:
###            cerf0, err0 = cerf111, err111
###    return cerf0, err0 # cerf()


#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

def getMantissaExponent_fromStr(s, sep, max_N):
    '''
    max_N is used to generate constatnts
    '~,~' is equivalent to '~,'
    Some test are also near __init__
    >>> PolyNum('(~1.2~,2.2~-0.3~)*(~1~0~)**(2)')
    PolyNum('(~1.2~,2.2~-0.3~)*(~1~0~)**(2)')
    >>> PolyNum('(~1.2~,2.5~-0.3~)')
    PolyNum('(~1.2~,2.5~-0.3~)')
    >>> PolyNum('(~1.2~,~2.5~-0.3~)')
    PolyNum('(~1.2~,2.5~-0.3~)')
    >>> PolyNum('(~1.2~)')
    PolyNum('(~1.2~)')
    >>> PolyNum('(~0~,2.5~-0.3~)')
    PolyNum('(~2.5~,-0.3~)*(~1~0~)**(-1)')
    >>> PolyNum('(~,2.5~-0.3~)')
    PolyNum('(~2.5~,-0.3~)*(~1~0~)**(-1)')
    >>> PolyNum('(~-1.1~2.2~,-3.3~)')
    PolyNum('(~-1.1~,2.2~-3.3~)*(~1~0~)**(1)')
    '''
    if not s:
        return [], 0
    me = s.replace(" ", "").split('**')
    if len(me) > 2:
        raise ValueError(
            "{!r} error - only 1 exponent allowed here.".format(s))
    if len(me) > 1:
        expo = int(me[1].strip('()')) # -2
    else:
        expo = 0
    mLR_ = me[0].split('*')[0] # '(~1.2~,2.~-0.3~)' - ignore '*(~1~0~)'
    
    # const 
    if mLR_[0] == 'c':
        mant = []
        if mLR_ == 'const:(~2~,-4~4~-4~4~...~)':
            for __ in range(max_N//2):
                mant.extend([4,-4])
            mant[0] = 2
        elif mLR_ == 'const:(~1~,2~2~2~2~...~)':
            mant = [1] + [2 for __ in range(max_N-1)]
        else:
            raise ValueError(
            "{!r} error - unknow PN const format.".format(s))
        return mant[:max_N], expo
    
    # values
    mLR_ = mLR_.replace(sep+',','`,') # '(~1.2`,2.~-0.3~)' (for case '(`,2.~-0.3~)')
    mLR = mLR_.strip('()'+sep).split('`,') # ['1.2`, '2.~-0.3']
    if not mLR[0]: #ex. for input '`,2.~-0.3' -> mLR[0] == ''
        mL=['0']
    else:
        mL = mLR[0].split(sep)
    expo += len(mL) - 1 #ex. for input '(~-1.~2.2~,-3.3~)' -> expo += 1
    if len(mLR) > 1:
        # mLR_.strip(sep)  '~,~' case -> '~...
        mR = mLR[1].strip(sep).split(sep) # ['2.', '-0.3']
    else:
        mR = []
    m = mL + mR # ['1.2', '2.', '-0.3']
    # mant = [float(d) for d in m]
    mant = [digitPN.flt(d) for d in m]
    return mant, expo




#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

if __name__ == "__main__":
    #print(getMantissaExponent_fromStr('','~',32)) # ([], 0)
    #print(getMantissaExponent_fromStr('0','~',32)) #([0.0], 0)
    #print(getMantissaExponent_fromStr('(~,2.~-0.3~)','~',32)) # ([0.0, 2.0, -0.3], 0)
    #print(getMantissaExponent_fromStr('(~,2.~-0.3~)','~',32)) # ([0.0, 2.0, -0.3], 0)
    #print(getMantissaExponent_fromStr('c(~','~',32)) # ValueError: 'c(~' error - unknow PN const format.
    #print(getMantissaExponent_fromStr('const:(~2~,-4~4~-4~4~...~)','~',32)) #
    #print(getMantissaExponent_fromStr('const:(~1~,2~2~2~2~...~)','~',32)) #

#    p1 = PolyNum([1.,2,3],-3)
#    p2 = PolyNum([10.,20,30],-1)
#    print(p1,p2)
#    p3 = p1 +p2
#    print(p3)

#    from numpy.testing import (
#        run_module_suite, assert_, assert_equal, assert_array_equal,
#        assert_almost_equal, assert_array_almost_equal, assert_raises, 
#        rundocs
#        )
#    rundocs(); print('OK.')

     import doctest
     doctest.testmod(); print('OK.') #sometimes kernel restart is needed...
    
    #print(PolyNum([1,2,3]))
    #print(PolyNum(''))
    
    #import numpy as np
    #print(1 + np.finfo(np.longdouble).eps) #1.0000000000000002
    # np.finfo(np.longdouble).eps == 2.220446049250313e-16
    
    # v=1.0; resolution=1.0/1024
    # while (v+resolution > v ): resolution = resolution/2
    # resolution = resolution*2     #2.220446049250313e-16
    
    #import sys
    #print(sys.float_info)
    #sys.float_info(max=1.7976931348623157e+308, max_exp=1024, max_10_exp=308, min=2.2250738585072014e-308, min_exp=-1021, min_10_exp=-307, dig=15, mant_dig=53, epsilon=2.220446049250313e-16, radix=2, rounds=1)    