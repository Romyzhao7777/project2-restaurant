"""
visualization.py - Displays ranked restaurants using Plotly bar chart.
"""
from typing import Any, Dict, List

import networkx as nx
import plotly.graph_objects as go
from matplotlib import pyplot as plt
from matplotlib import colors as mcolors
import matplotlib.patches as mpatches


def visualize_rankings(rankings: list[tuple[str, float]]) -> None:
    """
    Plot top 10 ranked restaurants using a horizontal bar chart.

    :param rankings: List of (restaurant name, PageRank score) tuples, sorted descending.
    :return: None
    """
    top = rankings[:10]
    names = [name for name, _ in top]
    scores = [score for _, score in top]

    fig = go.Figure(data=[
        go.Bar(x=scores, y=names, orientation='h', marker={'color': 'royalblue'})
    ])
    fig.update_layout(
        title='Top 10 Recommended Restaurants',
        xaxis_title='PageRank Score',
        yaxis_title='Restaurant',
        yaxis={'autorange': 'reversed'}  # top rank at top
    )
    fig.show()


def visualize_location_graph(data: list[dict[str, Any]], plt_module: Any = plt) -> None:
    """
    Visualize restaurants grouped by location with color legend.
    """
    g = nx.Graph()

    for r in data:
        name = r['name']
        location = r['location']
        g.add_node(name, location=location)

    # Add edges for same-location restaurants
    loc_map: dict[str, list[str]] = {}
    for node, attr in g.nodes(data=True):
        loc = attr['location']
        loc_map.setdefault(loc, []).append(node)

    for loc, node_list in loc_map.items():
        for i in range(len(node_list)):
            for j in range(i + 1, len(node_list)):
                g.add_edge(node_list[i], node_list[j])

    # Map locations to color indices
    locations = sorted(list(set(attr['location'] for _, attr in g.nodes(data=True))))
    location_to_color = {loc: idx for idx, loc in enumerate(locations)}
    color_indices = [location_to_color[g.nodes[n]['location']] for n in g.nodes]

    pos = nx.spring_layout(g, seed=42)
    nodes = nx.draw_networkx_nodes(
        g, pos,
        node_size=50,
        node_color=color_indices,
        cmap=plt_module.cm.Set3
    )
    nx.draw_networkx_edges(g, pos, width=0.5, alpha=0.3)

    # Add legend manually
    legend_patches = [
        mpatches.Patch(color=nodes.cmap(nodes.norm(idx)), label=loc)
        for loc, idx in location_to_color.items()
    ]
    plt_module.legend(
        handles=legend_patches,
        title="Locations",
        bbox_to_anchor=(1.05, 1),
        loc='upper left',
        borderaxespad=0.
    )

    plt_module.title("Restaurant Location Graph")
    plt_module.subplots_adjust(right=0.75)
    plt_module.show()

# if __name__ == "__main__":
#     import python_ta
#     python_ta.check_all(config={
#         'extra-imports': ['plotly.graph_objects', 'matplotlib.pyplot', 'networkx'],
#         'allowed-io': [],
#         'max-line-length': 120
#     })
