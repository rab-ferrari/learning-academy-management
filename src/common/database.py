# -*- coding: utf-8 -*-
"""Database Data Handling

Implements persistent data handling. To simplify the initial implementation
and since large volumes of data aren't expected, the data is simply stored
on an external json file and imported/edited on each execution.
"""

import os
import json
import shutil
import common.params

class Database:
  """Database Handling

  Imports json data, stores it and implements retrieval/set methods.
  The `data` attribute will be a 'public attribute' and will be accessed
  directly through the class instance.

  The program input parameters will also be available on the params json
  file, but these are expected not to be persistent and change with every
  execution. the `params` attribute will also be public.

  Attributes:
    data_file (str): Path to data file for persistent storage
    data (dict): Dict options with available flows
  """

  def __init__(self, data_file=None, params_file=None):
    """Database Class Constructor

    Initializes the class attributes.

    Args:
      data_file (str): Path to database file if non-default
      params_file (str): Path to params if non-default
    """
    # initialize database and params file paths
    if data_file is None:
      data_file   = common.params._PATH_DATABASE
    self.data_file = data_file
    if params_file is None:
      params_file = common.params._PATH_PARAMS

    # import data
    self.data = {}
    with open(self.data_file) as json_file:
      self.data = json.load(json_file)

    # import params
    self.params = {}
    with open(params_file) as json_file:
      self.params = json.load(json_file)

    # look for any image files - if found, store on arts path
    self.art = None
    for source_file in os.listdir(common.params._PATH_STAGING):
      if source_file.endswith(".png"):
        target_file = os.path.join(common.params._PATH_ARTS, "art.png")
        shutil.move(os.path.join(common.params._PATH_STAGING, source_file), target_file)
        self.art = target_file
        break

    # TODO: debug only - hard coded art
    self.art = os.path.join(common.params._PATH_ARTS, "art.png")

  def __del__(self):
    """Database Class Destructor

    Writes back the data content to the persistent json file.
    """
    with open(self.data_file, "w") as json_file:
      json.dump(self.data, json_file, indent=2)

  def get_event_input(self):
    """Get Event Input

    Returns:
      (str): Event passed as input parameter
    """
    return self.params["event"]
