import json

import requests


def get_all_filenames(url):
    return json.loads(requests.get(url=url).content)


def upload_file(url, filename, path):  # content_type='application/octet-stream'):
    # return requests.post(url=url, files={'file': (filename, open(path, 'rb'), content_type)})
    with open(path, 'rb') as f:
        return requests.post(url=url, files={'file': (filename, f)})


def get_file_data(url, filename):
    return bytes(requests.get(url=url, params={"filename": filename}).content)


def delete_file(url, filename):
    return requests.delete(url=url, params={"filename": filename})


def replace_file_data(url, filename, path):
    with open(path, 'rb') as f:
        return requests.put(url=url, files={'file': (filename, f)})

print(

)