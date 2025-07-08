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


with open("vtk_gen.vtk", "w") as f:
    f.write("# vtk DataFile Version 2.0\n")
    f.write("vtk_gen, Created by Gmsh 4.14.0\n")
    f.write("ASCII\n")
    f.write("DATASET UNSTRUCTURED_GRID\n\n")
    f.write(f"POINTS {len(points)} float\n")

    for x, y, z in points:
        f.write(f"{x} {y} {z}\n")
    f.write("\n")

    f.write(f"CELLS {len(points)} {len(points) * 2}\n")

    for i in range(len(points)):
        f.write(f"1 {i}\n")

    f.write("\n")

    f.write(f"CELL_TYPES {len(points)}\n")

    for _ in range(len(points)):
        f.write("1\n")