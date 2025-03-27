"""
restaurant_graph.py - Builds similarity graph and ranks using PageRank.
"""
import networkx as nx


def build_restaurant_graph(data):
    """
        Construct a similarity graph from restaurant data.

        Nodes represent restaurants, edges represent similarity between restaurants.
        Similarity is computed using cuisine, rating, and price.

        :param data: List of restaurant dictionaries.
        :return: NetworkX Graph with similarity-weighted edges.
        """
    g = nx.Graph()
    for r in data:
        g.add_node(r['Restaurant Name'], rating=r['Aggregate rating'],
                   cost=r['Average Cost for two'], cuisine=r['Cuisines'])
    names = list(g.nodes())
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            r1 = g.nodes[names[i]]
            r2 = g.nodes[names[j]]
            sim = compute_similarity(r1, r2)
            if sim > 0:
                g.add_edge(names[i], names[j], weight=sim)
    return g


def compute_similarity(r1, r2):
    """
        Compute similarity score between two restaurants.

        Combines:
        - cuisine match (binary)
        - rating closeness (normalized difference)
        - cost closeness (normalized difference)

        :param r1: Node attribute dict
        :param r2: Node attribute dict
        :return: Weighted similarity score [0, 1]
        """
    cuisine_score = 1 if r1['cuisine'] == r2['cuisine'] else 0
    rating_score = 1 - abs(float(r1['rating']) - float(r2['rating'])) / 5

    cost1 = float(r1['cost'])
    cost2 = float(r2['cost'])
    if max(cost1, cost2) == 0:
        cost_score = 0  # 避免除以0
    else:
        cost_score = 1 - abs(cost1 - cost2) / max(cost1, cost2)

    return 0.5 * cuisine_score + 0.3 * rating_score + 0.2 * cost_score


def rank_restaurants(g):
    """
        Rank restaurants using the PageRank algorithm.

        :param g: NetworkX graph of restaurant nodes
        :return: List of (restaurant name, PageRank score), sorted descending
        """
    pr = nx.pagerank(g, weight='weight')
    print("=== PageRank Results ===")
    for k, v in pr.items():
        print(k, "→", round(v, 4))
    return sorted(pr.items(), key=lambda x: x[1], reverse=True)
