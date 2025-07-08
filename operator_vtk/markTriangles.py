import pyvista as pv
import numpy as np
from vtkReader import read_triangles_vtk
import meshio

all_points = []
triangles = read_triangles_vtk("sphere1.vtk")

point_id = {}

for tr in triangles:
    for coord in tr["coords"]:
        coord_tuple = tuple(coord)
        point_id[coord_tuple] = len(all_points)
        all_points.append(coord)


points = np.array(all_points, dtype=np.float64)
triangles = []
is_marked = []

for tri in triangles:
    vertex_ids = [point_id[tuple(coord)] for coord in tri["coords"]]
    triangles.append(vertex_ids)
    is_marked.append(1 if tri["isMarked"] else 0)

triangles = np.array(triangles, dtype=np.int32)
is_marked = np.array(is_marked, dtype=np.int32)


mesh = meshio.Mesh(
    points=points,
    cells=[("triangle", triangles)],  # Указываем тип ячеек (треугольники)
    cell_data={"isMarked": [is_marked]}  # Данные для раскраски
)

mesh.write("marked_triangles.vtk", file_format="vtk")  # или "vtk-ascii"

