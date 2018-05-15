# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from PNlib import PolyNumConf
PolyNumConf.max_N=32 # PN significant digits number (restart jupyter kernel on change)
from PNlib.PolyNum import PolyNum

# Z-transform (live example):
f_1111 = 0.5 * PolyNum('const:(~1~,2~2~2~2~...~)')
p_tr = PolyNum('const:(~2~,-4~4~-4~4~...~)') # 2*(~1~-1~)/(~1~1~)

    
h_b = [0.15,0.2] # diffrent sampling periods for graphs
x_b = []
T_0 = 0.04
for h in h_b:
    p = 1/h * p_tr
    x_b += [ p * f_1111 * 1 / (p**2 + p + 4) * ( -(-T_0) * ( (p**2 +1).sqrt() ) ).exp() ]

x_b0 = []
for h in h_b:
    p = 1/h * p_tr
    x_b0 += [ p * f_1111 * 1 / (p**2 + p + 4) * ( -(-T_0) * ( (p**2 +1).sqrt() ) ).exp() * (-T_0*p).exp() ]

import plotly.plotly as py
import plotly.graph_objs as go
style = [{"line": {"color": "rgba (255, 0, 0, 1)", "dash": "6px,3px", "width": 0.8}, 
    "marker": {"color": "#FF0000", "size": 6.0, "symbol": "dot"}, "mode": "lines+markers"
    },
    {"line": {"color": "rgba (0, 0, 255, 1)", "dash": "solid", "width": 0.8}, 
    "marker": {"color": "#0000FF", "size": 6.0, "symbol": "diamond"}, "mode": "lines+markers"
    }]

app = dash.Dash()

layout_a = go.Layout(autosize=False, width=800, height=220,
    margin=go.Margin(l=50, r=50, b=40, t=20, pad=4),
    yaxis=dict(range=[-35, 35]), xaxis=dict(title='t',range=[0, 25])
)

def your_compute_figure_function(h_0, h_1): # arg: new_slider_value
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

traces_b = []
for n, h in enumerate(h_b):  # diffrent sampling periods
    traces_b += [go.Scatter( y=list(x_b[n]), x0=0, dx=h, name='h='+str(h), **style[n] )]

layout_b = go.Layout(autosize=False, width=800, height=300,
    margin=go.Margin(l=50, r=50, b=40, t=20, pad=4),
    yaxis=dict(range=[-0.5, 0.5]), xaxis=dict(title='t',range=[0, 6.6])
)

traces_b0 = []
for n, h in enumerate(h_b):  # diffrent sampling periods
    traces_b0 += [go.Scatter( y=list(x_b0[n]), x0=0, dx=h, name='h='+str(h), **style[n] )]
    
app.layout = html.Div([
    dcc.Markdown(children='''\
# Discrete representations of generalized time domain functions

The functions of continuous time defined for $t \geq 0$, can be expressed in **Mikusinski's operational calculus** in form of functions of **Heaviside's operator** $ p = \cfrac{1}{\int_0^t} $ where $X(p)$ denote $\color{magenta}{\text{Laplace transform}}$ formulas...

This way we get discrete samples of abstract functions, like derivative of non-smooth function, like  
$
\{x_a(t)\} = \{ \cfrac{\mathrm{d}}{\mathrm{d}t} \delta(t) \} = \color{brown}{ p \cdot \{1\} \cdot \ } \color{magenta}{p} 
$, 
where Laplace transform  $ \color{magenta}{X(p) = p} $ or function containing negative delay, like  
$
\{x_b(t)\} = \color{brown}{ p \cdot \{1\} \cdot \ } \color{magenta}{ \cfrac{1}{p^2 + p + 4}\ \exp(-(-0.1)\sqrt{p^2 +1}) } 
$ 
(see
[Mikusinski's remarks about negative delay operator](http://www.pei.prz.edu.pl/~kubaszek/smacd06/JM_OperCalc.html)).

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
    html.Label('h_0, h_1'),
    dcc.RangeSlider(id='sli_h', value=[0.4, 0.8], min=0.3, max=0.9, step=0.05, updatemode='drag'),
    dcc.Graph(
        id='grf2_44_44',
        figure=your_compute_figure_function(0.5, 0.7)
    ),
    dcc.Markdown(children='''\
---
### Digital samples of signal containing negative delay operator:

```python
h_b = [0.15,0.2] # diffrent sampling periods for graphs
x_b = []
T_0 = 0.04
for h in h_b:
    p = 1/h * p_tr
    x_b += [ p * f_1111 * 1 / (p**2 + p + 4) * ( -(-T_0) * ( (p**2 +1).sqrt() ) ).exp() ]
```
'''
    ),
    dcc.Graph(
        id='grf_exp1',
        figure={
            'data': go.Data(traces_b),
            'layout': layout_b
        }
    ),
    dcc.Markdown(children='''\
---
Neutralizing negative delay operator

```python
x_b0 = []
for h in h_b:
    p = 1/h * p_tr
    x_b0 += [ p * f_1111 * 1 / (p**2 + p + 4) * ( -(-T_0) * ( (p**2 +1).sqrt() ) ).exp() * (-T_0*p).exp() ]
```
'''
    ),
    dcc.Graph(
        id='grf_exp1zero',
        figure={
            'data': go.Data(traces_b0),
            'layout': layout_b
        }
    )
])

@app.callback(Output('grf2_44_44', 'figure'),
             [Input('sli_h', 'value')])
def your_data_analysis_function(new_slider_values):
    new_figure = your_compute_figure_function(*new_slider_values)
    return new_figure

if __name__ == '__main__':
    app.run_server()
