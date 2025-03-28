"""
visualization.py - Displays ranked restaurants using Plotly bar chart.
"""
import plotly.graph_objects as go
import networkx as nx
import matplotlib.pyplot as plt


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


def build_top10_graph(filtered: list[dict], ranked: list[tuple[str, float]]) -> nx.Graph:
    """
    Build a NetworkX graph for the top 10 recommended restaurants.

    :param filtered: List of restaurant dictionaries (each with 'name' and 'location').
    :param ranked: Ranked list of restaurants as tuples (restaurant name, score).
    :return: A NetworkX Graph built from the top 10 restaurants.
    """
    # Get top 10 restaurant names.
    top_names = {name for name, _ in ranked[:10]}
    # Filter restaurants to only include those in the top 10.
    top_restaurants = [_unique_rest_item for _unique_rest_item in filtered if _unique_rest_item['name'] in top_names]

    graph = nx.Graph()
    for res_obj in top_restaurants:
        graph.add_node(res_obj['name'], location=res_obj['location'])

    # Add edges for restaurants that share the same location.
    loc_map = {}
    for node, node_info in graph.nodes(data=True):
        loc_value = node_info['location']
        loc_map.setdefault(loc_value, []).append(node)
    for nodes_list in loc_map.values():
        for i in range(len(nodes_list)):
            for j in range(i + 1, len(nodes_list)):
                graph.add_edge(nodes_list[i], nodes_list[j])

    return graph


def draw_graph(graph: nx.Graph) -> None:
    """
    Draw the given graph using a spring layout. Also builds a legend based on restaurant locations.

    :param graph: A NetworkX Graph with nodes that have a 'location' attribute.
    :return: None
    """
    # Map each unique location to a unique color index.
    unique_locs = sorted({node_info['location'] for _, node_info in graph.nodes(data=True)})
    loc_to_color = {loc_item: idx for idx, loc_item in enumerate(unique_locs)}
    node_colors = [loc_to_color[graph.nodes[node]['location']] for node in graph.nodes]

    pos = nx.spring_layout(graph, seed=42, k=1.5, iterations=100)

    fig, ax = plt.subplots(figsize=(12, 8))
    nx.draw_networkx_edges(graph, pos, ax=ax, alpha=0.3, width=0.5)
    nx.draw_networkx_nodes(
        graph, pos, ax=ax, node_size=100,
        node_color=node_colors, cmap=plt.get_cmap("Set3")
    )
    nx.draw_networkx_labels(graph, pos, labels={n: n for n in graph.nodes()}, font_size=9, ax=ax)
    ax.margins(x=0.2)

    # Build legend handles using empty scatter plots.
    legend_handles = []
    cmap = plt.get_cmap("Set3")
    max_color = max(loc_to_color.values()) if loc_to_color else 1
    for location_name in unique_locs:
        color_val = cmap(loc_to_color[location_name] / (max_color if max_color else 1))
        handle = ax.scatter([], [], color=color_val, label=location_name)
        legend_handles.append(handle)
    ax.legend(handles=legend_handles, title="Locations", bbox_to_anchor=(1, 1), loc="upper left")

    ax.set_title("Top 10 Restaurant Location Graph")
    ax.axis("off")
    fig.tight_layout()
    try:
        plt.show()
    except KeyboardInterrupt:
        pass


def visualize_location_graph_top10(filtered: list[dict], ranked: list[tuple[str, float]]) -> None:
    """
    Build and display a location graph for the top 10 recommended restaurants.

    :param filtered: List of restaurant dictionaries (each with 'name' and 'location').
    :param ranked: Ranked list of restaurants as tuples (restaurant name, score).
    :return: None
    """
    graph = build_top10_graph(filtered, ranked)
    draw_graph(graph)


# if __name__ == "__main__":
#     import doctest
#
#     doctest.testmod()
#
#     import python_ta
#
#     python_ta.check_all(config={
#         'extra-imports': ['plotly.graph_objects', 'matplotlib.pyplot', 'networkx'],
#         'allowed-io': [],
#         'max-line-length': 120
#     })
