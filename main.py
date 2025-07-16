import numpy as np
from particle_generator import sphere_cloud, cone_cloud
from vtk_reader import vtk_reader
import ray_tracing
from vtk_writer import dict_param, vtk_writer
from config_reader import parse_config
from area_calculation import interaction_area
import time
from combiner import conbine_models
import logging

logging.basicConfig(filename='info.log', level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

config = parse_config("config.txt")
models_params = config['models']
clouds = config['clouds']
path_dir = config['project_directory'][0]['path']
particles = []
source_points = []

for cloud in clouds:
    if cloud['figure_type'] == 'sphere':
        particles.append(sphere_cloud(cloud['number_of_particles'], cloud['radius'],
                 cloud["source"], cloud['distribution_type'], cloud['sigma_r']))
        source_points.append(cloud["source"])
    elif cloud['figure_type'] == 'sphere':
        particles.append(cone_cloud(cloud['number_of_particles'], cloud['radius'],
                 cloud["source"], cloud['distribution_type'], cloud['sigma_r'], cloud["height"], cloud['orientation_angle'],
                    cloud['sigma_z']))
    else:
        raise ValueError("Неизвестная форма облака частиц")

# models = []
cells, nodes, _, _ = vtk_reader(models_params[0]["path"])
orginal_model_p = {}
orginal_model_p[models_params[0]["path"].split('\\')[-1]] = {'num_cell': len(cells), 'num_nodes': len(nodes)}
for i in range(1, len(models_params)):
    path = models_params[i]["path"]
    cells, nodes = conbine_models(cells, nodes, path)
    orginal_model_p[path.split('\\')[-1]] = {'num_cell': len(cells), 'num_nodes': len(nodes)}


cell_param = np.zeros((len(cells), 1))
#print('cell', cells)
# print('nodes', nodes)

# print(orginal_model_p)
start_time = time.time()
num_cloud = 0
for cloud in particles:

    for part_num in range(len(cloud)):
        length = 0
        answer = 0
        interaction, min_interaction = [], []
        for cell_num in range(len(cells)):
            answer, length = ray_tracing.ray_tracing_check(source_points[num_cloud], cloud[part_num], nodes[cells[cell_num]])
            if answer == True:
                interaction.append([length, cell_num])
        if len(interaction) != 0:
            min_interaction = min(interaction, key = lambda x: x[0])
            cell_param[min_interaction[1]] += 1
    num_cloud += 1


color_cells = {}
color_cells = dict_param(color_cells, 'color', cell_param)
vtk_writer(path_dir, nodes, cells, color_cells)

all_area = interaction_area(nodes, cells)

end_time = time.time()
_time = end_time - start_time

logging.info(f"The program has successfully completed it`s work!\n"
             f"Affected numbers particle: {sum(cell_param)} %\n"
             f"All numbers particle: {np.array(particles).size / 3}\n"
             f"Probability: {sum(cell_param) / (np.array(particles).size / 3)}\n"
             f"Operating time: {_time}\n"
             f"Numbers of cells and rays: {len(cells)} * {np.array(particles).size / 3} = {len(cells) * np.array(particles).size / 3}\n")


