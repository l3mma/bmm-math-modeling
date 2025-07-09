from numpy import cross, dot, array
from operator_vtk.vtk_gen import *

def ray_tracing_check(orig, part_point, point0, point1, point2):

    E1 = array(point1) - array(point0)
    E2 = array(point2) - array(point0)
    D = array(part_point) - array(orig)
    T = array(orig) - array(point0)
    total_det = dot(cross(D, E2), E1)

    if total_det == 0:
        return False

    t = dot(cross(T, E1), E2) / total_det
    u = dot(cross(D, E2), T) / total_det
    v = dot(cross(T, E1), D) / total_det

    if u >= 0 and v >= 0 and (u + v) <= 1:
        return True
    else:
        return False