from pointGen import points

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