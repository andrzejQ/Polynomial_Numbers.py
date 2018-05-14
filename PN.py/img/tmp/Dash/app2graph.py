import dash
import dash_core_components as dcc
import dash_html_components as html

import plotly.plotly as py
import plotly.graph_objs as go
style = [{"line": {"color": "rgba (255, 0, 0, 1)", "dash": "6px,3px", "width": 0.8}, 
    "marker": {"color": "#FF0000", "size": 6.0, "symbol": "dot"}, "mode": "lines+markers"
    },
    {"line": {"color": "rgba (0, 0, 255, 1)", "dash": "solid", "width": 0.8}, 
    "marker": {"color": "#0000FF", "size": 6.0, "symbol": "diamond"}, "mode": "lines+markers"
    }]

h_a = [0.4,0.8] # diffrent sampling periods for graphs
x_a = [[2/h_a[0]**2],[2/h_a[1]**2]]
s = 1
for i in range(31):
    s = -s
    x_a[0].append(s*4/h_a[0]**2)
    x_a[1].append(s*4/h_a[1]**2)
    
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
