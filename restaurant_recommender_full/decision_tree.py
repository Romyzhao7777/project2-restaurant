"""
decision_tree.py - Collects user input and filters restaurant dataset.
"""


def get_user_preferences():
    """
       Prompt user for their preferences.

       Asks for:
       - Cuisine type (e.g., Indian, Chinese)
       - Minimum acceptable rating (float)
       - Maximum acceptable cost for two (float)

       :return: A dictionary with keys 'cuisine', 'min_rating', and 'max_cost'.
       """
    print("Welcome to the Restaurant Recommender!")
    cuisine = input("Enter desired cuisine type (e.g., Indian, Chinese): ")
    min_rating = float(input("Minimum rating (e.g., 3.5): "))
    max_cost = float(input("Maximum cost for two (e.g., 1000): "))
    return {"cuisine": cuisine, "min_rating": min_rating, "max_cost": max_cost}


def filter_restaurants(data, preferences):
    """
       Filter the list of restaurant data based on user preferences.

       Conditions:
       - Cuisine contains user preference (case-insensitive substring match)
       - Aggregate rating is greater than or equal to minimum rating
       - Average cost for two is less than or equal to maximum cost

       :param data: A list of dictionaries containing restaurant data.
       :param preferences: Dictionary with 'cuisine', 'min_rating', and 'max_cost' keys.
       :return: Filtered list of dictionaries that meet all user preferences.
       """
    result = []
    for r in data:
        if preferences['cuisine'].lower() not in r['Cuisines'].lower():
            continue
        if r['Aggregate rating'] < preferences['min_rating']:
            continue
        if r['Average Cost for two'] > preferences['max_cost']:
            continue
        result.append(r)
    return result
