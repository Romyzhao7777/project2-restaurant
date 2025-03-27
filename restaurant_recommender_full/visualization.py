"""
visualization.py - Displays ranked restaurants using Plotly bar chart.
"""

import plotly.graph_objects as go


def visualize_rankings(rankings):
    """
    Plot top 10 ranked restaurants using a horizontal bar chart.

    :param rankings: List of (restaurant name, PageRank score) tuples, sorted descending.
    """
    top = rankings[:10]
    names = [name for name, _ in top]
    scores = [score for _, score in top]

    fig = go.Figure(data=[
        go.Bar(x=scores, y=names, orientation='h', marker=dict(color='royalblue'))
    ])
    fig.update_layout(
        title='Top 10 Recommended Restaurants',
        xaxis_title='PageRank Score',
        yaxis_title='Restaurant',
        yaxis=dict(autorange='reversed')  # top rank at top
    )
    fig.show()
