import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd

try:
    R = int(input("Inter radius of missile: "))
    assert R > 0
except AssertionError as e:
    print("Negative radius")
    exit()
try:
    N = int(input("Inter number of shattered pieces: "))
    assert N > 0
except AssertionError as e:
    print("Negative number of shattered pieces")
    exit()

d = input("""
    TYPE DISTRIBUTION:
    1) GAUSSIAN
    2) POISSON
    3) UNIFORM
""").lower()

points = []
match d:
    case "gaussian":
        points = np.random.randn(N, 3)
    case "poisson":
        points = np.column_stack([np.random.poisson(R / 2, N), np.random.poisson(R / 2, N), np.random.poisson(R / 2, N)])
    case "uniform":
        points = np.random.uniform(low = -R, high = R, size = (N,3))

distances = np.linalg.norm(points, axis=1)
points_inside = points[distances <= R]