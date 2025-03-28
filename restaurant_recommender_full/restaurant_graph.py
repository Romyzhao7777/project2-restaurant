"""
restaurant_graph.py - Builds similarity graph and ranks using PageRank.
"""

from typing import Any, Dict, List, Tuple
import networkx as nx


def build_restaurant_graph(data: List[Dict[str, Any]]) -> nx.Graph:
    """
    Construct a similarity graph from restaurant data.

    Nodes represent restaurants, and edges represent similarity between restaurants.
    Similarity is computed using cuisine, rating, and price.

    :param data: List of restaurant dictionaries.
    :return: A NetworkX Graph with similarity-weighted edges.
    """
    g = nx.Graph()
    for r in data:
        g.add_node(
            r['name'],
            rating=r['rate'],
            cost=r['approx_cost(for two people)'],
            cuisine=r['cuisines']
        )
    names = list(g.nodes())
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            r1 = g.nodes[names[i]]
            r2 = g.nodes[names[j]]
            sim = compute_similarity(r1, r2)
            if sim > 0:
                g.add_edge(names[i], names[j], weight=sim)
    return g


def compute_similarity(r1: Dict[str, Any], r2: Dict[str, Any]) -> float:
    """
    Compute similarity score between two restaurants.

    Combines:
    - Cuisine match (binary)
    - Rating closeness (normalized difference)
    - Cost closeness (normalized difference)

    :param r1: Node attribute dictionary.
    :param r2: Node attribute dictionary.
    :return: A weighted similarity score in [0, 1].
    """
    set1 = set(map(str.strip, r1['cuisine'].split(',')))
    set2 = set(map(str.strip, r2['cuisine'].split(',')))
    cuisine_score = 1 if set1 & set2 else 0
    rating_score = 1 - abs(float(r1['rating']) - float(r2['rating'])) / 5

    cost1 = float(r1['cost'])
    cost2 = float(r2['cost'])
    if max(cost1, cost2) == 0:
        cost_score = 0.0  # Avoid division by zero.
    else:
        cost_score = 1 - abs(cost1 - cost2) / max(cost1, cost2)

    return 0.5 * cuisine_score + 0.3 * rating_score + 0.2 * cost_score


def rank_restaurants(g: nx.Graph) -> List[Tuple[str, float]]:
    """
    Rank restaurants using the PageRank algorithm.

    :param g: A NetworkX graph of restaurant nodes.
    :return: A list of (restaurant name, PageRank score) tuples, sorted in descending order.
    """
    pr = nx.pagerank(g, weight='weight')
    # Removed print statements to comply with the forbidden I/O function rule.
    return sorted(pr.items(), key=lambda x: x[1], reverse=True)


# if __name__ == "__main__":
#     import doctest
#
#     doctest.testmod()
#
#     import python_ta
#
#     python_ta.check_all(config={
#         'extra-imports': ['networkx'],
#         'allowed-io': [],
#         'max-line-length': 120
#     })
