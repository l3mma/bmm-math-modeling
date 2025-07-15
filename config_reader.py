def _crop_data(data: str):
    if not("{" in data and "}" in data):
        return []
    data = data[data.find("{") + 1:data.find("}")]
    data = data.replace(" ", "")
    data = data.split(";")
    answer = []
    for elem in data:
        if elem != "":
            answer.append(elem)
    return answer


def _convert_to_dict_data(data: list, dtypes_funcs: dict, num_required_params=0, params=[]):
    answer = {}
    if len(data) < num_required_params:
        return f"Колисчесво данных не должно быть меньше числа обязательных параметров ({num_required_params} для этого объекта) "

    if len(params) == 0:
        params = list(dtypes_funcs.keys())

    if len(data) > len(params):
        return "Количесво данных не должно превышать число параметров"

    for i in range(len(data)):
        if params[i] not in dtypes_funcs:
            return f"Для этого объекта не существует параметра {params[i]}"
        try:
            answer[params[i]] = dtypes_funcs[params[i]](data[i])
        except ValueError:
            return f"Неправильный тип данных для параметра {params[i]}"
    return answer

def _to_models_data(data: str, dtypes_funcs: dict):
    data = _crop_data(data)
    return _convert_to_dict_data(data, dtypes_funcs)

def _to_clouds_data(data: str, dtypes_funcs: dict):
    data = _crop_data(data)
    sphere_params = ["figure_type", "numder_of_particles", \
                        "distribution_type", "distribution_params", "source", "radius"]
    cone_params = ["figure_type", "numder_of_particles",  \
                        "distribution_type", "distribution_params", "source", "radius", "height", "orientation_angle"]
    if len(data) == 0:
        return "Нет данных"

    match _to_str(data[0]):
        case "sphere":
            return _convert_to_dict_data(data, dtypes_funcs, 2, sphere_params)
        case "cone":
            return _convert_to_dict_data(data, dtypes_funcs, 2, cone_params)
        case _:
            return f"Отсутсвует тип фигуры {data[0]}"


def _str_to_vector(data):
    if not("[" in data and "]" in data):
        raise ValueError("Вектор должен быть записан в []")
    data = data[data.find("[") + 1:data.find("]")]
    data = data.replace(" ", "")

    if len(data) == 0:
        return []

    try:
        data = list(map(float, data.split(",")))
    except ValueError:
        raise ValueError("Компоненты вектора должны быть числами")
    return data

def _to_str(data):
    if data.count('"') == 2:
        return data[data.find('"') + 1: data.rfind('"')]
    elif data.count("'") == 2:
        return data[data.find("'") + 1: data.rfind("'")]
    # elif data.count('"') == 1 or data.count("'") == 1:
    #     raise ValueError("Строка должна быть записана в одинаковых кавычках или без них")
    else:
        return data


def read_config(config_path):
    data = []
    try:
        with open(config_path, "r") as file:
            data = file.readlines()
    except FileNotFoundError:
        return "Неверный путь к файлу"

    models = []
    clouds = []
    _models_dtypes_funcs = {"path": _to_str}
    _clouds_dtypes_funcs = {"figure_type": _to_str, "numder_of_particles": int, \
                          "distribution_type": _to_str, "distribution_params": _str_to_vector, "source": _str_to_vector,\
                            "radius": float, "height": float, "orientation_angle": _str_to_vector }
    reading_flag = False
    current_reading = ""


    for line in data:
        # check if blank line or comment
        if line == '\n' or line[0] == "#":
            continue

        # start or finish reading one objects data
        if "model" in line or "cloud" in line:
            reading_flag = True

        if "}" in line:
            current_reading += line[:-1]

            match current_reading[:current_reading.find("{")]:
                case "model":
                    models.append(_to_models_data(current_reading, _models_dtypes_funcs))
                case "cloud":
                    clouds.append(_to_clouds_data(current_reading, _clouds_dtypes_funcs))
                case _:
                    return "Некорректный ввод"

            reading_flag = False
            current_reading = ""

        if reading_flag:
            current_reading += line[:-1]

    if reading_flag:
        return "Некорректный ввод: отсутсвует }"
    return models, clouds

def check_reading(data):

    checkable_params = {"distribution_type": ["uniform", "gaussian"]}

    for block in data:
        for elem in block:
            if str(type(elem)) == "<class 'str'>":
                return False

            for param in checkable_params.keys():
                if param in elem.keys() and elem[param] not in checkable_params[param]:
                    return False
    return True

if __name__ == "__main__":
    print(read_config("config.txt"))
    print(check_reading(read_config("config.txt")))