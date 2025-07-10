import numpy as np
from vtk_generator import vtk_point_generator
def sphere_cloud(distribution, num_points, radius, path_particles, sigma=0.5):

    if distribution == 'uniform':
        phi = np.random.uniform(0, 2 * np.pi, num_points)
        theta = np.arccos(np.random.uniform(-1, 1, num_points))
        u = np.random.uniform(0, 1, num_points)
        r = radius * np.cbrt(u)
        x = r * np.sin(theta) * np.cos(phi)
        y = r * np.sin(theta) * np.sin(phi)
        z = r * np.cos(theta)
        points = np.vstack([x, y, z]).T
        vtk_point_generator(points, path_particles)

    elif distribution == 'gaussian':
        x = np.random.normal(0, sigma, num_points)
        y = np.random.normal(0, sigma, num_points)
        z = np.random.normal(0, sigma, num_points)
        x /= (abs(x).max() / radius)
        y /= (abs(y).max() / radius)
        z /= (abs(z).max() / radius)

        points = np.vstack([x, y, z]).T
        vtk_point_generator(points, path_particles)

    else:
        raise ValueError("Неизвестное распределение")

    return points