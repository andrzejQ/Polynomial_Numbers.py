# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, print_function, unicode_literals
#but tested only in python 3.6+

#CPy: float: 0.024s, mp: 0.42s
#iPy: float: 0.020s, mp: 0.36s


import digitPN
from PolyNum import PolyNum

def testSpeed():
    PolyNum()
    PolyNum('(~1.2~,2.5~-0.3~)*(~1~0~)**(-2)')
    PolyNum('(~1.2~)')
    PolyNum('(~0~,2.5~-0.3~)')
    PolyNum('(~,2.5~-0.3~)')
    PolyNum('(~-1.1~2.2~,-3.3~)')
    # p_trap(h) == (2/h) * (~1~-1~) / (~1~1~) == (1/h) * (~2~,-4~4~-4~4~...~)
    y1=PolyNum('const:(~2~,-4~4~-4~4~...~)'); y1._strPN_cut = 7;  y1
    # flat samples ready to multiply by (a/2):
    y2=PolyNum('const:(~1~,2~2~2~2~...~)'); y2._strPN_cut = 7;  y2
    p1 = PolyNum([1.1,2,3],-2); p1
    p2 = PolyNum(p1, 12); p2
    PolyNum('(~0.1~,2e-38~4.3~6.1e-10~)').chop()
    PolyNum('(~1e-36~,2e-38~4.3~6.0~)').chop()
    p = PolyNum([3.,0,1,2])
    p(5.)  # 3. * 5.**0 + 0 * 5.**(-1)1 + 1 * 5.**(-2) + 2 * 5.**(-3)
    p1 = PolyNum([3.,0,1,2],-2)
    p1(5.)
    ### p(PolyNum([5.]))  # 3. * 5.**0 + 0 * 5.**(-1)1 + 1 * 5.**(-2) + 2 * 5.**(-3)
    # not important case, consuming long time
    PolyNum([1.,2,3],-2) * 100
    PolyNum([1.,2,3],-2) * PolyNum([0.1,2],-5)
    PolyNum([0.1,2],-5) * PolyNum([1.,2,3],-2)
    100 * PolyNum([1.,2,3],-2) #__rmul__ test
    p1 = PolyNum([1.,2,3],-2) #__imul__   test 
    p1 *= PolyNum([0.1,2],-5)
    p1     
    p100 = 100. #__imul__   test 
    p100 *= PolyNum([0.1,2],-5)
    p100     
    y1 = PolyNum([1.,0.2,0.3],-2) / PolyNum([0.1,0.2],-5)
    y1._strPN_cut = 7; str(y1)
    y2 = PolyNum('(~0.1~,0.2~)',-5) / PolyNum('(~1.~,0.2~0.4~)',-2)
    y2._strPN_cut = 7; str(y2)
    PolyNum([1.,0.2,0.3],-2) / 100
    y3 = 100 / PolyNum('(~1.~,0.2~0.3~)',-2) #__rdiv__ test
    y3._strPN_cut = 7; y3
    p1 = PolyNum([1.,0.2,0.3],-2) #__idiv__   test 
    p1 /= PolyNum([0.1,0.2],-5)
    p1._strPN_cut = 7; p1     
    p100 = 100. #__idiv__   test 
    p100 /= PolyNum([0.1,0.2],-5)
    p100._strPN_cut = 7; p100     
    PolyNum('(~1~,2~3~)') + PolyNum('(~10~,20~30~)')
    PolyNum('(~1~,2~3~)*(~1~0~)**(-3)') + PolyNum('(~10~,20~30~)*(~1~0~)**(-1)')
    PolyNum('(~1~,2~3~)*(~1~0~)**(-3)') + 100
    PolyNum('(~1~2~3~)') + 100
    100 + PolyNum([1.,2,3],-2) #__radd__ test
    p1 = PolyNum([1.,2,3],-2) #__iadd__   test 
    p1 += PolyNum([0.1,5],-4)
    p1     
    p100 = 100. #__iadd__   test 
    p100 += PolyNum([0.1,2],-4)
    p100     
    PolyNum('(~1~,2~3~)') - PolyNum('(~10~,20~30~)')
    PolyNum('(~1~,2~3~)*(~1~0~)**(-3)') - PolyNum('(~10~,20~30~)*(~1~0~)**(-1)')
    PolyNum('(~1~,2~3~)*(~1~0~)**(-3)') - 100
    PolyNum('(~1~2~3~)') - 100
    100 - PolyNum([1.1,2,3],-2) #__radd__ test
    p1 = PolyNum([1.1,2.5,3],-2) #__iadd__   test 
    p1 -= PolyNum([0.1,5.1],-4)
    p1     
    p100 = 100. #__iadd__   test 
    p100 -= PolyNum([0.1,2],-4)
    p100     
    xx = PolyNum('(~0.1~,2.0~)')
    y0 = 1 / xx
    y0._strPN_cut = 5
    y0
    y1 = xx **(-1)
    y1._strPN_cut = 5
    y1
    y0xx = (y0 * xx); y0xx._strPN_cut = 22; y0xx
    y1xx = (y1 * xx); y1xx._strPN_cut = 22; y1xx
    abs(PolyNum('(~2.4~,-1.1~-8.8~)'))
    x = PolyNum('(~2.4~,-1.1~-8~)')
    x.isnonnegative()
    abs(x).isnonnegative()
    PolyNum(0.0).isnonnegative()
    x <= x
    x <= abs(x)
    x <= 2*x
    abs(x) <= 2*abs(x)
    x = PolyNum([2.4, 1.1])
    x >= x
    -x >= x
    y05 = PolyNum([0.1,2.5]).sqrt()
    y05._strPN_cut = 4;
    y1 = y05 * y05
    #using **0.5 gives better result:    PolyNum('(~0.1~,2~0~-1.1234667099445442e-14~0~0~0~...~)')
    y1._strPN_cut = 2; 
    y1 = PolyNum([0.1,2.]).exp()
    y1._strPN_cut = 7;  
    y2 = PolyNum([0.1,2.],-2).exp()
    y2._strPN_cut = 7;  
    from digitPN import flt
    h = flt('0.3')
    pZ = PolyNum('const:(~2~,-4~4~-4~4~...~)') / h  # 2/h * (~1~-1~)/(~1~1~)
    x1 = (flt('-0.7')*pZ + 1).expZ( pZ, flt('0.7'), h )  # exp(-0.7 p + 1)
    x1._strPN_cut = 7;  
    x = [ 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15,16,\
                     17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32]
    
    x1 = PolyNum(x)
    x1[0]
    x2 = PolyNum(x,-2)
    x2[31]
    x3 = PolyNum(x,-3)
    (x3[:])[:32]
    x4 = PolyNum(x,4)
    x = [ 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15,16,\
                     17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32]
    x1 = PolyNum(x)
    list(x1)[:32]
    x2 = PolyNum(x,-2)
    list(x2)[:32]
    x4 = PolyNum(x,4)
    x4
    from digitPN import flt
    Y = PolyNum('(~0~,10~20~30~)') # 
    h = flt('0.02') 
    b0 = flt('5')
    t = [(tk+1)*h for tk in range(len(Y))] #it sould be any length, but for test ...
    y, err = zip( *(Y.invTr05exp_b0_LaplPN(_t, b0) for _t in t) )
    def y_ok(t):
        return flt('10')/digitPN.sqrt(digitPN.pi*t)*digitPN.exp(-b0*b0/t/4)+ \
                    flt('20')*digitPN.erfc(b0/digitPN.sqrt(t)/2)+ \
                    flt('60')*digitPN.sqrt(t/digitPN.pi)*digitPN.exp(-b0*b0/t/4)- \
                    flt('30')*b0*digitPN.erfc(b0/digitPN.sqrt(t)/2)
    yOK = PolyNum([y_ok(t_) for t_ in t])
    y = PolyNum(y)
    abs( y - yOK ) <= (digitPN.epsilonPNdig*1024*1024) * PolyNum('const:(~1~,2~2~2~2~...~)')
    PolyNum('(~1.2~,2.2~-0.3~)*(~1~0~)**(2)')
    PolyNum('(~1.2~,2.5~-0.3~)')
    PolyNum('(~1.2~,~2.5~-0.3~)')
    PolyNum('(~1.2~)')
    PolyNum('(~0~,2.5~-0.3~)')
    PolyNum('(~,2.5~-0.3~)')
    print(PolyNum('(~-1.1~2.2~,-3.3~)'))
    
if __name__ == "__main__":
    print(type(PolyNum('~0~')[0])) #type (mantissa[0])
    import timeit
    setup = "from __main__ import testSpeed"
    print( timeit.timeit( "testSpeed()", setup=setup, number=10) )
