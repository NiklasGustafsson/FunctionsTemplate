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


PNG = b'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'

def get_image():
    """Return an image"""
    return {"result": PNG, "resultType": "image"}
