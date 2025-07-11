import numpy as np
from vtk_generator import vtk_point_generator
import matplotlib.pyplot as plt
def sphere_cloud(distribution, num_points, radius, path_particles, center, sigma=0.5):

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

# def plot_parts(points):
#     fig = plt.figure(figsize=(10,7))
#     ax = fig.add_subplot(111, projection='3d')
#     ax.scatter(points[:,0], points[:,1], points[:,2],s=10,alpha=0.6)
#     ax.set_xlabel("X")
#     ax.set_xlabel("Y")
#     ax.set_xlabel("Z")
#     plt.show()
#
# n = 2000
# center = [9, 4, 5]
# R = 2
# points = sphere_cloud('gaussian',n,R,0, center)
#
# plot_parts(points)

def cone_cloud(A_COEFFICENT, B_COEFFICENT, RADIUS, HEIGHT,  NUM_POINTS,LEVELS):
    points = []
    ANGLE_OF_17_SIDES_TRIANGLE = 2 * np.pi / 17
    for z in np.linspace(0, HEIGHT, LEVELS):
        scale = 1 - z/HEIGHT
        for angle in np.linspace(0, 2 * np.pi, ANGLE_OF_17_SIDES_TRIANGLE):
            x = A_COEFFICENT * scale * RADIUS * np.cos(angle)
            y = B_COEFFICENT * scale * RADIUS * np.sin(angle)
            points = np.vstack([x, y, z]).T

    return points

