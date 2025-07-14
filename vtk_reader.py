import meshio

def vtk_reader_cells(path):
    mesh = meshio.read(path)

    cells = []
    for cell_block in mesh.cells:
        cells.append(cell_block.data)
    _cells = cells[2]
    return _cells

def vtk_reader_nodes(path):
    mesh = meshio.read(path)
    _nodes = mesh.pointsimport meshio

def vtk_reader_cells(path):
    mesh = meshio.read(path)

    cells = []
    for cell_block in mesh.cells:
        cells.append(cell_block.data)
    _cells = cells
    return _cells

def vtk_reader_nodes(path):
    mesh = meshio.read(path)
    _nodes = mesh.points
    return _nodes

def vtk_reader_cell_data(path):
    mesh = meshio.read(path)
    _cell_data = mesh.cell_data
    return _cell_data

def vtk_reader_point_data(path):
    mesh = meshio.read(path)
    _point_data = mesh.point_data
    return _point_data
    return _nodes
