# -*- coding: utf-8 -*-
"""Module Import

Name: CreateDatabaseEvent

Compiles data into database format, adds some additional fields that will
be filled by other modules and stores everything in the database.

TODO:
  We are able to set an `is_online_meeting` flag in the microsoft calendar,
  so it might be useful to input and store this parameter as well.

TODO: check if name already exists ; add url to required inputs ; use url as search key
"""
import os
from common.params import (
  _PATH_ARTS
)


def perform(flow, config, database, logger, **kwargs):

  # compile meetings data
  meetings = []
  for datetime in database.params["datetimes"]:
    meetings.append({
      "datetime": datetime,
      "email_scheduled": False,
      "happened": False,
      "zoom_location": None,
      "presence_list": []
    })

  # rename and retrieve art path
  name = database.params["event"]
  art  = os.path.join(_PATH_ARTS, f"{name}.png")
  os.rename(database.art, art)

  # compile complete event data struct
  event = {
    "name"     : name,
    "description": database.params["description"],
    "sympla_id": None,
    "sympla_url": None,
    "capacity" : 5,
    "art"      : art,
    "teachers" : database.params["teachers"],
    "meetings" : meetings,
    "email_conversation_id": None,
    "participants": []
  }

  # store back event data into database
  database.data["events"][name] = event
