import numpy as np
import matplotlib.pyplot as plt

A_COEFF, B_COEFF = 1, 1
HEIGHT = 10
ANGLE_X = 90
ANGLE_Y = -30
ANGLE_Z = -45
NUM_POINTS = 100
SLICES = 21

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

def create_cone_surface(A_COEFF,B_COEFF, HEIGHT, SLICES):
    points = []
    for z in np.linspace(2, HEIGHT, SLICES):
        scale = 1 - z/HEIGHT
        for angle in np.linspace(0, 2 * np.pi):
            x = A_COEFF * scale * np.cos(angle)
            y = B_COEFF * scale * np.sin(angle)
            points.append([x, y, z])
    return np.array(points)

def generate_pt_inside(A_COEFF, B_COEFF, HEIGHT, NUM_POINTS):
    points = []
    while  len(points) < NUM_POINTS:
        z = np.random.uniform(HEIGHT/2,HEIGHT)
        scale = 1 - z/HEIGHT
        r = np.sqrt(np.random.uniform(0,1))
        angle = np.random.uniform(0, 2 * np.pi)
        x = A_COEFF * r * scale * np.cos(angle)
        y = B_COEFF * r * scale * np.sin(angle)
        points.append([x, y, z])
    return np.array(points)

# (R_total @ points.T).T -> points @ R_total.T
# (3,N).T -> (N,3)
def rotation(points, angle_x, angle_y, angle_z):
    R_x = rotation_x(angle_x)
    R_y = rotation_y(angle_y)
    R_z = rotation_z(angle_z)
    R_total = R_z @ R_y @ R_x
    return points @ R_total.T

cone_surface = create_cone_surface(A_COEFF, B_COEFF, HEIGHT,SLICES)
inner_pt = generate_pt_inside(A_COEFF, B_COEFF, HEIGHT, NUM_POINTS)
rotated_cone = rotation(cone_surface, ANGLE_X, ANGLE_Y, ANGLE_Z)
rotated_pt = rotation(inner_pt, ANGLE_X, ANGLE_Y, ANGLE_Z)


fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')

ax.scatter(rotated_cone[:, 0], rotated_cone[:, 1], rotated_cone[:, 2],
           s=10, c='blue', alpha=0.3)

ax.scatter(rotated_pt[:, 0], rotated_pt[:, 1], rotated_pt[:, 2],
           s=10, c='red', alpha=0.5)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.tight_layout()
plt.show()