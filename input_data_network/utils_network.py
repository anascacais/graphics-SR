# built-in
import ast

# third party
from matplotlib.colors import LinearSegmentedColormap
import pandas as pd
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

# local
from utils_authors_affil import get_bigrams


LinearSegmentedColormap.from_list(name='saraiva2022', colors=[
                                  '#4179A0', '#A0415D', '#44546A', '#44AA97', '#FFC000', '#0F3970', '#873C26'])


def get_network_body(filepath, remove_single):

    try:
        bigrams = pd.read_csv('aux_files/bigrams.csv', index_col=0)
    except:
        bigrams = get_bigrams(filepath)

    # Create dictionary of edges and their weights
    d = bigrams.set_index('bigrams').T.to_dict('records')[0]

    print('\nNumber of papers shared by pairs of authors and respective counts:')
    print(f'    {np.unique(list(d.values()), return_counts=True)}')

    # Remove pairs of authors with a single connection
    if remove_single:
        del_list = []

        for key in d.keys():
            if d[key] == 1:
                del_list += [key]
        for key in del_list:
            del d[key]

    # Create network
    G = nx.Graph()

    # Create connections between nodes
    for k, v in d.items():
        k = ast.literal_eval(k)
        # Change authors' names from "surname,name" to "n. surname"
        # author1 = f'{k[0].split(",")[1][0]}. {k[0].split(",")[0]}'
        # author2 = f'{k[1].split(",")[1][0]}. {k[1].split(",")[0]}'
        G.add_edge(k[0], k[1], weight=(v * 10))

    return G


def plot_network(G, node_size, node_color, legend, remove_single, colormap, title):

    if not remove_single:
        legend = None

    if node_color is None:
        node_color = '#00b4d9'

    _, ax = plt.subplots(figsize=(16, 12))
    pos = nx.spring_layout(G)

    # Plot networks
    nx.draw_networkx(G, pos,
                     font_size=10,
                     width=2,
                     edge_color='grey',
                     node_color=node_color,
                     with_labels=True,
                     ax=ax,
                     cmap=colormap,
                     node_size=[v*80 for v in node_size.values()])

    if legend is not None:
        ax.legend(handles=legend)
    plt.title(title)
    plt.show()
