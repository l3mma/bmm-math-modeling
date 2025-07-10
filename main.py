import numpy as np
from particle_generator import sphere_cloud
from vtk_reader import vtk_reader_cells, vtk_reader_nodes
import ray_tracing
from config_reader import read_config
from marker_cell import marker_cell
import meshio

_params = read_config("config.txt")

print(_params)
models = 'test_file.vtk'
sphere_cloud(_params['distribution_type'], _params['Numder_of_particles'],_params['Radius'],_params['Path_cloud'])
particles = _params['Path_cloud'] + "\\particles.vtk"

print(particles)
source_coords = _params["Source"]
cells = vtk_reader_cells(models)
nodes = vtk_reader_nodes(models)
nodes_p = vtk_reader_nodes(particles)
cell_param = np.zeros(len(cells))

for part_num in range(len(nodes_p)):
    length = 0
    answer = 0
    interaction, min_interaction = [], [-1, 0]
    for cell_num in range(len(cells)):
        answer, length = ray_tracing.ray_tracing_check(source_coords, nodes_p[part_num], nodes[cells[cell_num][0]], nodes[cells[cell_num][1]], nodes[cells[cell_num][2]])
        if answer == True:
            interaction = [length, cell_num]
            if interaction[0] >= min_interaction[0]:
                min_interaction = interaction
    if min_interaction[0] >= 0:
        cell_param[min_interaction[1]] = 1

# for part_num in range(len(nodes_p)):
#     length = 0
#     answer = 0
#     interactions, min_ray = [], []
#     for cell_num in range(len(cells)):
#         answer, length = ray_tracing.ray_tracing_check(source_coords, nodes_p[part_num], nodes[cells[cell_num][0]], nodes[cells[cell_num][1]], nodes[cells[cell_num][2]])
#         if answer == True:
#             interactions.append([length, cell_num])
#     if len(interactions) != 0:
#         min_ray = min(interactions, key = lambda x: x[0])
#         cell_param[min_ray[1]] = 1

print(cell_param)
path_save = _params['Path_cloud']
marker_cell(nodes, cells, cell_param, path_save)
