import numpy as np
from vtk_generator import vtk_point_generator
import matplotlib.pyplot as plt
def sphere_cloud(num_points, radius, path_particles, center=[0,0,0], distribution = 'uniform', sigma=0.5):

    if distribution == 'uniform':
        phi = np.random.uniform(0, 2 * np.pi, num_points)
        theta = np.arccos(np.random.uniform(-1, 1, num_points))
        rho = np.random.uniform(0, 1, num_points)
        r = radius * np.sqrt(rho)
        x = r * np.sin(theta) * np.cos(phi)
        y = r * np.sin(theta) * np.sin(phi)
        z = r * np.cos(theta)
        points = np.vstack([x, y, z]).T
        vtk_point_generator(points + center, path_particles)

    elif distribution == 'gaussian':
        x = np.random.normal(0, sigma, num_points)
        y = np.random.normal(0, sigma, num_points)
        z = np.random.normal(0, sigma, num_points)
        x /= (abs(x).max() / radius)
        y /= (abs(y).max() / radius)
        z /= (abs(z).max() / radius)

        points = np.vstack([x, y, z]).T
        vtk_point_generator(points + center, path_particles)

    else:
        raise ValueError("Неизвестное распределение")

    return points + center

def cone_cloud(num_points, radius, path_particles, center, height, angle_rot, distribution='uniform',sigma=0.5):
    if distribution == 'uniform':
        z = np.sqrt(np.random.uniform(0, 1, num_points)) * height
        r = (z / height) * radius * np.sqrt(np.random.uniform(0, 1, num_points))
        angles = np.random.uniform(0, 2 * np.pi, num_points)
        x = r * np.cos(angles)
        y = r * np.sin(angles)

        points = np.vstack([x, y, z]).T

        points = rotate(points, angle_rot)
        vtk_point_generator(points + center, path_particles)

    return points + center

def rotation_x(angle):
    theta = np.radians(angle)
    return np.array([
        [1, 0, 0],
        [0, np.cos(theta), -np.sin(theta)],
        [0, np.sin(theta), np.cos(theta)]
    ])

def rotation_y(angle):
    theta = np.radians(angle)
    return np.array([
        [np.cos(theta), 0, np.sin(theta)],
        [0, 1, 0],
        [-np.sin(theta), 0, np.cos(theta)]
    ])

def rotation_z(angle):
    theta = np.radians(angle)
    return np.array([
        [np.cos(theta), -np.sin(theta), 0],
        [np.sin(theta), np.cos(theta), 0],
        [0, 0, 1]
    ])


def rotate(points, angle_rot):
    angle_x, angle_y, angle_z = angle_rot
    R_x = rotation_x(angle_x)
    R_y = rotation_y(angle_y)
    R_z = rotation_z(angle_z)
    R_total = R_z @ R_y @ R_x
    points = points @ R_total.T
    return points
