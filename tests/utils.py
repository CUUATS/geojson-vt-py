import json
import os


def load_json(file_name):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, 'fixtures', file_name)
    with open(file_path, 'r') as json_file:
        return json.load(json_file)


def json_str(obj):
    return json.dumps(integerize(obj), sort_keys=True)


def integerize(obj):
    if isinstance(obj, float):
        return int(obj)

    if isinstance(obj, dict):
        result = {}
        for (k, v) in obj.items():
            result[k] = integerize(v)
        return result

    if isinstance(obj, list):
        return [integerize(item) for item in obj]

    return obj


def closed(geometry):
    return [geometry + geometry[0:3]]
