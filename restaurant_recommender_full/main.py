"""
main.py - Full-featured Restaurant Recommender using decision tree, graph, PageRank, and visualization.
"""

from data_loader import load_and_preprocess_data
from decision_tree import get_user_preferences, filter_restaurants
from restaurant_graph import build_restaurant_graph, rank_restaurants
from visualization import visualize_rankings


def main() -> None:
    """
        The main entry point for the program.

        It runs the complete pipeline:
        1. Loads the cleaned restaurant data from zomato.csv
        2. Collects user preferences for cuisine, rating, and cost
        3. Filters restaurants based on preferences
        4. Constructs a similarity graph using selected features
        5. Applies PageRank algorithm to rank restaurants
        6. Displays the top-ranked restaurants as a bar chart using Plotly
        """
    data = load_and_preprocess_data("zomato_cleaned (1).csv")
    user_pref = get_user_preferences()
    filtered = filter_restaurants(data, user_pref)
    graph = build_restaurant_graph(filtered)
    ranked = rank_restaurants(graph)
    visualize_rankings(ranked)
    print(f"Restaurants after filtering: {len(filtered)}")
    if not filtered:
        print("❌ No restaurants matched your preferences. Try relaxing your filters.")
        return


if __name__ == "__main__":
    main()
