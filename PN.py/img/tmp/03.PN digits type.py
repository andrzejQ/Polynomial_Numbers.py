
# coding: utf-8

# ## Floatingpoint operations
# 
# *(this chapter is not important on first contact with Polynomial Numbers)*
# 
# `PolyNum` class is ready to use different floating point format of PN digits. See `PolyNumConf.py`. To have homogeneous type of float calculations, for example `mpf` from `mpmath`, use the same type for scalars using strings to initialize all scalars and all PNs. Recommended starting precision: mpmath -> mp.prec = 128  (38 dec. significant dig. of float), max_N=64 or 128 (PN significant digits number).
#     

# In[1]:


from PNlib import PolyNumConf
PolyNumConf.max_N=80 # PN significant digits number (restart jupyter kernel on change conf.)
PolyNumConf.FLOAT_TYPE = 'FLOAT-MPMATH-MPF'
PolyNumConf.MPMATH_PREC = 150
#PolyNumConf const can be changed efficiently before loading any other PNlib files


# In[2]:


from PNlib.digitPN import flt
#example: h = flt('0.1') - Use it for all scalars.
print(repr(flt('0.1')))                 # ...9982')


# In[3]:


from PNlib.PolyNum import PolyNum
print(repr(PolyNum().mantissa[0]))


# ### Example

# In[4]:


# Z-transform live example of homogeneous type of float calculations (to set in PolyNumConf.py)
h = flt('0.01') # sampling period
p = 1/h * PolyNum('const:(~2~,-4~4~-4~4~...~)') #intiger can be mixed with mpf float
E_0 = flt('10')
E = E_0/2 * PolyNum('const:(~1~,2~2~2~2~...~)') # flt('10')/2, but not 10/2
R, L, C = flt('20'), flt('2'), flt('1e-3')
Z_C = 1 / (p*C)
Z = R + p*L + Z_C
U_C = E * Z_C / Z


# In[5]:


# plt.plot(E, 'r--',U_C, 'b-') 
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
plt.plot(E, 'r--',U_C, 'b-')
plt.grid(b=True)
plt.text(0.6,10.4,"$ e(t) $", fontsize=16, color='red')
plt.text(21,12.2,"$ u_C(t) $", fontsize=16, color='blue')
plt.show();


# In[7]:


print(repr(U_C.mantissa[0])) #to see float type


# - - - -
# [<<<... 02. PN Laplace and Z transforms ...](02.PN Laplace and Z transforms.ipynb) _ | _ [... 04. PN generalized time domain functions ...>>>](04.PN generalized time domain functions.ipynb)
