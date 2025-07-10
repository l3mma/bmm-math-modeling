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

class Cone:
    def __init__(self, a_coeff, b_coeff, height, num_points):
        self.a_coeff = a_coeff
        self.b_coeff = b_coeff
        self.height = height
        self.num_points = num_points
        self.points = None

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

    def generate_points(self):
        points = []
        while len(points) < self.num_points:
            z = np.random.uniform(self.height / 2, self.height)
            scale = 1 - z / self.height
            r = np.sqrt(np.random.uniform(0, 1))
            angle = np.random.uniform(0, 2 * np.pi)
            x = self.a_coeff * r * scale * np.cos(angle)
            y = self.b_coeff * r * scale * np.sin(angle)
            points.append([x, y, z])
        self.points = np.array(points)
        return self.points

    def rotate(self, angle_x=0, angle_y=0, angle_z=0):
        if self.points is None:
            raise ValueError("No points generated yet. Call generate_points() first.")

        R_x = self.rotation_x(angle_x)
        R_y = self.rotation_y(angle_y)
        R_z = self.rotation_z(angle_z)
        R_total = R_z @ R_y @ R_x
        self.points = self.points @ R_total.T
        return self.points
