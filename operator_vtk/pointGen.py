import numpy as np

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

d = int(input("""
    TYPE DISTRIBUTION:
    1) GAUSSIAN
    2) POISSON
    3) UNIFORM
"""))

points = []
match d:
    case 1:
        points = np.random.randn(N, 3)
    case 2:
        x = np.random.poisson(1, N)
        y = np.random.poisson(1, N)
        z = np.random.poisson(1, N)
        points = np.column_stack([x,y,z])
    case 3:
        points = np.random.uniform(low = 0, high = R, size = (N,3))