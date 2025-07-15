def vtk_writer(path_particles, points, cells=[], cells_data=[], points_data=[], cells_data_name=[], points_data_name=[]):
    with open(path_particles, "w") as f:
        f.write("# vtk DataFile Version 2.0\n")
        f.write("Created by Gmsh 4.14.0\n")
        f.write("ASCII\n")
        f.write("DATASET UNSTRUCTURED_GRID\n")

        f.write(f"POINTS {len(points)} float\n")
        for x, y, z in points:
            f.write(f"{x} {y} {z}\n")
        f.write("\n")

        if len(cells) != 0:
            num_verteces = len(cells[0])
            f.write(f"CELLS {len(cells)} {len(cells) * (num_verteces + 1)}\n")
            for cell in cells:
                f.write(f"{num_verteces} {cell[0]} {cell[1]} {cell[2]}\n")
            f.write("\n")
            f.write(f"CELL_TYPES {len(cells)}\n")
            for _ in range(len(cells)):
                f.write("5\n")


        if len(cells_data_name) != 0:
            for num_cells_data in range(len(cells_data_name)):
                if len(cells_data[num_cells_data]) != len(cells):
                    raise ValueError(f"Длина массива параметров ячеек {len(cells_data[num_cells_data])} /= числу ячеек {len(cells)}")
                f.write("\n")
                f.write(f"CELL_DATA {len(cells)}\n")
                if len(cells_data[num_cells_data][0]) == 1:
                    f.write(f"SCALARS {cells_data_name[num_cells_data]} float\n")
                    f.write("LOOKUP_TABLE default\n")
                    for data in cells_data[num_cells_data]:
                        f.write(f"{data[0]}\n")
                else:
                    f.write(f"VECTORS {cells_data_name[num_cells_data]} float\n")
                    for data in cells_data[num_cells_data]:
                        f.write(f"{data[0]} {data[1]} {data[2]}\n")


        if len(points_data_name) != 0:
            for num_points_data in range(len(points_data_name)):
                if len(points_data[num_points_data]) != len(points):
                    raise ValueError(
                        f"Длина массива параметров точек {len(points_data[num_points_data])} != числу точек {len(points)}")
                f.write("\n")
                f.write(f"POINTS_DATA {len(points)}\n")
                if len(points_data[num_points_data][0]) == 1:
                    f.write(f"SCALARS {points_data_name[num_points_data]} float\n")
                    f.write("LOOKUP_TABLE default\n")
                    for data in points_data[num_points_data]:
                        f.write(f"{data[0]}\n")
                else:
                    f.write(f"VECTORS {points_data_name[num_points_data]} float\n")
                    for data in points_data[num_points_data]:
                        f.write(f"{data[0]} {data[1]} {data[2]}\n")
