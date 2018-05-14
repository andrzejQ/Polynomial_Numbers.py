import dash
import dash_core_components as dcc
import dash_html_components as html

from PNlib import PolyNumConf
PolyNumConf.max_N=32 # PN significant digits number (restart jupyter kernel on change)
from PNlib.PolyNum import PolyNum

# Z-transform (live example):
f_1111 = 0.5 * PolyNum('const:(~1~,2~2~2~2~...~)')
p_tr = PolyNum('const:(~2~,-4~4~-4~4~...~)') # 2*(~1~-1~)/(~1~1~)

h_a = [0.4,0.8] # diffrent sampling periods for graphs
x_a = []
for h in h_a:  # diffrent sampling periods
    p = 1/h * p_tr
    x_a += [ p * f_1111 * p ]
    
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
    
traces_a = []
for n, h in enumerate(h_a):  # diffrent sampling periods
    traces_a += [go.Scatter( y=list(x_a[n]), x0=0, dx=h, name='h='+str(h), **style[n] )]
layout_a = go.Layout(autosize=False, width=800, height=220,
    margin=go.Margin(l=50, r=50, b=20, t=0, pad=4),
    yaxis=dict(range=[-35, 35]), xaxis=dict(title='t')
)

traces_b = []
for n, h in enumerate(h_b):  # diffrent sampling periods
    traces_b += [go.Scatter( y=list(x_b[n]), x0=0, dx=h, name='h='+str(h), **style[n] )]
layout_b = go.Layout(autosize=False, width=800, height=300,
    margin=go.Margin(l=50, r=50, b=30, t=0, pad=4),
    yaxis=dict(range=[-0.5, 0.5]), xaxis=dict(title='t')
)

traces_b0 = []
for n, h in enumerate(h_b):  # diffrent sampling periods
    traces_b0 += [go.Scatter( y=list(x_b0[n]), x0=0, dx=h, name='h='+str(h), **style[n] )]
    
app = dash.Dash()

app.layout = html.Div([
    dcc.Graph(
        id='2_44_44',
        figure={
            'data': go.Data(traces_a),
            'layout': layout_a
        }
    ),
    dcc.Markdown(children='''\
---
xxyyzz'''
    ),
    dcc.Graph(
        id='exp1',
        figure={
            'data': go.Data(traces_b),
            'layout': layout_b
        }
    ),
    dcc.Markdown(children='''\
---
000 000'''
    ),
    dcc.Graph(
        id='exp1zero',
        figure={
            'data': go.Data(traces_b0),
            'layout': layout_b
        }
    )
])


if __name__ == '__main__':
    app.run_server()
