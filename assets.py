import csv
import os
from io import StringIO

import UnityPy
from UnityPy.enums import ClassIDType

from constants import localization_dir, table_dir_prefix, default_input_dir, default_output_dir


def filter_data_files(data_path: str):
    data_files = []
    if os.path.isdir(data_path):
        for root, _, files in os.walk(data_path):
            for file_name in files:
                if file_name == "__data":
                    path = os.path.join(root, file_name)
                    data_files.append(path)
    else:
        data_files.append(data_path)
    return data_files


def is_localization_file(path: str):
    return localization_dir in path.split("/")


def filter_localization_files(files: [str]):
    file = next(filter(is_localization_file, files), None)
    return file


def is_localization_table_file(path: str):
    paths = path.split("/")
    for p in paths:
        if p.startswith(table_dir_prefix):
            return True
    return False


def filter_localization_table_files(files: [str]):
    file = next(filter(is_localization_table_file, files), None)
    return file


def dump_assets(files: [str], input_path, output_path: str):
    for file in files:
        env = UnityPy.load(file)

        output_dir = os.path.dirname(file).replace(input_path, output_path)
        # iterate over internal objects
        for obj in env.objects:
            if obj.type == ClassIDType.TextAsset:
                data = obj.read()

                path = os.path.join(output_dir, data.name)
                # save file
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "wb") as f:
                    f.write(data.script)


def swipe_localization(file: str, src, target: str, output_path: str):
    output_path = os.path.join(output_path, localization_dir, file.split(f"{localization_dir}/")[1])

    env = UnityPy.load(file)
    for obj in env.objects:
        if obj.type == ClassIDType.TextAsset:
            data = obj.read()
            new_csv = __swipe_csv_column(src, target, data.text)
            data.text = new_csv
            data.save()

            # save file
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(env.file.save())


def __swipe_csv_column(src: str, des: str, content: str):
    buffer = StringIO()
    writer = csv.writer(buffer, delimiter='\t')

    data = csv.reader(content.splitlines(), delimiter='\t')
    headers = next(data)
    src_index = headers.index(src)
    dst_index = headers.index(des)

    writer.writerow(headers)
    for i, row in enumerate(data):
        if row[dst_index]:
            row[src_index], row[dst_index] = row[dst_index], row[src_index]

        writer.writerow(row)

    return buffer.getvalue()


def patch_data_content(src_path, patch_path: str):
    dst_script = None
    dst_env = UnityPy.load(patch_path)
    for obj in dst_env.objects:
        if obj.type == ClassIDType.TextAsset:
            dst_data = obj.read()
            dst_script = dst_data.script

    if not dst_script:
        raise Exception("dst script not found")

    src_env = UnityPy.load(src_path)
    for obj in src_env.objects:
        if obj.type == ClassIDType.TextAsset:
            src_data = obj.read()
            src_data.script = dst_script
            src_data.save()

    # save file
    output_path = src_path.replace(default_input_dir, default_output_dir)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(src_env.file.save())


def patch_content(src_path, patch_path: str):
    with open(patch_path, "rb") as f:
        content = f.read()

    env = UnityPy.load(src_path)
    for obj in env.objects:
        if obj.type == ClassIDType.TextAsset:
            src_data = obj.read()
            src_data.script = content
            src_data.save()

    # save file
    output_path = src_path.replace(default_input_dir, default_output_dir)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(env.file.save())
