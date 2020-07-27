
def myadd(x, y):
    return x + y

def badadd(x : float, y : float) -> float:
    return x + y + 1

def get_table() -> "NumberMatrix":
    return [[1, 2], [3, 4]]

def get_pandas(rows : int, columns : int) -> "NumberMatrix":
    import numpy as np
    import pandas as pd
    data = np.random.rand(rows, columns)
    column_names = [chr(ord('A') + x) for x in range(columns)]
    df = pd.DataFrame(data, columns=column_names)
    return df
