import networkx as nx
import pandas as pd
import json
from plotly.graph_objs import Scatter, Figure, Layout

# Cargar los datos
df = pd.read_excel('data.xlsx')

# Crear el grafo
G = nx.Graph()
for _, row in df.iterrows():
    autor = row['Autor']
    titulo = row['Título']
    G.add_node(autor, label=autor)
    G.add_node(titulo, label=titulo)
    G.add_edge(autor, titulo)

# Generar posiciones de nodos
pos = nx.spring_layout(G)

# Crear trazas para nodos y aristas
edge_trace = Scatter(x=[], y=[], mode='lines', line=dict(color='black', width=0.5))
for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_trace['x'] += (x0, x1, None)
    edge_trace['y'] += (y0, y1, None)

node_trace = Scatter(
    x=[], y=[], text=[], mode='markers+text',
    marker=dict(size=10, color='skyblue'),
    textposition='top center'
)
for node in G.nodes():
    x, y = pos[node]
    node_trace['x'] += (x,)
    node_trace['y'] += (y,)
    node_trace['text'] += (node,)

# Crear la figura
fig = Figure(
    data=[edge_trace, node_trace],
    layout=Layout(
        title='Red de Autores y Títulos',
        showlegend=False,
        hovermode='closest',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    )
)

# Guardar la figura en formato JSON
fig_json = fig.to_json()
with open("static/graph.json", "w") as f:
    f.write(fig_json)
