"""
main.py - Full-featured Restaurant Recommender.

Uses decision tree, graph, PageRank, and visualization.
"""

from typing import Any, Dict, List
import data_loader
import decision_tree
import restaurant_graph
import visualization


def get_popular_cuisines(restaurants: List[Dict[str, Any]], top_n: int = 10) -> List[str]:
    """
    Compute the most popular cuisines from the dataset without using Counter.
    Assumes the 'Cuisines' field may contain comma-separated values.

    :param restaurants: List of restaurant data dictionaries.
    :param top_n: Number of top cuisines to return.
    :return: List of popular cuisines.
    """
    cuisine_counts: Dict[str, int] = {}
    for entry in restaurants:
        cuisines_str = str(entry["Cuisines"])  # Cast to str to safely call split()
        for single_cuisine in cuisines_str.split(","):
            single_cuisine = single_cuisine.strip()
            if single_cuisine:
                cuisine_counts[single_cuisine] = cuisine_counts.get(single_cuisine, 0) + 1
    sorted_cuisines = sorted(cuisine_counts.items(), key=lambda x: x[1], reverse=True)
    return [item[0] for item in sorted_cuisines[:top_n]]


def compute_recommendations(
    restaurants: List[Dict[str, Any]], preferences: Dict[str, Any]
) -> (List[Dict[str, Any]], List[Any]):
    """
    Compute filtered restaurants and ranked recommendations.

    :param restaurants: List of restaurant data dictionaries.
    :param preferences: User preferences.
    :return: Tuple of (filtered restaurants, ranked recommendations).
    """
    filtered = decision_tree.filter_restaurants(restaurants, preferences)
    if not filtered:
        return filtered, []
    graph = restaurant_graph.build_restaurant_graph(filtered)
    ranked = restaurant_graph.rank_restaurants(graph)
    return filtered, ranked


if __name__ == "__main__":  # noqa: E9998
    # All I/O is performed only in the main entry point.
    all_data = data_loader.load_and_preprocess_data("zomato_cleaned (1).csv")
    popular_cuisines = get_popular_cuisines(all_data, top_n=10)

    print("Popular cuisines: ")
    for cuisine in popular_cuisines:
        print(f" - {cuisine}")

    user_cuisine = input("Enter desired cuisine: ").strip()
    if not user_cuisine:
        user_cuisine = ""
    try:
        user_min_rating = float(input("Minimum rating (0.0 - 5.0): "))
    except ValueError:
        user_min_rating = 0.0
    try:
        user_max_cost = float(input("Maximum cost for two (e.g., 1000): "))
    except ValueError:
        user_max_cost = 999999.0

    # Pass the user's selections to get_user_preferences.
    user_preferences = decision_tree.get_user_preferences(
        cuisine_input=user_cuisine,
        min_rating_input=user_min_rating,
        max_cost_input=user_max_cost
    )

    filtered_restaurants, ranked_restaurants = compute_recommendations(all_data, user_preferences)
    print(f"Restaurants after filtering: {len(filtered_restaurants)}")
    if not filtered_restaurants:
        print("❌ No restaurants matched your preferences. Try relaxing your filters.")
    else:
        visualization.visualize_rankings(ranked_restaurants)

    import python_ta
    python_ta.check_all(config={
        'extra-imports': [
            'data_loader',
            'decision_tree',
            'restaurant_graph',
            'visualization'
        ],
        'allowed-io': ['print', 'input'],
        'max-line-length': 100
    })
