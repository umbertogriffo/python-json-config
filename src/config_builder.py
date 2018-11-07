import json

from src.config import Config
from src.config_node import ConfigNode


class ConfigBuilder(object):
    def __init__(self):
        self.__validation_types = {}
        self.__validation_functions = {}
        self.__transformation_functions = {}
        self.__config: Config = None

    def validate_field_type(self, field_name: str, field_type: type):
        self.__validation_types[field_name] = field_type
        return self

    def validate_field_value(self, field_name: str, validation_function):
        self.__validation_functions[field_name] = validation_function
        return self

    def transform_field_value(self, field_name: str, transformation_function):
        self.__transformation_functions[field_name] = transformation_function
        return self

    def parse_config(self, file_name: str) -> ConfigNode:
        self.__config = Config(json.load(open(file_name, "r")))
        self.__validate_types()
        self.__validate_field_values()
        self.__transform_field_values()

        return self.__config

    def __validate_types(self):
        for field_name, field_type in self.__validation_types.items():
            value = self.__config.traverse_path(field_name)
            assert isinstance(value, field_type), f'Config field "{field_name}" with value "{value}" is not of type {field_type}'

    def __validate_field_values(self):
        for field_name, validation_function in self.__validation_functions.items():
            value = self.__config.traverse_path(field_name)
            assert validation_function(value), f'Config field "{field_name}" contains invalid value "{value}"'

    def __transform_field_values(self):
        for field_name, transformation_function in self.__transformation_functions.items():
            value = self.__config.traverse_path(field_name)
            new_value = transformation_function(value)
            self.__config.update_path(field_name, new_value)
