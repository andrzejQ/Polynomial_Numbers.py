import plotly.plotly as py
from plotly.graph_objs import *

trace0 = Scatter(
    x=[1, 2, 3, 4],
    y=[10, 15, 13, 17]
)
trace1 = Scatter(
    x=[1, 2, 3, 4],
    y=[16, 5, 11, 9]
)
data = Data([trace0, trace1])

py.plot(data, filename = 'basic-line')

# (base) ...PN.py\PN.py\img\tmp\Plotly>python py.plt.Zero.py
# High five! You successfully sent some data to your account on plotly. View your plot in your browser at https://plot.ly/~andrzejQ/0 or inside your plot.ly account where it is named 'basic-line'
