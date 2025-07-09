from vtk_reader import *
from vtk_gen import rotation_z
import ray_tracing
from cfg import HEIGHT, ANGLE_Z
import numpy as np

models = 'output.vtk'
particles = "vtk_gen.vtk"

Z_ROTATION = rotation_z(ANGLE_Z)
source_coords = Z_ROTATION @ np.array([0.0, 0.0, HEIGHT])

cells = vtk_reader_cells(models)
nodes = vtk_reader_nodes(models)
nodes_p = vtk_reader_nodes(particles)
cell_param = np.zeros(len(cells))

for cell_num in range(len(cells)):
    for part_num in range(len(nodes_p)):
        sc = source_coords
        particle = nodes_p[part_num]
        v0 = nodes[cells[cell_num][0]]
        v1 = nodes[cells[cell_num][1]]
        v2 = nodes[cells[cell_num][2]]
        if ray_tracing.ray_tracing_check(sc, particle, v0, v1, v2):
            cell_param[cell_num] += 1

with open("output_colored.vtk", "w") as f:
    f.write("# vtk DataFile Version 2.0\n")
    f.write("Colored Mesh with Intersections\n")
    f.write("ASCII\n")
    f.write("DATASET UNSTRUCTURED_GRID\n\n")
    f.write(f"POINTS {len(nodes)} float\n")

    for x, y, z in nodes:
        f.write(f"{x} {y} {z}\n")
    f.write("\n")
    f.write(f"CELLS {len(cells)} {len(cells) * 4}\n")
    for cell in cells:
        f.write(f"3 {cell[0]} {cell[1]} {cell[2]}\n")
    f.write("\n")

    # triangle type 5
    f.write(f"CELL_TYPES {len(cells)}\n")
    for _ in cells:
        f.write("5\n")
    f.write("\n")

    # color cells
    f.write(f"CELL_DATA {len(cells)}\n")
    f.write("SCALARS cell_color float 3\n")  # RGB
    f.write("LOOKUP_TABLE custom_colors\n")
    for param in cell_param:
        if param > 0:
            f.write("1.0 0.0 0.0\n")
        else:
            f.write("0.7 0.7 0.7\n")
    f.write("\n")