def parse_config(file_path):
    config = {
        "models": [],
        "clouds": [],
        "project_directory": []
    }
    default = {
        "distribution_type": 'uniform',
        "source": [0, 0, 0],
        "radius": 1,
        "sigma_r": 0.5,
    }
    default_cone = {
        "sigma_z": 0.5,
        "height": 1,
        "orientation_angle": [0, 0, 0]
    }
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = [line.strip() for line in file if line.strip()]
        i = 0
        while i < len(lines):
            line = lines[i]
            if line.startswith("project_directory{"):
                project_directory_data = {}
                i += 1
                while i < len(lines) and not lines[i].startswith("}"):
                    current_line = lines[i].rstrip(';')
                    if current_line:
                        if "path" not in project_directory_data:
                            project_directory_data["path"] = current_line
                    i += 1
                if 'path' not in project_directory_data:
                    raise ValueError('Пути до директории не существует')
                config["project_directory"].append(project_directory_data)

            if line.startswith("model{"):
                model_data = {}
                i += 1
                while i < len(lines) and not lines[i].startswith("}"):
                    current_line = lines[i].rstrip(';')
                    if current_line:
                        if "path" not in model_data:
                            model_data["path"] = current_line
                    i += 1
                if 'path' not in model_data:
                    raise ValueError('No exist path to model')
                config["models"].append(model_data)

            elif line.startswith("cloud{"):
                cloud_data = {}
                i += 1
                while i < len(lines) and not lines[i].startswith("}"):
                    current_line = lines[i].rstrip(';')
                    if current_line:
                        if "figure_type" not in cloud_data:
                            cloud_data["figure_type"] = current_line
                        elif "number_of_particles" not in cloud_data:
                            cloud_data["number_of_particles"] = int(current_line)
                        elif "distribution_type" not in cloud_data:
                            cloud_data["distribution_type"] = current_line
                        elif "source" not in cloud_data:
                            cloud_data["source"] = eval(current_line)
                        elif "radius" not in cloud_data:
                            cloud_data["radius"] = float(current_line)
                        elif "sigma_r" not in cloud_data:
                            cloud_data["sigma_r"] = float(current_line)
                        elif "sigma_z" not in cloud_data and cloud_data["figure_type"] != "sphere":
                            cloud_data["sigma_z"] = float(current_line)
                        elif "height" not in cloud_data and cloud_data["figure_type"] != "sphere":
                            cloud_data["height"] = float(current_line)
                        elif "orientation_angle" not in cloud_data and cloud_data["figure_type"] != "sphere":
                            cloud_data["orientation_angle"] = eval(current_line)
                    i += 1

                if 'figure_type' not in cloud_data:
                    raise ValueError('Не задана форма облака частиц')
                if 'number_of_particles' not in cloud_data:
                    raise ValueError('Не задано количество частиц')

                for key, value in default.items():
                    if key not in cloud_data:
                        cloud_data[key] = value
                if cloud_data['figure_type'] == 'cone':
                    for key, value in default_cone.items():
                        if key not in cloud_data:
                            cloud_data[key] = value

                config["clouds"].append(cloud_data)
            i += 1

    return config