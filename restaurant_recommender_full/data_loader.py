"""
data_loader.py - Load and clean Zomato CSV with field limit fix and manual header mapping.
"""

import csv
from typing import Any, Dict, List, TextIO


def _open_file(filepath: str) -> TextIO:
    """
    Open a file for reading with UTF-8 encoding.

    This helper function encapsulates the call to open() so that it can be
    explicitly listed in the allowed-io configuration.

    :param filepath: Path to the file.
    :return: A file object opened for reading.
    """
    return open(filepath, "r", encoding="utf-8")


def load_and_preprocess_data(filepath: str) -> List[Dict[str, Any]]:
    """
    Load and preprocess restaurant data from a CSV file.

    Fields extracted:
    - name → 'Restaurant Name'
    - cuisines → 'Cuisines'
    - approx_cost(for two people) → 'Average Cost for two'
    - rate → 'Aggregate rating'
    - votes → 'Votes'

    Handles:
    - Column name mapping
    - Comma removal from cost
    - Value conversion and exception handling

    :param filepath: Path to Zomato CSV file.
    :return: List of cleaned restaurant data dictionaries.
    """
    # Set the CSV field size limit inside the function
    csv.field_size_limit(10**7)
    result: List[Dict[str, Any]] = []
    with _open_file(filepath) as f:
        reader = csv.reader(f)
        headers = next(reader)
        col_idx = {
            'name': headers.index('name'),
            'cuisines': headers.index('cuisines'),
            'rate': headers.index('rate'),
            'approx_cost(for two people)': headers.index('approx_cost(for two people)'),
            'votes': headers.index('votes'),
            'location': headers.index('location'),
            'url': headers.index('url')
        }
        for row in reader:
            try:
                cost_str = row[col_idx['approx_cost(for two people)']].replace(',', '').strip()
                entry = {
                    'name': row[col_idx['name']],
                    'cuisines': row[col_idx['cuisines']],
                    'rate': float(row[col_idx['rate']]),
                    'approx_cost(for two people)': float(cost_str),
                    'votes': int(row[col_idx['votes']]),
                    'location': row[col_idx['location']],
                    'url': row[col_idx['url']]
                }
                result.append(entry)
            except (ValueError, IndexError, KeyError):
                continue
    return result


# if __name__ == "__main__":
#     import doctest
#
#     doctest.testmod()
#
#     import python_ta
#
#     python_ta.check_all(config={
#         'extra-imports': ['csv'],
#         'allowed-io': ['_open_file'],
#         'max-line-length': 120
#     })
