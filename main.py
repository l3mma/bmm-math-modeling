from operator_vtk.vtk_reader import *
from operator_vtk.vtk_gen import rotation_z
import ray_tracing
from config import HEIGHT, ANGLE_Z

models = 'abcd.vtk'
particles = "vtk_gen.vtk"

source_coords = rotation_z(ANGLE_Z) @ np.array([0.0, 0.0, HEIGHT])

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
        cell_param[cell_num] += ray_tracing.ray_tracing_check(sc,particle,v0,v1,v2)

print(cell_param)