
# coding: utf-8

# In[54]:


# place folder `PNlib` near to *.ipynb
# --- "04y.PN generalized time domain functions.ipynb"  ---- XXy - plotly version ----
from PNlib import PolyNumConf
PolyNumConf.max_N=32 # PN significant digits number (restart jupyter kernel on change)


# In[55]:


from PNlib.PolyNum import PolyNum


# # Discrete representations of generalized time domain functions
# 
# ## Laplace transform
# 
# The functions of continuous time defined for $t \geq 0$, can be expressed in **Mikusinski's operational calculus** in form of functions of **Heaviside's operator** $ p = \cfrac{1}{\int_0^t} $ where $X(p)$ denote $\color{magenta}{\text{Laplace transform}}$ formulas: 
# 
# $$
# \{ x (t) \} = \color{magenta}{X(p)} \color{brown}{ \cdot p \cdot \{1\} }
# $$
# 
# $ \{1\} $ denotes function, with value $ 1 $ for all $ t \geq 0 $.
# 
# For example $ \{ 200\ sin(t) \} = \color{magenta}{200\ \cfrac{2}{p^2 + 4}} \color{brown}{  \cdot  p \cdot \{1\} }$.
# 
# ##  Z-transform
# 
# Z-transform corresponds to $ \{ x (t) \} $ is determined by series of samples in discrete time $ t_k = k\ h $, where $ k = 0, 1,\dots$ and $ h $ is the sampling period:
# 
# $$
# \underline{x} = (^\sim x_0\!^\sim, x_1\!^\sim x_2\!^\sim \dots ^\sim) = \left.(x_0 \,z^0 + x_1 \,z^{-1} + x_2 \,z^{-2} + \dots)\right|_{z\,=\,(^\sim 1 ^\sim 0 ^\sim)}\\
# $$
# 
# Replacing continuous time function $\{1\}$ by sequence of samples $
# (^\sim 0.5^\sim, 1^\sim 1^\sim1^\sim \dots^\sim)
# $
# and replacing Heaviside operator $ p $ utilizing algorithm of numerical integration
# $$
# \underline{p} = \frac{2}{h} \left.\frac{1 - z^{-1}}{1 + z^{-1}}\right|_{z = (^\sim 1 ^\sim 0 ^\sim)} 
# = \frac{2}{h} \frac{(^\sim 1 ^\sim , -1 ^\sim)}{(^\sim 1 ^\sim , 1 ^\sim)}
# = \frac{1}{h}\ (^\sim 2^\sim, -4^\sim 4^\sim -4^\sim \dots^\sim) \\
# $$
# we obtain expression for approximate sequence of samples of function $\{ x(t) \}$:
# 
# 
# $$
# \\
# \underline{x} = \color{magenta}{X (\underline{p})} \color{brown}{  \cdot \underline{p} \cdot (^\sim0.5^\sim, 1^\sim1^\sim1^\sim \dots ^\sim) }
# $$

# This way we get discrete samples of abstract functions, like derivative of non-smooth function, like  
# $
# \{x_a(t)\} = \{ \cfrac{\mathrm{d}}{\mathrm{d}t} \delta(t) \} = \color{brown}{ p \cdot \{1\} \cdot \ } \color{magenta}{p} 
# $, 
# where Laplace transform  $ \color{magenta}{X(p) = p} $ or function containing negative delay, like  
# $
# \{x_b(t)\} = \color{brown}{ p \cdot \{1\} \cdot \ } \color{magenta}{ \cfrac{1}{p^2 + p + 4}\ \exp(-(-0.1)\sqrt{p^2 +1}) } 
# $ 
# (see
# [Mikusinski's remarks about negative delay operator](http://www.pei.prz.edu.pl/~kubaszek/smacd06/JM_OperCalc.html)).

# In[56]:


# Z-transform (live example):
f_1111 = 0.5 * PolyNum('const:(~1~,2~2~2~2~...~)')
p_tr = PolyNum('const:(~2~,-4~4~-4~4~...~)') # 2*(~1~-1~)/(~1~1~)


# ### Digital samples of derivative of the step function:
# 
# $
# \{x_a(t)\}  = \{ \cfrac{\mathrm{d}}{\mathrm{d}t} \delta(t) \} = \color{brown}{ p \cdot \{1\} \cdot \ } \color{magenta}{p} 
# $

# In[57]:


h_a = [0.4,0.8] # diffrent sampling periods for graphs
x_a = []
for h in h_a:  # diffrent sampling periods
    p = 1/h * p_tr
    x_a += [ p * f_1111 * p ]


# In[58]:


# --- "04y.PN generalized time domain functions.ipynb"  ---- plotly version ----
import plotly.plotly as py
import plotly.graph_objs as go
style = [{"line": {"color": "rgba (255, 0, 0, 1)", "dash": "6px,3px", "width": 0.8}, 
    "marker": {"color": "#FF0000", "size": 6.0, "symbol": "dot"}, "mode": "lines+markers"
    },
    {"line": {"color": "rgba (0, 0, 255, 1)", "dash": "solid", "width": 0.8}, 
    "marker": {"color": "#0000FF", "size": 6.0, "symbol": "diamond"}, "mode": "lines+markers"
    }]


# In[59]:


traces = []
for n, h in enumerate(h_a):  # diffrent sampling periods
    traces += [go.Scatter( y=list(x_a[n]), x0=0, dx=h, name='h='+str(h), **style[n] )]
    
layout = go.Layout(autosize=False, width=800, height=220,
    margin=go.Margin(l=50, r=50, b=20, t=0, pad=4),
    yaxis=dict(range=[-35, 35]), xaxis=dict(title='t')
)
fig = go.Figure(data=go.Data(traces), layout=layout)
py.iplot(fig, filename='x_a__h')


# - - - -

# ### Digital samples of signal containing negative delay operator:
# 
# $
# \{x_b(t)\} = \color{brown}{ p \cdot \{1\} \cdot \ } \color{magenta}{ \cfrac{1}{p^2 + p + 4}\ \exp(-(-T_0)\sqrt{p^2 +1}) } 
# $
# 
# $ \color{magenta}{ T_0 = 0.04 } $

# In[ ]:


h_b = [0.15,0.2] # diffrent sampling periods for graphs
x_b = []
T_0 = 0.04
for h in h_b:
    p = 1/h * p_tr
    x_b += [ p * f_1111 * 1 / (p**2 + p + 4) * ( -(-T_0) * ( (p**2 +1).sqrt() ) ).exp() ]


# In[ ]:


traces = []
for n, h in enumerate(h_b):  # diffrent sampling periods
    traces += [go.Scatter( y=list(x_b[n]), x0=0, dx=h, name='h='+str(h), **style[n] )]
    
layout = go.Layout(autosize=False, width=800, height=300,
    margin=go.Margin(l=50, r=50, b=30, t=0, pad=4),
    yaxis=dict(range=[-0.5, 0.5]), xaxis=dict(title='t')
)
fig = go.Figure(data=go.Data(traces), layout=layout)
py.iplot(fig, filename='x_b__h')


# Neutralizing negative delay operator we get regular function for $t \geq 0$
#  (see the last part of [Mikusinski's remarks about negative delay operator](http://www.pei.prz.edu.pl/~kubaszek/smacd06/JM_OperCalc.html)):

# $ \{x_b(t)\} = \color{brown}{ p \cdot \{1\} \cdot \ } \color{magenta}{ \cfrac{1}{p^2 + p + 4}\ \exp(-(-T_0)\sqrt{p^2 +1}) \cdot \exp(-T_0\, p)} $
# 
# $ \color{magenta}{ T_0 = 0.04 } $

# In[ ]:


x_b0 = []
for h in h_b:
    p = 1/h * p_tr
    x_b0 += [ p * f_1111 * 1 / (p**2 + p + 4) * ( -(-T_0) * ( (p**2 +1).sqrt() ) ).exp() * (-T_0*p).exp() ]


# In[ ]:


# plt.plot(x_b0) 
#plt.ylim((-0.5, 0.5))
traces = []
for n, h in enumerate(h_b):  # diffrent sampling periods
    traces += [go.Scatter( y=list(x_b0[n]), x0=0, dx=h, name='h='+str(h), **style[n] )]
    
layout = go.Layout(autosize=False, width=800, height=300,
    margin=go.Margin(l=50, r=50, b=30, t=0, pad=4),
    yaxis=dict(range=[-0.5, 0.5]), xaxis=dict(title='t')
)
fig = go.Figure(data=go.Data(traces), layout=layout)
py.iplot(fig, filename='x_b0__h')


# - - - -
# [<<<... 03. PN digits type ...](03.PN digits type.ipynb) _ | _ [... 05. PN - Black box ...>>>](05.PN - Black box.ipynb)
