import numpy as np
from config import *

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

def origin_point(HEIGHT):
    return np.array([0.0, 0.0, HEIGHT])

def generate_pt_inside(A_COEFF, B_COEFF, HEIGHT, NUM_POINTS):
    points = []
    while len(points) < NUM_POINTS:
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

origin_pt = rotation(origin_point(HEIGHT), ANGLE_X, ANGLE_Y, ANGLE_Z)
inner_pt = generate_pt_inside(A_COEFF, B_COEFF, HEIGHT, NUM_POINTS)
rotated_pt = rotation(inner_pt, ANGLE_X, ANGLE_Y, ANGLE_Z)

with open("../vtk_gen.vtk", "w") as f:
    f.write("# vtk DataFile Version 2.0\n")
    f.write("vtk_gen, Created by Gmsh 4.14.0\n")
    f.write("ASCII\n")
    f.write("DATASET UNSTRUCTURED_GRID\n\n")
    f.write(f"POINTS {len(inner_pt)} float\n")

    for x, y, z in inner_pt:
        f.write(f"{x} {y} {z}\n")
    f.write("\n")

    f.write(f"CELLS {len(inner_pt)} {len(inner_pt) * 2}\n")

    for i in range(len(inner_pt)):
        f.write(f"1 {i}\n")

    f.write("\n")

    f.write(f"CELL_TYPES {len(inner_pt)}\n")

    for _ in range(len(inner_pt)):
        f.write("1\n")