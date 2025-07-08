import numpy as np
from vtkReader import read_triangles_vtk


def write_colored_vtk(triangles, output_path):
    points = []
    point_ID = {}
    triangles_vtk = []
    colors = []

    #assign id hashmap
    for tr in triangles:
        for coord in tr["coords"]:
            coord = tuple(coord)
            point_ID[coord] = len(points)
            points.append(coord)

    #mark triangles
    for tr in triangles:
        triangles_vtk.append([3] + [point_ID[tuple(coord)] for coord in tr["coords"]])
        if tr.get("isMarked", False):
            colors.append([255, 0, 0])
        else:
            colors.append([128, 128, 128])

    points = np.array(points, dtype=np.float64)
    with open(output_path, 'w') as f:
        f.write("# vtk DataFile Version 3.0\n")
        f.write("Colored Sphere Mesh\n")
        f.write("ASCII\n")
        f.write("DATASET UNSTRUCTURED_GRID\n\n")

        f.write(f"POINTS {len(points)} double\n")
        np.savetxt(f, points)
        f.write("\n")

        f.write(f"CELLS {len(triangles)} {len(triangles) * 4}\n")
        for tr in triangles_vtk:
            f.write(" ".join(map(str, tr)) + "\n")
        f.write("\n")

        f.write(f"CELL_TYPES {len(triangles)}\n")
        f.write("\n".join(["5"] * len(triangles)) + "\n\n")

        f.write(f"CELL_DATA {len(triangles)}\n")
        f.write("SCALARS Color unsigned_char 3\n")
        f.write("LOOKUP_TABLE default\n")
        for color in colors:
            f.write(" ".join(map(str, color)) + "\n")


triangles = read_triangles_vtk("sphere.vtk")
file_path = input("Enter file path: ")
write_colored_vtk(triangles, f"{file_path}.vtk")