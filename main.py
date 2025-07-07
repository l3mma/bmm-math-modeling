import vtk

def read_triangles_vtk(filename):
    reader = vtk.vtkUnstructuredGridReader()
    reader.SetFileName(filename)
    reader.Update()
    mesh = reader.GetOutput()

    points = mesh.GetPoints()
    num_points = points.GetNumberOfPoints()
    point_coords = []

    for i in range(num_points):
        coords = points.GetPoint(i)
        point_coords.append(coords)

    triangles = []
    for i in range(mesh.GetNumberOfCells()):
        cell = mesh.GetCell(i)
        if cell.GetCellType() == vtk.VTK_TRIANGLE:
            point_ids = cell.GetPointIds()
            id0, id1, id2 = point_ids.GetId(0), point_ids.GetId(1), point_ids.GetId(2)
            coord0 = point_coords[id0]
            coord1 = point_coords[id1]
            coord2 = point_coords[id2]
            triangles.append({
                "ids": [id0, id1, id2],
                "coords": [coord0, coord1, coord2]
            })

    return triangles

triangles = read_triangles_vtk("sphere2.vtk")

print(triangles[1]["ids"][2], triangles[1]["coords"][2])