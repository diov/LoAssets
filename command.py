import logging
import os

from assets import filter_data_files, dump_assets, swipe_localization, filter_localization_files, \
    filter_localization_table_files, patch_content, is_localization_table_file, patch_data_content, is_localization_file
from constants import default_output_dir, support_regions, support_languages, default_input_dir, \
    default_patch_dir
from serialization import serialize_bin, deserialize_bin, validate_bin, validate_json, validate_csv


class Command:
    def __init__(self, region=None):
        self.region = region or "ja"
        if self.region not in support_regions:
            logging.error("Unsupported region")
            return

    @staticmethod
    def dump():
        files = filter_data_files(default_input_dir)
        dump_assets(files, default_input_dir, default_output_dir)

    @staticmethod
    def serialize(input: str):
        is_validate = validate_bin(input)
        if not is_validate:
            logging.error("Invalid bin file")
        else:
            serialize_bin(input, default_output_dir)

    @staticmethod
    def deserialize(input: str):
        is_validate = validate_json(input)
        if not is_validate:
            logging.error("Invalid json file")
        else:
            deserialize_bin(input, default_output_dir)

    def clone(self, target: str):
        if target not in support_languages:
            logging.error("Unsupported language")
            return
        elif target == self.region:
            logging.error("Should not clone to the same language")
            return

        files = filter_data_files(default_input_dir)
        file = filter_localization_files(files)
        if not file:
            logging.error("No localization directory found")
            return
        swipe_localization(file, self.region, target, default_output_dir)
        pass

    @staticmethod
    def patch():
        input_files = filter_data_files(default_input_dir)
        for root, _, files in os.walk(default_patch_dir):
            for file_name in files:
                patch_file = os.path.join(root, file_name)
                if validate_bin(patch_file):
                    # Patch validated binary file
                    input_file = filter_localization_table_files(input_files)
                    if input_file:
                        patch_content(input_file, patch_file)
                elif validate_csv(patch_file):
                    # Patch validated csv file
                    input_file = filter_localization_files(input_files)
                    if input_file:
                        patch_content(input_file, patch_file)
                elif is_localization_table_file(patch_file):
                    # Patch mod localization table __data file
                    input_file = filter_localization_table_files(input_files)
                    if input_file:
                        patch_data_content(input_file, patch_file)
                elif is_localization_file(patch_file):
                    # Patch mod localization __data file
                    input_file = filter_localization_files(input_files)
                    if input_file:
                        patch_data_content(input_file, patch_file)
