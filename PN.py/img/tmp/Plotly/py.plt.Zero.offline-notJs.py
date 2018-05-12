import plotly
from plotly.graph_objs import Scatter, Layout

plotly.offline.plot({
    "data": [Scatter(x=[1, 2, 3, 4], y=[4, 3, 2, 1])],
    "layout": Layout(title="hello world")
    },
    include_plotlyjs=False,
    filename='temp-plot-noJS.html'
)
#>>> temp-plot.html - 2.6MB (plotly.js - 2.6MB inside)
#>>> temp-plot-niJS.html - 0.6kB

#<head>
#    <script src="plotly-latest.min.js"></script>
#</head>
#<head>
#    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
#</head>