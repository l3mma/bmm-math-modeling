import meshio
import numpy as np


def vtk_reader_cells(path):
    mesh = meshio.read(path)

    cells = []
    for cell_block in mesh.cells:
        cells.append(cell_block.data)
    _cells = cells[2]
    return _cells

def vtk_reader_nodes(path):
    mesh = meshio.read(path)
    _nodes = mesh.points
    return _nodes

def markedProperty(nodes):
    marked_nodes = np.column_stack((nodes, np.zeros(len(nodes))
    return marked_nodes

cells = vtk_reader_cells("sphere.vtk")
nodes = markedProperty(vtk_reader_nodes("sphere.vtk"))

print(nodes)