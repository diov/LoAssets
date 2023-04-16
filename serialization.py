import logging
import os.path

import requests


def validate_bin(path: str):
    if os.path.isdir(path):
        return False
    elif not os.path.exists(path):
        return False
    elif not os.path.getsize(path):
        return False
    else:
        with open(path, "rb") as f:
            header = f.read(8)
            return header == b"\x00\x01\x00\x00\x00\xff\xff\xff"


def validate_json(path: str):
    if os.path.isdir(path):
        return False
    elif not os.path.exists(path):
        return False
    elif not os.path.getsize(path):
        return False
    else:
        with open(path, "rb") as f:
            return f.read(1) == b"{"


def validate_csv(path: str):
    if os.path.isdir(path):
        return False
    elif not os.path.exists(path):
        return False
    elif not os.path.getsize(path):
        return False
    else:
        with open(path, "rb") as f:
            headers = f.readline()
            return headers == "code\tko\tja\ten\tc\tsc"


def serialize_bin(file, output_path: str):
    with open(file, 'rb') as f:
        file_content = f.read()

    url = "https://binser.azurewebsites.net/api/SerBin?code=15Nt3c9v-mJKqymOryauu-mUTiW7w3inDuybikcg8eZ8AzFuDe7VVA=="
    headers = {"Content-Type": "application/octet-stream"}
    response = requests.post(url, headers=headers, data=file_content)

    basename = os.path.basename(file)
    name_without_ext = os.path.splitext(basename)[0]
    path = os.path.join(output_path, f'{name_without_ext}.json')
    with open(path, 'wb') as f:
        f.write(response.content)


def deserialize_bin(file, output_path: str):
    with open(file, 'rb') as f:
        file_content = f.read()

    url = "https://binser.azurewebsites.net/api/DeserBin?code=HqjKFtCn-SwOrgt2Uk11S_gwhdjHT7ciE53A4ikf5q-cAzFuBeiWvg=="
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, data=file_content)

    basename = os.path.basename(file)
    name_without_ext = os.path.splitext(basename)[0]
    path = os.path.join(output_path, f'{name_without_ext}.bin')
    with open(path, 'wb') as f:
        f.write(response.content)
