# -*- coding: utf-8 -*-
"""Miscellaneous Functions

This module lists various functions that are required by the program
but don't fit or don't require an explicit module just for them.
"""
import os
import time
import shutil

import common.params


def reset_log_dir():
  """Root Error Directory Removal

  Deletes the root logs directory if it exists and recreates it empty. Sleeps
  for 1s between the creation of each subdirectory to avoid any windows access
  level issues.

  Note:
    Some sleep calls and a duplicate `rmtree` instruction are used here to solve
    some rare bugs on the directory recreation (probably due to race conditions).
  """
  if os.path.isdir(common.params._LOG_PATH):
    shutil.rmtree(common.params._LOG_PATH, ignore_errors=True)
    shutil.rmtree(common.params._LOG_PATH, ignore_errors=True)
  time.sleep(1.0)
  os.makedirs(common.params._LOG_PATH)
  time.sleep(1.0)
  os.makedirs(common.params._LOG_PATH_MODULES)
