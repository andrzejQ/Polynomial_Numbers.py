
# coding: utf-8

# In[1]:


# -*- coding: utf-8 -*-
####  -*- coding: future_fstrings -*-   in py 2.7 for f-strings like in 3.6 (not tested here)


# In[2]:


from PNlib.PolyNum import PolyNum
# place folder `PNlib` near to *.ipynb


# As well PN operations as PN functions have easy computer implementation and are analogous to the floating-point arithmetic.

# In[3]:


a = PolyNum('(~-3.2~,-5.0~2.1~)') #live demo
b = PolyNum('(~-0.1~,1.0~)')


# In[5]:


# print() ___ R ___ PN ___  # Codefolding extension
print()
print('________ R _________','  ______________ PN ___________________')
print()
print('  a =       5.3 2    |   ', 'a =',                 f'{a:>28}')
print('  b =         2.1    |   ', 'b =',                 f'{b:>28}')
print('  * -------------    |   ','* ------------------------------')
print('            5 3 2    |   ',                   f'{a*b[1]:>32}')
print('        1 0 6 4      |   ',          f'{a*b[0]:>27}'         )
print('  a * b =========    |   ','a * b ==========================')
print('        1 1.1 7 2    |   ',                    f'{a * b:>32}')


# - - - -
# [<<<... 00. index ...](../index.ipynb) _ | _ [... 02. PN Laplace and Z transforms ...>>>](02.PN Laplace and Z transforms.ipynb)
