import numpy as np
import d3py
import pandas


N = 500
T = 5*np.pi
x = np.linspace(-T, T, N)
y = np.sin(x)
y0 = np.cos(x)

df = pandas.DataFrame({
    'x': x,
    'y': y,
    'y0': y0,
})

with d3py.PandasFigure(df, 'd3py_area', width=500, height=250) as fig:
    fig += d3py.geoms.Area('x', 'y', 'y0')
    fig += d3py.geoms.xAxis('x')
    fig += d3py.geoms.yAxis('y')
    fig.save_to_files()
    #fig.show()

import d3py
import networkx as nx    
G=nx.Graph()
G.add_edge(1,2)
G.add_edge(1,3)
G.add_edge(3,2)
G.add_edge(3,4)
G.add_edge(4,2)

with d3py.NetworkXFigure(G, name="graph_blog_20131130",width=500, height=500) as p:
    p += d3py.ForceLayout()
    p.css['.node'] = {'fill': 'blue', 'stroke': 'magenta'}
    p.save_to_files()
