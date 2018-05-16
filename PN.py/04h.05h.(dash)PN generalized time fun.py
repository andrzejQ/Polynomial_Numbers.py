# -*- coding: utf-8 -*-
#heroku: import os         
import dash  # http://localhost:8050/ #interactive graphs like 04.PN...ipynb, but without mathJax
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from PNlib import PolyNumConf
PolyNumConf.max_N=32 # PN significant digits number (restart jupyter kernel on change)
from PNlib.PolyNum import PolyNum

from plotly import tools
import plotly.plotly as py
import plotly.graph_objs as go
style = [{"line": {"color": "rgba (255, 0, 0, 1)", "dash": "6px,3px", "width": 0.8}, 
    "marker": {"color": "#FF0000", "size": 6.0, "symbol": "dot"}, "mode": "lines+markers"
    },
    {"line": {"color": "rgba (0, 0, 255, 1)", "dash": "solid", "width": 0.8}, 
    "marker": {"color": "#0000FF", "size": 6.0, "symbol": "diamond"}, "mode": "lines+markers"
    }]

app = dash.Dash()
#heroku: app = dash.Dash(__name__)
#heroku: server = app.server

layout_a = go.Layout(autosize=False, width=700, height=220,
    margin=go.Margin(l=50, r=50, b=40, t=20, pad=4),
    yaxis=dict(range=[-35, 35]), xaxis=dict(title='t',range=[0, 25])
)
layout_b = go.Layout(autosize=False, width=700, height=300,
    margin=go.Margin(l=50, r=50, b=40, t=20, pad=4),
    yaxis=dict(range=[-0.5, 0.5]), xaxis=dict(title='t',range=[0, 6.6])
)

# Z-transform (live example):
f_1111 = 0.5 * PolyNum('const:(~1~,2~2~2~2~...~)')
p_tr = PolyNum('const:(~2~,-4~4~-4~4~...~)') # 2*(~1~-1~)/(~1~1~)

def x_a_(p):
    return p * f_1111 * p
x_a_.layout_ = layout_a

T_0 = 0.04
def x_b_(p):
    return p * f_1111 * 1 / (p**2 + p + 4) * ( -(-T_0) * ( (p**2 +1).sqrt() ) ).exp()
x_b_.layout_ = layout_b

def x_b0_(p):
    return p * f_1111 * 1 / (p**2 + p + 4) * ( -(-T_0) * ( (p**2 +1).sqrt() ) ).exp() * (-T_0*p).exp()
x_b0_.layout_ = layout_b

def compute_fig_(h_0, h_1, x_p): # arg: new_slider_value, x_p = f(p)
    '''Compute x_01[ , ] only for changed h_0 or h_1'''
    figures_ = getattr(x_p, "_figures", None)
    h_01 = [ getattr(x_p, "_h0", None), getattr(x_p, "_h1", None) ]
    h_old, h_01 = h_01, [h_0,h_1] # 2 diffrent sampling periods for graphs
    x_01 = []
    for n, h in enumerate(h_01):  # diffrent sampling periods
        if h == h_old[n]:
            x_01 += [None]
        else:
            ##################################
            p = 1/h * p_tr
            x_01 += [ x_p(p) ]
            ##################################
    if figures_ is None:
        traces_01 = []
        for n, h in enumerate(h_01):  # diffrent sampling periods
            traces_01 += [go.Scatter( y=list(x_01[n]), x0=0, dx=h, name='h='+str(h), **style[n] )]
        figures_={'data': go.Data(traces_01), 'layout': getattr(x_p, "layout_", None)}
    else: #only update y,x data for changed h
        for n, x_ in enumerate(x_01):
            if x_:
                h = h_01[n]
                figures_['data'][n].update( y=list(x_), x=[k*h for k in range(len(x_))] )
    x_p._figures = figures_
    x_p._h0 = h_01[0]
    x_p._h1 = h_01[1]
    return figures_


def blackBox1(p):
    return 1 / (p**2 + p + 4)
blackBox1.yaxisRange = [-3.1, 2.1]

def x_d(a, p):
    return f_1111 * p**(a+1)
x_d.yaxisRange = [-100000, 100000]
    
def blackBox2(p_):
    return 1 / (p_**2 + p_ + 4) * ( -0.5 * ( (p_**2 +1).sqrt() ) ).exp()
blackBox2.yaxisRange = [-0.31, 0.41]

def x_e(b, p_):
    return p_ * f_1111 * (b*p_).exp()
x_e.yaxisRange = [-300e12, 200e12]
    
def compute_fig_xy_(a, h, x_p_, blackBox_): # arg: sliders values, x_p_(a, p), blackBox_(p)
    fig = getattr(x_p_, "_figures", None)
    h_old = getattr(x_p_, "_h", None)
    blackBox1 = getattr(x_p_, "blackBox_", None)

    p = 1/h * p_tr
    if (blackBox1 is None) or (h_old != h):
        blackBox1 = blackBox_(p) #else skip calc. for spead up
    x_ =  x_p_(a, p)
    trace___x = go.Scatter( y=list(x_), x0=0, dx=h, name='inp.', **style[0])
    y_ = x_ * blackBox1
    trace___y = go.Scatter( y=list(y_), x0=0, dx=h, name='out.', **style[1])
    
    fig = tools.make_subplots(rows=2, cols=1, shared_xaxes=True)
    fig.append_trace(trace___x, 1, 1)
    fig.append_trace(trace___y, 2, 1)
    fig['layout'].update(height=500, width=700)
    fig['layout']['xaxis1'].update(range=[0, 4.3], title='t')
    #fig['layout']['xaxis2'].update(range=[0, 4.3], title='t')
    fig['layout']['yaxis1'].update(range=x_p_.yaxisRange, title='x(t)')
    fig['layout']['yaxis2'].update(range=blackBox_.yaxisRange, title='y(t)')
    x_p_._figures = fig
    x_p_._h = h
    return fig

######################################################

app.layout = html.Div([
    dcc.Markdown(children=r'''
    
[ Andrzej Kubaszek, Rzeszow University of Technology, 2018](http://www.pei.prz.edu.pl/%7Ekubaszek/index_en.html)

Floating point arithmetic for 'numbers' with digits such as real numbers, can be used to solve differential or difference equations using Mikusinski's or Bellert's operational calculus theory.

*( This page was build with [plot.ly dash](https://plot.ly/products/dash/) )*

# Discrete representations of generalized time domain functions

## Laplace transform

The functions of continuous time defined for *t* ≥ 0, can be expressed in **Mikusinski's operational calculus** in form of functions of **Heaviside's operator** *p* = 1 / ∫  
where *X(p)* denote **Laplace transform** formulas: 
'''
    ),
    html.Img(src="https://pei.prz.edu.pl/~kubaszek/smacd06/LaplZPNbig.png", alt="LaplZ_PN_", style={'float':"right", 'width':"30em"} ),
    dcc.Markdown(children=r'''
{ *x(t)* } = *X(p)* · *p* · {1}

{1} denotes function, with value 1 for all *t* ≥ 0 .

For example { 200 sin(2t) } = ( 200 · 2 / (p² + 4) ) · *p* · {1} .

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

# h - sampling period from slider
p = 1/h * p_tr
x_a = p * f_1111 * p
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
        figure={
            'data': compute_fig_(0.5, 0.7, x_a_),
            'layout': getattr(x_a_, "layout_", None)
        }
    ),
    dcc.Markdown(children=r'''
---
### Digital samples of signal containing negative delay operator:

{*x_b(t)*} = *p* · {1} · (1 / (*p*² + *p* + 4) exp( -(-T₀)√(*p*² +1) )

T₀ = 0.04

```python
T_0 = 0.04
p = 1/h * p_tr
x_b = p * f_1111 * 1 / (p**2 + p + 4) * ( -(-T_0) * ( (p**2 +1).sqrt() ) ).exp()
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
            'data': compute_fig_(0.1, 0.2, x_b_),
            'layout': getattr(x_b_, "layout_", None)
        }
    ),
    dcc.Markdown(children=r'''
---
Neutralizing negative delay operator we get regular function for $t ≥ 0$
 (see the last part of [Mikusinski's remarks about negative delay operator](http://www.pei.prz.edu.pl/~kubaszek/smacd06/JM_OperCalc.html)):

{*x_b(t)*} = *p* · {1} · (1 / (*p*² + *p* + 4) exp( -(-T₀)√(*p*² +1) ) · exp(-T₀  p)

T₀ = 0.04

```python
p = 1/h * p_tr
x_b0 = p * f_1111 * 1 / (p**2 + p + 4) * ( -(-T_0) * ( (p**2 +1).sqrt() ) ).exp() * (-T_0*p).exp()
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
            'data': compute_fig_(0.1, 0.2, x_b0_),
            'layout': getattr(x_b0_, "layout_", None)
        }
    ),
    dcc.Markdown(children=r'''
---    
# Black box parameters
---    

## Derivative of the step function on input of black box  

{*x(t)*} = { dᵃ/dtᵃ *δ(t)* } = *p* · {1} · *p* ᵃ 

Sequences of the samples, which correspond to this abstract functions - a-th derivative of Dirac's delta function can be used to filter characteristic of DSP algorithm closed in black box.

```python
# a, h - from sliders
p = 1/h * p_tr
blackBox1 = 1 / (p**2 + p + 4)
x_ =  f_1111 * p**(a+1)
y_ = x_ * blackBox1
```
    
''' ),
    html.Div([
    
        html.Div([
            html.Label('Derivative level:'),
            dcc.Slider(
                id='sli_aa', value=2.0, min=-1.0, max=2.6, step=0.1
                , updatemode='drag', className='sli_h'
                , marks={0:'0',1:'1',2:{'label':'2', 'style':{'color':'red'}}} ),
            html.Div('a=',id='slider-output-aa'),
        ], style={'padding':'0 10px', 'width': '44%', 'display': 'inline-block'}),
        html.Div([
            html.Label('Sampling step:'),
            dcc.Slider(
                id='sli_h_d', value=0.15, min=0.05, max=0.2, step=0.01, 
                updatemode='drag', className='sli_h'),
            html.Div('h=',id='slider-output-h_d')
        ], style={'padding':'0 10px', 'width': '44%', 'display': 'inline-block'}),
    ], style={'width':600, 'paddingLeft':10}),
    dcc.Graph(
        id='grf_d',
        figure=compute_fig_xy_(2.0, 0.15, x_d, blackBox1)
    ),
    dcc.Markdown(children=r'''
Although *x(t)* is "unrealistic function" ( (a+1)  - derivative of the step function), it samples can be generated and applied into input of black box. For *a* ≤ 2.0 output of black box gives samples of "realistic function" *y(t)*, that means - smaller *h* leads to  more accurate *y(t)*. For *a* > 2.0 output is not convergent with decreasing *h*.
''' ),

    dcc.Markdown(children=r'''
---

## Delay operator with negative delay on input of black box

{*x(t)*} = *p* · {1} · exp(-(-*b*) *p*) } 

Sequences of the samples, which correspond to this abstract functions - function with negative delay operator - can be used to filter delay operator of DSP algorithm closed in black box.

```python
# b, h - from sliders
p_ = 1/h * p_tr
blackBox2 =  1 / (p_**2 + p_ + 4) * ( -0.5 * ( (p_**2 +1).sqrt() ) ).exp()
x_ =  p_ * f_1111 * (b*p_).exp()
y_ = x_ * blackBox2
```
''' ),
    html.Div([
    
        html.Div([
            html.Label('Negative delay:'),
            dcc.Slider(
                id='sli_bb', value=0.5, min=-1.0, max=0.6, step=0.02
                , updatemode='drag', className='sli_h'
                , marks={0:'0', 0.6:'0.6',0.5:{'label':'0.5', 'style':{'color':'red'}}} ),
            html.Div('b=',id='slider-output-bb'),
        ], style={'padding':'0 10px', 'width': '44%', 'display': 'inline-block'}),
        html.Div([
            html.Label('Sampling step:'),
            dcc.Slider(
                id='sli_h_e', value=0.15, min=0.05, max=0.2, step=0.01, 
                updatemode='drag', className='sli_h'),
            html.Div('h=',id='slider-output-h_e')
        ], style={'padding':'0 10px', 'width': '44%', 'display': 'inline-block'}),
    ], style={'width':600, 'paddingLeft':10}),
    dcc.Graph(
        id='grf_e',
        figure=compute_fig_xy_(0.5, 0.15, x_e, blackBox2)
    ),
    dcc.Markdown(children=r'''
Although *x(t)* is "unrealistic function" (pure delay operator with negative delay), it samples can be generated and applied into input of black box. For *b* ≤ 0.5 output of black box gives samples of "realistic function" *y(t)*, that means - smaller *h* leads to  more accurate *y(t)*. For *b* > 0.5 output is not convergent with decreasing *h*.

* [PNlib on GitHub (Python library)](https://github.com/andrzejQ/Polynomial_Numbers.py)
* [jupyter notebooks index (nbviewer, GitHub)](index.ipynb)
* [mybinder - jupyter notebooks index (live)](https://mybinder.org/v2/gh/andrzejQ/Polynomial_Numbers.py.git/master?filepath=index.ipynb)
* [html - www.pei.prz.edu.pl/~kubaszek](http://www.pei.prz.edu.pl/%7Ekubaszek/index_en.html)

''' )
], style={'padding':30}, className="container"
)

#############

@app.callback(Output('grf2_44_44', 'figure'),
             [Input('sli_h_a', 'value')])
def data_analysis_x_a(new_slider_values):
    new_figure = compute_fig_(*new_slider_values, x_a_)
    return new_figure

@app.callback(Output('grf_exp1', 'figure'),
             [Input('sli_h_b', 'value')])
def data_analysis_x_b(new_slider_values):
    new_figure = compute_fig_(*new_slider_values, x_b_)
    return new_figure

@app.callback(Output('grf_exp1zero', 'figure'),
             [Input('sli_h_b0', 'value')])
def data_analysis_x_b0(new_slider_values):
    new_figure = compute_fig_(*new_slider_values, x_b0_)
    return new_figure

@app.callback(Output('slider-output-aa', 'children'),
             [Input('sli_aa', 'value')])
def update_output_sli_a(a):
    return 'a = {}'.format(a)
    
@app.callback(Output('slider-output-h_d', 'children'),
             [Input('sli_h_d', 'value')])
def update_output_sli_a(h):
    return 'h = {}'.format(h)
    
@app.callback(Output('grf_d', 'figure'),
             [Input('sli_aa', 'value'), Input('sli_h_d', 'value')])
def data_analysis_xy_d(a, h):
    new_figure = compute_fig_xy_(a, h, x_d, blackBox1)
    return new_figure


@app.callback(Output('slider-output-bb', 'children'),
             [Input('sli_bb', 'value')])
def update_output_sli_a(a):
    return 'b = {}'.format(a)
    
@app.callback(Output('slider-output-h_e', 'children'),
             [Input('sli_h_e', 'value')])
def update_output_sli_a(h):
    return 'h = {}'.format(h)
    
@app.callback(Output('grf_e', 'figure'),
             [Input('sli_bb', 'value'), Input('sli_h_e', 'value')])
def data_analysis_xy_e(b, h):
    new_figure = compute_fig_xy_(b, h, x_e, blackBox2)
    return new_figure


if __name__ == '__main__':
    app.run_server(debug=True)
# »« √· ⅟  ∫ᵗ≠≤≥ ⁰¹²³⁴⁵⁶⁸⁹⁺⁻ᵃ°ⁱⁿªº⁽⁾ ₀₁₂₃₄₆₇₈₉₊₋₌₎ₐₑₒ ¼½ δ ∞
