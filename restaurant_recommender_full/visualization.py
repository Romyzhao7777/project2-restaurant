"""
visualization.py - Displays ranked restaurants using Plotly bar chart.
"""

import plotly.graph_objects as go


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


# if __name__ == "__main__":
#     import doctest
#     doctest.testmod()
#
#     import python_ta
#     python_ta.check_all(config={
#         'extra-imports': ['plotly.graph_objects'],
#         'allowed-io': [],
#         'max-line-length': 120
#     })
