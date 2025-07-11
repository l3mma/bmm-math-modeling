def marker_cell(nodes, cells, cell_param, path_save):
    with open(path_save + "\\output_colored.vtk", "w") as f:
        f.write("# vtk DataFile Version 2.0\n")
        f.write("Colored Mesh with Intersections\n")
        f.write("ASCII\n")
        f.write("DATASET UNSTRUCTURED_GRID\n\n")
        f.write(f"POINTS {len(nodes)} float\n")

        for x, y, z in nodes:
            f.write(f"{x} {y} {z}\n")
        f.write("\n")
        f.write(f"CELLS {len(cells)} {len(cells) * 4}\n")
        for cell in cells:
            f.write(f"3 {cell[0]} {cell[1]} {cell[2]}\n")
        f.write("\n")

        # triangle type 5
        f.write(f"CELL_TYPES {len(cells)}\n")
        for _ in cells:
            f.write("5\n")
        f.write("\n")

        # color cells
        f.write(f"CELL_DATA {len(cells)}\n")
        f.write("SCALARS cell_color float 1\n")  # RGB
        f.write("LOOKUP_TABLE custom_colors\n")
        # for param in cell_param:
        #     if param > 0:
        #         f.write("2\n")
        #     else:
        #         f.write("0\n")
        for param in cell_param:
            if param > 0:
                f.write(f"{param}\n")
            else:
                f.write("0\n")
        f.write("\n")