# -*- coding: utf-8 -*-
"""Logger Creation

This module implements a custom creation of logging.Logger objects by customizing
its level, format and output (console or specific file).

Example:
  To instantiate a new logger in the code, simply make:
    logger = common.trace.create('output/directory/filename.log')
  and you're all set.
"""

import logging

_LOG_LEVEL  = logging.DEBUG


def create(local_log, console=False):
  """Logger and Handler Creation

  Creates a Logger object (custom class) with the logging level determined by
  common.args arguments. The logger object will send its information to a log
  file and to the console.

  Args:
    local_log (str): Path and filename for the local thread logger
    console (bool): If log output must be redirected to console

  Returns:
    (:obj:`logging.Logger`): Logger object (superclass logging.Logger)
  """
  if _LOG_LEVEL >= logging.INFO:
    formatter = logging.Formatter(
      "%(asctime)s [ %(levelname)s ] %(message)s",
      #"%(message)s",
      datefmt="%Y-%m-%d %H:%M:%S"
    )
  else:
    formatter = logging.Formatter(
      "%(asctime)s [ %(threadName)s, %(filename)s, %(funcName)s, %(lineno)d ]"
      "[ %(levelname)s ] %(message)s",
      datefmt="%Y-%m-%d %H:%M:%S"
    )

  logger = logging.Logger(local_log.rpartition(".")[0])
  logger.setLevel(_LOG_LEVEL)

  handlerlocal_log = logging.FileHandler(local_log)
  handlerlocal_log.setFormatter(formatter)
  logger.addHandler(handlerlocal_log)

  if console:
    handlerConsole = logging.StreamHandler()
    handlerConsole.setFormatter(formatter)
    logger.addHandler(handlerConsole)
  return logger
