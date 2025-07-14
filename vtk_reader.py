import meshio

def vtk_reader(path):
    mesh = meshio.read(path)
    
    _nodes = mesh.points
    _cell_data = mesh.cell_data
    _point_data = mesh.point_data

    cells = []
    for cell_block in mesh.cells:
        cells.append(cell_block.data)
    _cells = cells[2]
    
    return _cells, _nodes, _cell_data, _point_data
