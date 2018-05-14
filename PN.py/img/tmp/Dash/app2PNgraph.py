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

import plotly.plotly as py
import plotly.graph_objs as go
style = [{"line": {"color": "rgba (255, 0, 0, 1)", "dash": "6px,3px", "width": 0.8}, 
    "marker": {"color": "#FF0000", "size": 6.0, "symbol": "dot"}, "mode": "lines+markers"
    },
    {"line": {"color": "rgba (0, 0, 255, 1)", "dash": "solid", "width": 0.8}, 
    "marker": {"color": "#0000FF", "size": 6.0, "symbol": "diamond"}, "mode": "lines+markers"
    }]
traces = []
for n, h in enumerate(h_a):  # diffrent sampling periods
    traces += [go.Scatter( y=list(x_a[n]), x0=0, dx=h, name='h='+str(h), **style[n] )]
    
layout = go.Layout(autosize=False, width=600, height=180,
    margin=go.Margin(l=50, r=50, b=20, t=0, pad=4),
    yaxis=dict(range=[-35, 35]), xaxis=dict(title='t')
)

app = dash.Dash()

app.layout = html.Div([
    dcc.Graph(
        id='0101',
        figure={
            'data': go.Data(traces),
            'layout': layout
        }
    )
])


if __name__ == '__main__':
    app.run_server()
