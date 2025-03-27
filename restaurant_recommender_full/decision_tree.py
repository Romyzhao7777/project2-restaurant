"""
decision_tree.py - Collects user preferences and filters restaurant dataset.

Note:
- This module does NOT print or take user input directly (to comply with style rules).
- The calling code (e.g., in main.py) is responsible for any I/O.
"""

from typing import Any, Dict, List


def get_popular_cuisines(data: List[Dict[str, Any]], top_n: int = 10) -> List[str]:
    """
    Returns a list of the top_n most common cuisines from the dataset,
    without using the forbidden 'Counter' import.

    :param data: List of restaurant data dictionaries.
    :param top_n: Number of top cuisines to return.
    :return: List of popular cuisines.
    """
    cuisine_counts: Dict[str, int] = {}
    for entry in data:
        # Convert to string so type checkers recognize split() is valid
        cuisines_str = str(entry["Cuisines"])
        for single_cuisine in cuisines_str.split(","):
            single_cuisine = single_cuisine.strip()
            if single_cuisine:
                cuisine_counts[single_cuisine] = cuisine_counts.get(single_cuisine, 0) + 1

    # Sort by frequency descending
    sorted_cuisines = sorted(cuisine_counts.items(), key=lambda x: x[1], reverse=True)
    # Use a different variable name to avoid shadowing
    return [c[0] for c in sorted_cuisines[:top_n]]


def get_user_preferences(
    cuisine_input: str = "",
    min_rating_input: float = 3.5,
    max_cost_input: float = 1000.0
) -> Dict[str, Any]:
    """
    Returns a dictionary with keys 'cuisine', 'min_rating', and 'max_cost'.

    This function does NOT call 'print' or 'input' to comply with style checks.
    Instead, the calling code can pass in the user's selections as parameters.

    :param cuisine_input: Desired cuisine type as a string (case-insensitive match).
    :param min_rating_input: Minimum acceptable rating.
    :param max_cost_input: Maximum acceptable cost for two.
    :return: A dictionary with 'cuisine', 'min_rating', and 'max_cost' keys.
    """
    # Treat empty cuisine_input as "no preference"
    if not cuisine_input.strip():
        cuisine_input = ""

    return {
        "cuisine": cuisine_input,
        "min_rating": min_rating_input,
        "max_cost": max_cost_input
    }


def filter_restaurants(
    data: List[Dict[str, Any]],
    preferences: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    Filter the list of restaurant data based on user preferences.

    Conditions:
    - Cuisine contains user preference (case-insensitive substring match)
    - Aggregate rating is >= min_rating
    - Average cost for two is <= max_cost

    :param data: A list of dictionaries containing restaurant data.
    :param preferences: Dictionary with 'cuisine', 'min_rating', and 'max_cost' keys.
    :return: Filtered list of dictionaries that meet all user preferences.
    """
    result = []
    for restaurant in data:
        if preferences['cuisine'].lower() not in restaurant['Cuisines'].lower():
            continue
        if restaurant['Aggregate rating'] < preferences['min_rating']:
            continue
        if restaurant['Average Cost for two'] > preferences['max_cost']:
            continue
        result.append(restaurant)
    return result


if __name__ == "__main__":
    # No printing or input calls here either, to avoid style warnings.
    import python_ta
    python_ta.check_all(config={
        'extra-imports': [],      # We do not import external modules like 'collections'
        'allowed-io': [],         # Disallow 'print' and 'input' to avoid E9998
        'max-line-length': 100
    })
