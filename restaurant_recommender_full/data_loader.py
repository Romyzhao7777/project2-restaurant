"""
data_loader.py - Load and clean Zomato CSV with field limit fix and manual header mapping.
"""

import csv


def load_and_preprocess_data(filepath: str) -> list[dict[str, object]]:
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
    csv.field_size_limit(10**7)

    result = []
    with open(filepath, "r", encoding="utf-8") as f:
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


if __name__ == "__main__":
    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['csv'],
        'allowed-io': ['open', 'print'],
        'max-line-length': 100
    })

