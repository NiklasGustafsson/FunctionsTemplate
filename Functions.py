from __future__ import annotations
import itertools
import pandas as pd

def myadd(x, y):
    """Basic addition test"""
    return x + y


def badadd(x : float, y : float) -> float:
    """Another addition test"""
    return x + y + 1


def get_table() -> NumberMatrix:
    """Ensure list-of-list can be returned"""
    return [[1, 2], [3, 4]]


def get_table_2() -> pd.DataFrame:
    """Ensure DataFrame can be returned"""
    return pd.DataFrame([[1, 2], [3, 4]])


# Constants should not be exported
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


# Underscore-prefixed names should not be exported
def _column_names():
    yield from alphabet
    for i in itertools.count(start=1):
        yield from (f"{c}{i}" for c in alphabet)


def get_pandas(rows : int, columns : int) -> NumberMatrix:
    """Ensure pandas DataFrames can be returned

    rows: Number of rows to generate

    columns: Number of columns to generate

    Returns: two-dimensional matrix of random numbers"""
    import numpy as np
    import pandas as pd
    data = np.random.rand(rows, columns)
    column_names = list(itertools.islice(_column_names(), columns))
    df = pd.DataFrame(data, columns=column_names)
    return df


def get_names(columns : int) -> StringMatrix:
    """Test returning a matrix of strings

    columns: Number of columns worth of names to return"""
    return [list(itertools.islice(_column_names(), columns))]
