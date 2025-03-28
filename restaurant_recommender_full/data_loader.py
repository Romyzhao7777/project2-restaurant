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
            'Restaurant Name': headers.index('name'),
            'Cuisines': headers.index('cuisines'),
            'Average Cost for two': headers.index('approx_cost(for two people)'),
            'Aggregate rating': headers.index('rate'),
            'Votes': headers.index('votes')
        }
        for row in reader:
            try:
                cost_str = row[col_idx['Average Cost for two']].replace(',', '').strip()
                entry = {
                    'Restaurant Name': row[col_idx['Restaurant Name']],
                    'Cuisines': row[col_idx['Cuisines']],
                    'Average Cost for two': float(cost_str),
                    'Aggregate rating': float(row[col_idx['Aggregate rating']]),
                    'Votes': int(row[col_idx['Votes']])
                }
                result.append(entry)
            except (ValueError, IndexError, KeyError):
                continue
    return result


# if __name__ == "__main__":
#     import doctest
#     doctest.testmod()
#
#     import python_ta
#     python_ta.check_all(config={
#         'extra-imports': ['csv'],
#         'allowed-io': ['_open_file'],
#         'max-line-length': 120
#     })
