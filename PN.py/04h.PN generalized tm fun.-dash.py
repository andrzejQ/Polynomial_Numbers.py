# -*- coding: utf-8 -*-
import dash  # http://localhost:8050/ #interactive graphs like 04.PN...ipynb, but without mathJax
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from PNlib import PolyNumConf
PolyNumConf.max_N=32 # PN significant digits number (restart jupyter kernel on change)
from PNlib.PolyNum import PolyNum

# Z-transform (live example):
f_1111 = 0.5 * PolyNum('const:(~1~,2~2~2~2~...~)')
p_tr = PolyNum('const:(~2~,-4~4~-4~4~...~)') # 2*(~1~-1~)/(~1~1~)

import plotly.plotly as py
import plotly.graph_objs as go
style = [{"line": {"color": "rgba (255, 0, 0, 1)", "dash": "6px,3px", "width": 0.8}, 
    "marker": {"color": "#FF0000", "size": 6.0, "symbol": "dot"}, "mode": "lines+markers"
    },
    {"line": {"color": "rgba (0, 0, 255, 1)", "dash": "solid", "width": 0.8}, 
    "marker": {"color": "#0000FF", "size": 6.0, "symbol": "diamond"}, "mode": "lines+markers"
    }]

app = dash.Dash()

layout_a = go.Layout(autosize=False, width=700, height=220,
    margin=go.Margin(l=50, r=50, b=40, t=20, pad=4),
    yaxis=dict(range=[-35, 35]), xaxis=dict(title='t',range=[0, 25])
)
layout_b = go.Layout(autosize=False, width=700, height=300,
    margin=go.Margin(l=50, r=50, b=40, t=20, pad=4),
    yaxis=dict(range=[-0.5, 0.5]), xaxis=dict(title='t',range=[0, 6.6])
)
layout_d_x = go.Layout(autosize=False, width=700, height=200,
    margin=go.Margin(l=50, r=50, b=40, t=20, pad=4),
    yaxis=dict(range=[-90000, 90000]), xaxis=dict(title='t',range=[0, 4.6])
)
layout_d_y = go.Layout(autosize=False, width=700, height=200,
    margin=go.Margin(l=50, r=50, b=40, t=20, pad=4),
    yaxis=dict(range=[-3.0, 2.0]), xaxis=dict(title='t',range=[0, 4.6])
)

def compute_fig_x_a(h_0, h_1): # arg: new_slider_value
    h_a = [h_0,h_1] # diffrent sampling periods for graphs
    x_a = []
    for h in h_a:  # diffrent sampling periods
        p = 1/h * p_tr
        x_a += [ p * f_1111 * p ]
    traces_a = []
    for n, h in enumerate(h_a):  # diffrent sampling periods
        traces_a += [go.Scatter( y=list(x_a[n]), x0=0, dx=h, name='h='+str(h), **style[n] )]
    new_figure_a={'data': go.Data(traces_a), 'layout': layout_a}
    return new_figure_a

T_0 = 0.04
    
def compute_fig_x_b(h_0, h_1): # arg: new_slider_value
    h_b = [h_0,h_1] # diffrent sampling periods for graphs
    x_b = []
    for h in h_b:
        p = 1/h * p_tr
        x_b += [ p * f_1111 * 1 / (p**2 + p + 4) * ( -(-T_0) * ( (p**2 +1).sqrt() ) ).exp() ]
    traces_b = []
    for n, h in enumerate(h_b):  # diffrent sampling periods
        traces_b += [go.Scatter( y=list(x_b[n]), x0=0, dx=h, name='h='+str(h), **style[n] )]
    new_figure_b={'data': go.Data(traces_b), 'layout': layout_b}
    return new_figure_b
    
def compute_fig_x_b0(h_0, h_1): # arg: new_slider_value
    h_b0 = [h_0,h_1] # diffrent sampling periods for graphs
    x_b0 = []
    for h in h_b0:
        p = 1/h * p_tr
        x_b0 += [ p * f_1111 * 1 / (p**2 + p + 4) * ( -(-T_0) * ( (p**2 +1).sqrt() ) ).exp() * (-T_0*p).exp() ]
    traces_b0 = []
    for n, h in enumerate(h_b0):  # diffrent sampling periods
        traces_b0 += [go.Scatter( y=list(x_b0[n]), x0=0, dx=h, name='h='+str(h), **style[n] )]
    new_figure_b0={'data': go.Data(traces_b0), 'layout': layout_b}
    return new_figure_b0
    
def compute_fig_xy_d(a, h, xy='x'): # arg: new_slider_value
    p = 1/h * p_tr
    blackBox1 = 1 / (p**2 + p + 4)
    x_ =  f_1111 * p**(a+1)
    if xy == 'x':
        layout_d = layout_d_x
        traces_d = [ go.Scatter( y=list(x_), x0=0, dx=h, name='x_d(t), a='+str(a)+', h='+str(h), **style[0] ) ]
    else:
        y_ = x_ * blackBox1
        layout_d = layout_d_y
        traces_d = [ go.Scatter( y=list(y_), x0=0, dx=h, name='y_d(t), a='+str(a)+', h='+str(h), **style[1] ) ]
    new_figure_d={'data': go.Data(traces_d), 'layout': layout_d}
    return new_figure_d

app.layout = html.Div([
    dcc.Markdown(children=r'''
# Discrete representations of generalized time domain functions

## Laplace transform

The functions of continuous time defined for *t* ≥ 0, can be expressed in **Mikusinski's operational calculus** in form of functions of **Heaviside's operator** *p* = 1 / ∫  
where *X(p)* denote **Laplace transform** formulas: 

{ *x(t)* } = *X(p)* · *p* · {1}

{1} denotes function, with value 1 for all *t* ≥ 0 .

For example { 200 sin(t) } = ( 200 · 2 / (p² + 4) ) · *p* · {1} .

##  Z-transform

Z-transform corresponds to  { *x(t)* } is determined by series of samples in discrete time *t*_k = *k* *h* , where *k* = 0, 1,... and *h* is the sampling period:

*x* = (~ x₀~, x₁~ x₂~ ... ~) = (x₀  z⁰ + x₁  z⁻¹ + x₂  z⁻² + ...), where z = (~ 1 ~ 0 ~)

Replacing continuous time function {1} by sequence of samples (~ 0.5~, 1~ 1~1~ ...~)..
and replacing Heaviside operator *p* utilizing algorithm of numerical integration


*p* = ( 2 / h ) (1 - z⁻¹) / (1 + z⁻¹) , where z = (~ 1 ~ 0 ~)  
= ( 2 / h ) (~ 1 ~ , -1 ~) / (~ 1 ~ , 1 ~)  
= ( 1 / h ) (~ 2~, -4~ 4~ -4~ ...~) 

we obtain expression for approximate sequence of samples of function { _x(t)_ }:

*x* = *X(p)* · *p* · (~0.5~, 1~1~1~ ... ~) 

This way we get discrete samples of abstract functions, like derivative of non-smooth function, like  

{*x_a(t)*} = { d/dt *δ(t*) } = *p* · {1} · *p*

where Laplace transform  *X(p)* = *p*

or function containing negative delay, like  

{*x_b(t)*} = *p* · {1} · (1 / (*p*² + *p* + 4) exp( -(-0.1)√(*p*² +1) )

(see
[Mikusinski's remarks about negative delay operator](http://www.pei.prz.edu.pl/~kubaszek/smacd06/JM_OperCalc.html)).

### Digital samples of derivative of the step function:

{*x_a(t)*} = { d/dt *δ(t*) } = *p* · {1} · *p*

```python
# Z-transform (live example):
f_1111 = 0.5 * PolyNum('const:(~1~,2~2~2~2~...~)')
p_tr = PolyNum('const:(~2~,-4~4~-4~4~...~)') # 2*(~1~-1~)/(~1~1~)

h_a = [0.4,0.8] # diffrent sampling periods for graphs
x_a = []
for h in h_a:  # diffrent sampling periods
    p = 1/h * p_tr
    x_a += [ p * f_1111 * p ]
```
'''
    ),
    html.Div([
        html.Label('Change values of sampling step h: o ------------------ o'),
        dcc.RangeSlider(
            id='sli_h_a', value=[0.4, 0.8], min=0.3, max=0.9, step=0.01, 
            updatemode='drag', className='sli_h')
        ],
        style={'width':600, 'padding':10}
    ),
    dcc.Graph(
        id='grf2_44_44',
        figure=compute_fig_x_a(0.5, 0.7)
    ),
    dcc.Markdown(children=r'''
---
### Digital samples of signal containing negative delay operator:

{*x_b(t)*} = *p* · {1} · (1 / (*p*² + *p* + 4) exp( -(-T₀)√(*p*² +1) )

T₀ = 0.04

```python
h_b = [0.15,0.2] # diffrent sampling periods for graphs
x_b = []
T_0 = 0.04
for h in h_b:
    p = 1/h * p_tr
    x_b += [ p * f_1111 * 1 / (p² + p + 4) * ( -(-T_0) * ( (p² +1).sqrt() ) ).exp() ]
```
'''
    ),
    html.Div([
        html.Label('Change values of sampling step h: o ------------------ o'),
        dcc.RangeSlider(
            id='sli_h_b', value=[0.15, 0.2], min=0.1, max=0.3, step=0.01, updatemode='drag',
            className='sli_h')
        ],
        style={'width':600, 'padding':10}
    ),
    dcc.Graph(
        id='grf_exp1',
        figure={
            'data': compute_fig_x_b(0.1, 0.2),
            'layout': layout_b
        }
    ),
    dcc.Markdown(children=r'''
---
Neutralizing negative delay operator we get regular function for $t ≥ 0$
 (see the last part of [Mikusinski's remarks about negative delay operator](http://www.pei.prz.edu.pl/~kubaszek/smacd06/JM_OperCalc.html)):

{*x_b(t)*} = *p* · {1} · (1 / (*p*² + *p* + 4) exp( -(-T₀)√(*p*² +1) ) · exp(-T₀  p)

T₀ = 0.04

```python
x_b0 = []
for h in h_b:
    p = 1/h * p_tr
    x_b0 += [ p * f_1111 * 1 / (p² + p + 4) * ( -(-T_0) * ( (p**2 +1).sqrt() ) ).exp() * (-T_0*p).exp() ]
```
'''
    ),
    html.Div([
        html.Label('Change values of sampling step h: o ------------------ o'),
        dcc.RangeSlider(
            id='sli_h_b0', value=[0.15, 0.2], min=0.1, max=0.3, step=0.01, 
            updatemode='drag', className='sli_h')
        ],
        style={'width':600, 'padding':10}
    ),
    dcc.Graph(
        id='grf_exp1zero',
        figure={
            'data': compute_fig_x_b0(0.1, 0.2),
            'layout': layout_b
        }
    ),
    dcc.Markdown(children=r'''
---    
# Black box parameters
---    

## Derivative of the step function on input of black box  

{*x_d(t)*} = { (d/dt)^*a* *δ(t*) } = *p* · {1} · *p*^*a*

Sequences of the samples, which correspond to this abstract functions - a-th derivative of Dirac's delta function can be used to filter characteristic of DSP algorithm closed in black box.

    
''' ),
    html.Div([
        html.Label('Change derivative level _a_:'),
        dcc.Slider(
            id='sli_a', value=2.0, min=-1.0, max=2.6, step=0.1, 
            updatemode='drag', className='sli_h'),
        html.Label('Change sampling step _h_:'),
        dcc.Slider(
            id='sli_h_d', value=0.15, min=0.05, max=0.2, step=0.01, 
            updatemode='drag', className='sli_h')
        ],
        style={'width':600, 'padding':10}
    ),
    dcc.Graph(
        id='grf_d_x',
        figure={
            'data': compute_fig_xy_d(2.0, 0.15, 'x'),
            'layout': layout_d_x
        }
    ),
    dcc.Graph(
        id='grf_d_y',
        figure={
            'data': compute_fig_xy_d(2.0, 0.15, 'y'),
            'layout': layout_d_y
        }
    )

], 
className="container"
)

@app.callback(Output('grf2_44_44', 'figure'),
             [Input('sli_h_a', 'value')])
def data_analysis_x_a(new_slider_values):
    new_figure = compute_fig_x_a(*new_slider_values)
    return new_figure

@app.callback(Output('grf_exp1', 'figure'),
             [Input('sli_h_b', 'value')])
def data_analysis_x_b(new_slider_values):
    new_figure = compute_fig_x_b(*new_slider_values)
    return new_figure

@app.callback(Output('grf_exp1zero', 'figure'),
             [Input('sli_h_b0', 'value')])
def data_analysis_x_b0(new_slider_values):
    new_figure = compute_fig_x_b0(*new_slider_values)
    return new_figure

@app.callback(Output('grf_d_x', 'figure'),
             [Input('sli_a', 'value'), Input('sli_h_d', 'value')])
def data_analysis_xy_d(a, h, xy='x'):
    new_figure = compute_fig_xy_d(a, h, xy='x')
    return new_figure

@app.callback(Output('grf_d_y', 'figure'),
             [Input('sli_a', 'value'), Input('sli_h_d', 'value')])
def data_analysis_xy_d(a, h, xy='y'):
    new_figure = compute_fig_xy_d(a, h, xy='y')
    return new_figure

    
if __name__ == '__main__':
    app.run_server()
#√·∫≠≤≥ ⁰¹²³⁴⁵⁶⁸⁹⁺⁻ⁱⁿ⁽⁾ ₀₁₂₃₄₆₇₈₉₊₋₌₎ₐₑₒ ¼½ δ
