def extract_section(lines, section_name):
    start_index = -1
    for i, line in enumerate(lines):
        if line.strip().upper().startswith(section_name):
            start_index = i
            break
    if start_index == -1:
        return None, [], len(lines)

    header_line = lines[start_index]
    section_data = []
    for i in range(start_index + 1, len(lines)):
        if lines[i].strip().upper().startswith(("POINTS", "CELLS", "CELL_TYPES", "CELL_DATA", "POINT_DATA")):
            return header_line, section_data, i
        section_data.append(lines[i])
    return header_line, section_data, len(lines)


def merge_sections(section_name, header1, data1, header2, data2):
    if header1 and header2:
        if section_name == "POINTS":
            point_count1 = int(header1.strip().split()[1])
            point_count2 = int(header2.strip().split()[1])
            data_type = header1.strip().split()[2]
            return [f"POINTS {point_count1 + point_count2} {data_type}\n"], data1 + data2, point_count1, point_count2

        elif section_name == "CELLS":
            cell_count1, index_count1 = map(int, header1.strip().split()[1:3])
            cell_count2, index_count2 = map(int, header2.strip().split()[1:3])
            return [f"CELLS {cell_count1 + cell_count2} {index_count1 + index_count2}\n"], data1 + data2, None, None

        elif section_name == "CELL_TYPES":
            type_count1 = int(header1.strip().split()[1])
            type_count2 = int(header2.strip().split()[1])
            return [f"CELL_TYPES {type_count1 + type_count2}\n"], data1 + data2, None, None

    elif header1:
        return [header1], data1, int(header1.strip().split()[1]) if section_name == "POINTS" else None, 0

    elif header2:
        return [header2], data2, 0, int(header2.strip().split()[1]) if section_name == "POINTS" else None

    return [], [], 0, 0


def merge_vtk_files(file1_path, file2_path, output_path):
    with open(file1_path, 'r') as file1:
        lines1 = file1.readlines()
    with open(file2_path, 'r') as file2:
        lines2 = file2.readlines()

    merged_output = []

    index = 0
    while index < len(lines1):
        line = lines1[index]
        if line.strip().upper().startswith(("POINTS", "CELLS", "CELL_TYPES", "CELL_DATA", "POINT_DATA")):
            break
        merged_output.append(line)
        index += 1

    section_names = ["POINTS", "CELLS", "CELL_TYPES"]

    current_index1 = 0
    current_index2 = 0

    total_point_count = 0
    point_count1 = 0
    point_count2 = 0

    for section_name in section_names:
        header1, data1, next_index1 = extract_section(lines1[current_index1:], section_name)
        header2, data2, next_index2 = extract_section(lines2[current_index2:], section_name)

        merged_header, merged_data, count1, count2 = merge_sections(section_name, header1, data1, header2, data2)
        merged_output.extend(merged_header)
        merged_output.extend(merged_data)

        if section_name == "POINTS":
            point_count1 = count1 or 0
            point_count2 = count2 or 0
            total_point_count = point_count1 + point_count2

        current_index1 += next_index1
        current_index2 += next_index2

    cell_data_header1, cell_data_body1, _ = extract_section(lines1, "CELL_DATA")
    cell_data_header2, cell_data_body2, _ = extract_section(lines2, "CELL_DATA")

    if cell_data_header1 or cell_data_header2:
        cell_data_count1 = int(cell_data_header1.strip().split()[1]) if cell_data_header1 else 0
        cell_data_count2 = int(cell_data_header2.strip().split()[1]) if cell_data_header2 else 0
        total_cell_data_count = cell_data_count1 + cell_data_count2

        merged_output.append(f"CELL_DATA {total_cell_data_count}\n")
        merged_output.extend(cell_data_body1)
        merged_output.extend(cell_data_body2)

    if total_point_count > 0:
        merged_output.append(f"POINT_DATA {total_point_count}\n")
        merged_output.append("VECTORS RAD float\n")

        merged_output.extend(["0.0 0.0 0.0\n"] * point_count1)

        merged_output.extend(["0.1 0.0 0.0\n"] * point_count2)

    with open(output_path, 'w') as output_file:
        output_file.writelines(merged_output)

merge_vtk_files("output_colored.vtk", "vtk_gen.vtk", "united.vtk")
