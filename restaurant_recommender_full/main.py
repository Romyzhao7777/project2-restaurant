"""
main.py - Full-featured Restaurant Recommender.

Uses decision tree, graph, PageRank, and visualization.
"""

import data_loader
import decision_tree
import restaurant_graph
import visualization


def main() -> None:
    """
    The main entry point for the program.

    It runs the complete pipeline:
    1. Loads the cleaned restaurant data from zomato_cleaned (1).csv
    2. Collects user preferences for cuisine, rating, and cost
    3. Filters restaurants based on preferences
    4. Constructs a similarity graph using selected features
    5. Applies PageRank algorithm to rank restaurants
    6. Displays the top-ranked restaurants as a bar chart using Plotly
    """
    data = data_loader.load_and_preprocess_data("zomato_cleaned (1).csv")
    user_pref = decision_tree.get_user_preferences()
    filtered = decision_tree.filter_restaurants(data, user_pref)

    print(f"Restaurants after filtering: {len(filtered)}")
    if not filtered:
        print("❌ No restaurants matched your preferences. Try relaxing your filters.")
        return

    graph = restaurant_graph.build_restaurant_graph(filtered)
    ranked = restaurant_graph.rank_restaurants(graph)
    visualization.visualize_rankings(ranked)


if __name__ == "__main__":
    main()

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['data_loader', 'decision_tree', 'restaurant_graph', 'visualization',
                          'networkx', 'plotly.graph_objects'],
        'allowed-io': ['print', 'input'],
        'max-line-length': 100
    })

