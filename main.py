import numpy as np
from particle_generator import sphere_cloud, cone_cloud
from vtk_reader import vtk_reader_cells, vtk_reader_nodes
import ray_tracing
from config_reader import read_config
from marker_cell import marker_cell, interaction_area
import time

_params = read_config("config.txt")
print(_params)
if _params['Figure_type'] == 'sphere':
    sphere_cloud(_params['Numder_of_particles'], _params['Radius'], _params['Path_cloud'],
                 _params["Source"], _params['distribution_type'])
else:
    cone_cloud(_params['Numder_of_particles'], _params['Radius'], _params['Path_cloud'],
                 _params["Source"], _params["height_cone"], _params['Orientation_angle'],_params['distribution_type'])

model = _params["Model"]
particles = _params['Path_cloud'] + "\\particles.vtk"
source_coords = _params["Source"]
cells = vtk_reader_cells(model)
nodes = vtk_reader_nodes(model)
nodes_p = vtk_reader_nodes(particles)
cell_param = np.zeros(len(cells))

start_time = time.time()
for part_num in range(len(nodes_p)):
    length = 0
    answer = 0
    interaction, min_interaction = [], []
    for cell_num in range(len(cells)):
        answer, length = ray_tracing.ray_tracing_check(source_coords, nodes_p[part_num], nodes[cells[cell_num][0]], nodes[cells[cell_num][1]], nodes[cells[cell_num][2]])
        if answer == True:
            interaction.append([length, cell_num])
    if len(interaction) != 0:
        min_interaction = min(interaction, key = lambda x: x[0])
        cell_param[min_interaction[1]] += 1

path_save = _params['Path_cloud']
marker_cell(nodes, cells, cell_param, path_save)
np.savetxt('cell_data.txt', cell_param)

percent, all_area = interaction_area(cell_param, len(cells), nodes, cells)

end_time = time.time()
_time = end_time - start_time

print('Процент поражённой площади:', percent * 100,"%")
print("Вся площадь:", all_area)
print("Время выполнения программы:",_time, 'при числе ячеек Х лучей =', len(cells) * len(nodes_p))


