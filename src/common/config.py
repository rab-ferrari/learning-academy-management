# -*- coding: utf-8 -*-
"""Configuration File Handler

Declares global configuration parameters, initializes an info dictionary
containing all relevant configuration dependent information and implements
methods to access this information.
"""
import os
import configparser
import common.params


class Config:
  """Config Class

  Parses the main configuration file and implements methods to access this information.

  Attributes:
    env (str): Environment for current execution
    global_info (dict): Dictionary containing all configuration information
    info (dict): Dictionary containing configuration information for current environment
    secrets (dict): 
  """

  def __init__(self):
    """Config Class Constructor

    Initializes the info dictionaries by parsing the _PATH_CONFIG file defined in the
    parameters module.
    """
    parser = configparser.ConfigParser()
    parser.sections()
    parser.read(common.params._PATH_CONFIG)
    self.env          = None
    self.global_info  = {}
    self.info         = {}
    self.secrets      = {}

    # split the config items into dict fields
    for env in parser._sections:
      self.global_info[env] = {self.split(item)[0]:{} for item in parser._sections[env]}
      for item in parser._sections[env]:
        item_data = self.split(item)
        self.global_info[env][item_data[0]][item_data[1]] = parser._sections[env][item]

    parser = configparser.ConfigParser()
    parser.sections()
    parser.read(common.params._PATH_SECRETS)
    for env in parser._sections:
      self.secrets[env] = {}
      self.secrets[env] = {
        item: parser._sections[env][item]
        for item in parser._sections[env]
      }

  def split(self, item):
    """Split Config Item

    Splits the config item based on the predefined separator ".".

    Args:
      item (str): String to be splitted

    Returns:
      (:obj:`list` of :obj:`str`): Splitted values
    """
    return item.split(".")

  def limit_env_options(self, env_list):
    """Filter Environment Options

    Limits the environment information selection based on the env_list argument.

    Args:
      (:obj:`list` of :obj:`str`): List of allowed environment options
    """
    self.global_info = {env:self.global_info[env] for env in env_list}

  def get_env_options(self):
    """Environment Options

    Generates and returns list of available environment options.

    Returns:
      (:obj:`list` of :obj:`str`): Environment options - eg. "dev", "uat", "prod"
    """
    return list(self.global_info.keys())

  def set_environment(self, env):
    """Set Environment

    Sets the current execution environment and initializes the info attribute.

    Args:
      env (str): Environment option
    """
    self.env      = env
    self.info     = self.global_info[env]
    self.secrets  = self.secrets[env]

  def get_secret(self, secret):
    """Get Secret

    Retrieves a secret of a given service.

    Args:
      secret (str): Secret name

    Returns:
      (str): Secret value
    """
    return self.secrets[secret]

  def get_email(self, mail):
    """Get Email Address

    Args:
      secret (str): Email name/position

    Returns:
      (str): Email value
    """
    return self.info["mail"][mail]
