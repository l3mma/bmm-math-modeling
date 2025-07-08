
import numpy as np
import vtk_reader
import ray_tracing

models = 'test11.vtk'
particles = "vtk_gen.vtk"

sourse_coords = [5, 5, 5]
cells = vtk_reader.vtk_reader_cells(models)
nodes = vtk_reader.vtk_reader_nodes(models)
nodes_p = vtk_reader.vtk_reader_nodes(particles) + 3
cell_param = np.zeros(len(cells))


for cell_num in range(len(cells)):
    for part_num in range(len(nodes_p)):
        cell_param[cell_num] += ray_tracing.ray_tracing(sourse_coords, nodes_p[part_num], nodes[cells[cell_num][0]], nodes[cells[cell_num][1]], nodes[cells[cell_num][2]])

print(cell_param)