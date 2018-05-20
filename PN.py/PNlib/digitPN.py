# -*- coding: utf-8 -*-
"""
PolyNum digits type
===================

flt(digStr)
    Define default type of PN didits if PN value is based on string (or other 
        value converting to float type)
    Use it also for scalars, to have homogeneous type of float numbers:
        from digitPN import flt; x = flt('0.1')
    PN digits can be of an arbitrarty type field, for which inertactions with 
    int are determined: 0*x, 0*x+1 (zero and one of x-type), 1/x (inversion of 
    x-type). Type of first mantissa digit is propagated for next digits 
    in results of functions.

strF(dig, chop_=True, signifi_=9), reprF(): strF(dig, chop_=False, signifi_=15)
    string for for PolyNum.mantissa digits (for kind of float) in str(), repr(). 

zeroPNdig, onePNdig = flt('0'), flt('1')
   
epsilonPNdig 
    difference between 1 and the least value greater than 1 
    that is representable as a float

PNdig_isclose(a, b, rel_tol=epsilonPNdig*128, abs_tol=epsilonPNdig*128)
    compare equality of two PolyNum.mantissa digits
"""
from __future__ import division
__all__ = ['flt', 'strF', 'reprF', 'epsilonPNdig', 'onePNdig', 'zeroPNdig', 
           'PNdig_isclose']


if __name__ == '__main__' or __name__ == 'digitPN': 
    #standalone tests: digitPN -> rundocs(), doctest
    import PolyNumConf
else: #relative package import
    #print(f'''__nm__ = {__name__}''')
    from . import PolyNumConf

#in PolyNumConf:
#FLOAT_TYPE = 'FLOAT-MPMATH-MPF' # 'FLOAT-PYTHON' # 'FLOAT-NUMPY'
#MPMATH_PREC = 128   #38 dec. siginicant dig.
# =============================================================================
if PolyNumConf.FLOAT_TYPE == 'FLOAT-PYTHON':
# =============================================================================
    import sys
    import math
    epsilonPNdig = sys.float_info.epsilon #=2**-52 = 2.220446049250313e-16
    def flt(digStr):
        return(float(digStr))
    def strF(dig, chop_=True, signifi_=9):
        if dig and chop_: dig = chop(dig)
        try: return dig.__format__('1.'+str(signifi_)) #'1.9'
        except (ValueError, TypeError): return str(dig) 
            #without formatting (i.e. for int,  TypeError - for Fraction)
    
    floor = math.floor
    sqrt  = math.sqrt
    exp   = math.exp
    log   = math.log
    erfc  = math.erfc
    pi    = math.pi
# =============================================================================
elif PolyNumConf.FLOAT_TYPE == 'FLOAT-MPMATH-MPF':
# =============================================================================
    from mpmath import mp, mpf
    mp.prec = PolyNumConf.MPMATH_PREC #128  #38 dec. siginicant dig.
    epsilonPNdig = mpf(2)**(-mp.prec+1) #mp.epsilon 5.88e-39
    def flt(digStr):
        return(mpf(digStr))
    def strF(dig, chop_=True, signifi_=9):
        if dig: dig = chop(dig)
        return mp.nstr(dig,signifi_)
    
    floor = mp.floor
    sqrt  = mp.sqrt
    exp   = mp.exp
    log   = mp.log
    erfc  = mp.erfc
    pi    = mp.pi
# =============================================================================
elif PolyNumConf.FLOAT_TYPE == 'FLOAT-NUMPY':
# =============================================================================
    import numpy as np
    from scipy.special import erfc
    epsilonPNdig = np.finfo(np.longdouble).eps #2.220446049250313e-16
    def flt(digStr):
        return(float(digStr))
    def strF(dig, chop_=True, signifi_=9):
        if dig and chop_: dig = chop(dig)
        try: return dig.__format__('1.'+str(signifi_)) #'1.9'
        except (ValueError, TypeError): return str(dig) 
            #without formatting (i.e. for int,  TypeError - for Fraction)
    
    floor = np.floor
    sqrt  = np.sqrt
    exp   = np.exp
    log   = np.log
    erfc  = erfc
    pi    = np.pi
# =============================================================================
else: #todo for yourself...
# =============================================================================
    def flt(digStr):
        return(float(digStr))
    def strF(dig):
        if dig: dig = chop(dig)
        try: return dig.__format__('1.9') 
        except (ValueError, TypeError): return str(dig) 
            #without formatting (i.e. for int,  TypeError - for Fraction)
    def getEpsilon(one):
        v=one; epsilon=one/1024
        while (v+epsilon > v ): epsilon = epsilon/2
        return epsilon*2     #2.220446049250313e-16 for double
    epsilonPNdig = getEpsilon(1.0)
    #...
# =============================================================================

# =============================================================================
# universal `reprF`, `zeroPNdig`, `onePNdig` and `PNdig_isclose`

def reprF(dig):
    """
    repr() of PN digit
    """
    # return repr(dig)
    return strF(dig, chop_=False, signifi_=15)

zeroPNdig = flt('0') # flt('0') #zero of type of PN digits
onePNdig  = flt('1')
def chop(d, tol=epsilonPNdig*1024*1024, zero=zeroPNdig):#tol: 6e-33 by eps=6e-39
        """
        Converts x close to zero to exact zero        
        """
        if (abs(d) > tol):
            return d 
        else:
            return zero
    
def PNdig_isclose(a, b, rel_tol=epsilonPNdig*128, abs_tol=epsilonPNdig*128): 
    """
    Like `math.isclose` or `mpmath.almosteq` - for an arbitrary types a, b
    Return :
    True if a - b == 0 or |a - b| <= abs_tol
    else
        if (|a-b| and rel_tol) are compatybile type: 
            |a-b| <= rel_tol*max(|a|,|b|)
        else: 
            raise NotImplementedError 
    """
    if not a and not b: 
        return True
    diff = abs(a - b)
    if not diff:
        return True
    if diff <= abs_tol:
        return True
    absMax, abs2 = abs(a), abs(b)
    if absMax < abs2:
        absMax = abs2
    if isinstance(diff,type(rel_tol)):
        return diff <= rel_tol * absMax
    raise NotImplementedError 


if __name__ == "__main__":
    print(strF(zeroPNdig))  
    print(repr(zeroPNdig))
#    import doctest
#    doctest.testmod(); print('OK.')