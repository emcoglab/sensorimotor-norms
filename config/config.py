"""
===========================
Handles and provides access to config files.
===========================

Dr. Cai Wingfield
---------------------------
Embodied Cognition Lab
Department of Psychology
University of Lancaster
c.wingfield@lancaster.ac.uk
caiwingfield.net
---------------------------
2019
---------------------------
"""

from copy import deepcopy
from os import path
from typing import Dict

import yaml

from .singleton import UnsettableSingleton


class Config(metaclass=UnsettableSingleton):
    """
    Config class.
    It's a singleton, so whatever state it's in when it's called the first time, that's how it'll remain.
    """

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        Config._unset()

    def __init__(self, use_config_overrides_from_file: str = None, use_particular_overrides: Dict = None):
        default_config_file_location = path.join(path.dirname(path.realpath(__file__)), 'default_config.yaml')

        if use_particular_overrides is not None:
            print(f"Loading config file from {default_config_file_location} "
                  f"with specific overrides set")
            self.overridden = True
        elif use_config_overrides_from_file is not None:
            print(f"Loading config file from {default_config_file_location} "
                  f"with overrides from {use_config_overrides_from_file}")
            self.overridden = True
        else:
            print(f"Loading config file from {default_config_file_location} "
                  f"with no override.")
            self.overridden = False

        # Load files
        self._config_default: Dict
        self._config_override: Dict
        with open(default_config_file_location, mode="r", encoding="utf-8") as default_config_file:
            self._config_default = yaml.load(default_config_file, yaml.SafeLoader)
        if use_config_overrides_from_file is not None:
            with open(use_config_overrides_from_file, mode="r", encoding="utf-8") as override_config_file:
                self._config_override = yaml.load(override_config_file, yaml.SafeLoader)
        else:
            self._config_override = None

        # Apply particular overrides
        if use_particular_overrides is not None:
            self._specific_overrides: Dict = use_particular_overrides
        else:
            self._specific_overrides: Dict = dict()

    @staticmethod
    def _get_value(config_dict: Dict, *args):
        """
        Get the overridden value, if it exists.

        :param config_dict: the config dict
        :param args: sequence of keys
        :return:
        :raises: ConfigKeyNotSetError if the value wasn't present in the override
        """
        if config_dict is None:
            raise ConfigKeyNotSetError()
        try:
            drill_dict = deepcopy(config_dict)
            for key in args:
                drill_dict = drill_dict[key]
            return drill_dict
        except KeyError:
            raise ConfigKeyNotSetError()

    def value_by_key_path(self, *args):
        try:
            return Config._get_value(self._specific_overrides, *args)
        except ConfigKeyNotSetError:
            pass
        try:
            return Config._get_value(self._config_override, *args)
        except ConfigKeyNotSetError:
            pass
        return Config._get_value(self._config_default, *args)


class ConfigKeyNotSetError(KeyError):
    """Raised when a key is not properly set in the config file."""
    pass
