def read_config(config_path):
    params = {}
    int_params = ["Figure_type", "Numder_of_particles"]
    float_params = ["Radius"]
    vector_params = ["Orientation_angle", "Source"]
    with open(config_path, "r") as file:
        data = file.readlines()
        for line in data:
            if line == '\n' or line[0] == "#":
                continue
            try:
                key, value = line[:-1].split(" = ")
            except ValueError:
                print("Ошибка во входном файле")
                return

            if key in int_params:
                try:
                    value = int(value)
                    params[key] = value
                except ValueError:
                    print(f"Значение {key} должно быть целым числом")
                    return
            elif key in float_params:
                try:
                    value = float(value)
                    params[key] = value
                except ValueError:
                    print(f"Значение {key} должно быть числом")
                    return
            elif key in vector_params:
                if value[0] == "[" and value[-1] == "]":
                    try:
                        value = list(map(int, value[1:-1].split(",")))
                        params[key] = value
                    except ValueError:
                        print(f"В {key} должны быть перечислены координаты через ',', координаты должны быть числами")
                        return
                else:
                    print("Координаты вектора должны быть в []")
                    return
            else:
                params[key] = value
    return params
