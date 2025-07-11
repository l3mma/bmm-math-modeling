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
    _nodes = mesh.points
    return _nodes