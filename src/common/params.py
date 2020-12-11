# -*- coding: utf-8 -*-
"""Global Parameters

Declares global parameters that are referenced by several different modules.
"""
import os
from O365.calendar import (
  EventResponse
)

# global aliases
_VERSION          = "0.1 - hackaton poc"
_JOB_NAME         = "AUTO LA MANAGEMENT"

# log paths
_LOG_PATH         = None
_LOG_PATH_MODULES = None
_LOG_PATH_ERROR   = None
_LOG_GLOBAL       = None
_LOG_MAIN         = None

# assets paths
_PATH_ASSETS      = None
_PATH_STAGING     = None
_PATH_ARTS        = None
_PATH_CONFIG      = None
_PATH_MODULES     = None
_PATH_FLOWS       = None
_PATH_SECRETS     = None
_PATH_PARAMS      = None
_PATH_PERSISTENT  = None
_PATH_DATABASE    = None

# module execution messages
_MODULE_MESSAGE_START     = "\tModule started  : {}"
_MODULE_MESSAGE_SUCCESS   = "\tModule finished : {} successful!"
_MODULE_MESSAGE_ERROR     = "\tModule finished : {} with errors!"
_FLOW_TRANSITION_MESSAGE  = "\tFlow transition : {}.{} done!"
_FLOW_MESSAGE_START       = "Flow started  : {}"
_FLOW_MESSAGE_SUCCESS     = "Flow finished : {} successful!"
_FLOW_MESSAGE_ERROR       = "Flow finished : {} with errors!"

# confirmation status
_RESPONSE_STATUS_DECLINED  = "declined"
_RESPONSE_STATUS_PENDING   = "pending"
_RESPONSE_STATUS_TENTATIVE = "tentative"
_RESPONSE_STATUS_CONFIRMED = "confirmed"
_RESPONSE_STATUS = {
  EventResponse.Declined            : _RESPONSE_STATUS_DECLINED,
  EventResponse.NotResponded        : _RESPONSE_STATUS_PENDING,
  EventResponse.TentativelyAccepted : _RESPONSE_STATUS_TENTATIVE,
  EventResponse.Accepted            : _RESPONSE_STATUS_CONFIRMED,
  EventResponse.Organizer           : _RESPONSE_STATUS_CONFIRMED
}


def initialize(main_file, secrets_file=None):
  """Parameter Initialization

  Initializes path parameters that depend on the main file location so they
  are correctly imported.
  """
  current_path = os.path.dirname(main_file)

  global _LOG_PATH, _LOG_PATH_MODULES, _LOG_PATH_ERROR, _LOG_GLOBAL, _LOG_MAIN
  _LOG_PATH         = os.path.join(current_path, "logs")
  _LOG_PATH_MODULES = os.path.join(_LOG_PATH, "modules"     )
  _LOG_PATH_ERROR   = os.path.join(_LOG_PATH, "error"       )
  _LOG_GLOBAL       = os.path.join(_LOG_PATH, "global.log"  )
  _LOG_MAIN         = os.path.join(_LOG_PATH, "main.log"    )

  global _PATH_ASSETS, _PATH_CONFIG, _PATH_MODULES, _PATH_FLOWS, _PATH_SECRETS
  global _PATH_PARAMS, _PATH_DATABASE, _PATH_ARTS, _PATH_STAGING, _PATH_PERSISTENT
  _PATH_PERSISTENT  = os.path.join(current_path, "persistent"   )
  _PATH_ASSETS      = os.path.join(current_path, "assets"       )
  _PATH_STAGING     = os.path.join(current_path, "staging"      )
  _PATH_ARTS        = os.path.join(_PATH_PERSISTENT, "arts"         )
  _PATH_CONFIG      = os.path.join(_PATH_PERSISTENT, "config.ini"   )
  _PATH_DATABASE    = os.path.join(_PATH_PERSISTENT, "database.json")
  _PATH_MODULES     = os.path.join(_PATH_ASSETS, "modules.json" )
  _PATH_FLOWS       = os.path.join(_PATH_ASSETS, "flows.json"   )
  _PATH_PARAMS      = os.path.join(_PATH_STAGING, "input.json"  )

  if secrets_file is None:
    secrets_file = os.path.join(_PATH_PERSISTENT, "secrets.ini")
  _PATH_SECRETS     = secrets_file
