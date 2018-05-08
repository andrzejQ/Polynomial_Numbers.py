# -*- coding: utf-8 -*-
"""
PolyNum configuration
=====================
max_N = 64   #or 128 or 100 ..., 32 is mimnimum for doctest
    PN mantissa length i.e. PN significant digits number
    - is fixed as class attr. in `_max_N` in MantPN (->PolyNum) class definition.
    It can be changed before importing PolyNum.
    2**(N) - efficient for inversion and sqrt
    
sep = '~' # in PolyNum str() and repr()
    - is fixed as class attr. `_sep` in PolyNum class definition

FLOAT_TYPE = 'FLOAT-PYTHON' # 'FLOAT-MPMATH-MPF' # 'FLOAT-NUMPY'
    used in digitPN to define type and some finctions.
    Recommended float precision: mpmath -> mp.prec = 128,
    max_N=64 or 128 (PN significant digits number).
    For quick start with Polynomial numbers `FLOAT-PYTHON` is used.

MPMATH_PREC = 128   #38 dec. siginicant dig. if FLOAT_TYPE = 'FLOAT-MPMATH-MPF'

"""

__all__ = ['max_N','sep', 'FLOAT_TYPE', 'MPMATH_PREC']

max_N = 64   #or 128 or 100 ..., 32 is mimnimum for doctest - PN significant digits number

sep = '~' # in PN str() and repr()

FLOAT_TYPE = 'FLOAT-PYTHON'
#FLOAT_TYPE = 'FLOAT-MPMATH-MPF'
#FLOAT_TYPE = 'FLOAT-NUMPY'

MPMATH_PREC = 128   #38 dec. siginicant dig.
