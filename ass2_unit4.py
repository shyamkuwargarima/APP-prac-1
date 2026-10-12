
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

numbers = rng.integers(1, 100, 10)

labels = [
    "Maths", "Physics", "Chemistry", "English", "Python",
    "DBMS", "DSA", "OS", "Computer", "AI"
]

series = pd.Series(numbers, index=labels)

print(series)
