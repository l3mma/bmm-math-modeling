def vtk_writer(path_particles, points, cells=[], cells_data=[], points_data=[]):
    len_c = len(cells)
    len_p = len(points)
    len_cd = len(cells_data)
    len_pd = len(points_data)
    with open(path_particles, "w") as f:
        f.write("# vtk DataFile Version 2.0\n")
        f.write("Created by Gmsh 4.14.0\n")
        f.write("ASCII\n")
        f.write("DATASET UNSTRUCTURED_GRID\n")

        f.write(f"POINTS {len(points)} float\n")
        for x, y, z in points:
            f.write(f"{x} {y} {z}\n")
        f.write("\n")

        if len_c != 0:
            num_verteces = len(cells[0])
            f.write(f"CELLS {len_c} {len_c * (num_verteces + 1)}\n")
            for cell in cells:
                f.write(f"{num_verteces} {cell[0]} {cell[1]} {cell[2]}\n")
            f.write("\n")
            f.write(f"CELL_TYPES {len_c}\n")
            for _ in range(len_c):
                f.write("5\n")

        if len_cd != 0:
            for name_cd in cells_data.keys():
                if len(cells_data[name_cd]['data']) != len_c:
                    raise ValueError(f"Длина массива параметров ячеек {len(cells_data[name_cd]['data'])} /= числу ячеек {len_c}")
                f.write("\n")
                f.write(f"CELL_DATA {len_c}\n")
                if cells_data[name_cd]['type'] == 'SCALARS':
                    f.write(f"SCALARS {name_cd} float\n")
                    f.write("LOOKUP_TABLE default\n")
                    for data in cells_data[name_cd]['data']:
                        f.write(f"{data}\n")
                else:
                    f.write(f"VECTORS {name_cd} float\n")
                    for data in cells_data[name_cd]['data']:
                        f.write(f"{data[0]} {data[1]} {data[2]}\n")

        if len_pd != 0:
            for name_pd in points_data.keys():
                if len(points_data[name_pd]['data']) != len_p:
                    raise ValueError(f"Длина массива параметров ячеек {len(points_data[name_pd]['data'])} /= числу ячеек {len_p}")
                f.write("\n")
                f.write(f"POINTS_DATA {len_p}\n")
                if points_data[name_pd]['type'] == 'SCALARS':
                    f.write(f"SCALARS {name_pd} float\n")
                    f.write("LOOKUP_TABLE default\n")
                    for data in points_data[name_pd]['data']:
                        f.write(f"{data}\n")
                else:
                    f.write(f"VECTORS {name_pd} float\n")
                    for data in points_data[name_pd]['data']:
                        f.write(f"{data[0]} {data[1]} {data[2]}\n")
