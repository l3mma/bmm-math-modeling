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
print('Конфигурационный файл успешно прочитан!')
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
print('Облако частиц успешно создано!')

# models = []
cells, nodes, _, _ = vtk_reader(models_params[0]["path"])
orginal_model_p = {}
orginal_model_p[models_params[0]["path"].split('\\')[-1]] = {'num_cell': len(cells), 'num_nodes': len(nodes)}
for i in range(1, len(models_params)):
    path = models_params[i]["path"]
    cells, nodes = conbine_models(cells, nodes, path)
    orginal_model_p[path.split('\\')[-1]] = {'num_cell': len(cells), 'num_nodes': len(nodes)}

num_cloud_particles = int(np.array(particles).size / 3)
point_data_vec_c = np.zeros((num_cloud_particles, 3))
point_data_scal_c = np.zeros((num_cloud_particles, 1))

cell_data = {}
cell_param_all = np.zeros((len(cells), 1))
#print('cell', cells)
# print('nodes', nodes)

# print(orginal_model_p)
start_time = time.time()
num_cloud = 0
index_cloud = 0
print('Начат процесс пересечения частиц и моделей успешно выполнено!')
for cloud in particles:
    cell_param = np.zeros((len(cells), 1))
    for part_num in range(len(cloud)):
        length = 0
        answer = 0
        interaction, min_interaction = [], []
        for cell_num in range(len(cells)):
            answer, length = ray_tracing.ray_tracing_check(source_points[num_cloud], cloud[part_num], nodes[cells[cell_num]])
            vector = cloud[part_num] - source_points[num_cloud]
            point_data_vec_c[part_num + index_cloud] = vector / np.linalg.norm(vector)

            if answer == True:
                interaction.append([length, cell_num])
                point_data_scal_c[part_num + index_cloud] = 1

        if len(interaction) != 0:
            min_interaction = min(interaction, key = lambda x: x[0])
            cell_param[min_interaction[1]] += 1
    cell_param_all += cell_param
    num_cloud += 1
    cell_data = dict_param(cell_data, f'cloud_{num_cloud}', cell_param)
    index_cloud += len(cloud)
    # vtk_writer(f'B:\\GMM_2025\\v5\\bmm-math-modeling-MayorIvan1-patch-1\\clouds-{num_cloud}.vtk', cloud)
print('Обработка процесса пересечения частиц и моделей успешно выполнено!')
point_data = {}
point_data_vec_m = np.zeros((len(nodes), 3))
point_data_vec = np.vstack([point_data_vec_m, point_data_vec_c])
point_data = dict_param(point_data, 'trace_vector', point_data_vec)
point_data_scal_m = np.zeros((len(nodes), 1))
point_data_scal = np.vstack([point_data_scal_m, point_data_scal_c])
point_data = dict_param(point_data, 'interaction', point_data_scal)

cell_data = dict_param(cell_data, f'cloud_all', cell_param_all)


points_cloud = []
points_all = np.vstack([nodes, particles[0]])
for cloud in range(1,len(particles)):
    points_all = np.vstack([points_all, particles[cloud]])


point_data_scal_m = np.zeros((len(nodes), 1))
point_data_scal_c = np.ones((num_cloud_particles, 1))
point_data_scal = np.vstack([point_data_scal_m, point_data_scal_c])
point_data = dict_param(point_data, 'mass_point', point_data_scal)


# color_cells = {}
# color_cells = dict_param(color_cells, 'color', cell_param)
vtk_writer(path_dir, points_all, cells, cell_data, point_data)

all_area = interaction_area(nodes, cells)

end_time = time.time()
_time = end_time - start_time

print(f'Время выполнения работы программы: {_time} сек')

logging.info(f"The program has successfully completed it`s work!\n"
             f"Affected numbers particle: {sum(cell_param_all)} %\n"
             f"All numbers particle: {np.array(particles).size / 3}\n"
             f"Probability: {sum(cell_param_all) / (np.array(particles).size / 3)}\n"
             f"Operating time: {_time}\n"
             f"Numbers of cells and rays: {len(cells)} * {np.array(particles).size / 3} = {len(cells) * np.array(particles).size / 3}\n")


