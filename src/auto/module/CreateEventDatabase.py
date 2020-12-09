# -*- coding: utf-8 -*-
"""Module Import

Name: CreateEventDatabase

Creates an event entry on the database. It does:
  - store the event data in the database
  - copy
"""
import os
import shutil
import common.params


def perform(flow, config, database, logger, **kwargs):

  # compile meetings data
  meetings = []
  for datetime in database.params["datetimes"]:
    meetings.append({
      "datetime": datetime,
      "happened": False,
      "zoom_location": None,
      "presence_list": []
    })

  # rename and retrieve art path
  name = database.params["event"]
  art  = os.path.join(common.params._PATH_ARTS, f"{name}.png")
  os.rename(database.art, art)

  # compile complete event data struct
  event = {
    "name"     : name,
    "art"      : art,
    "meetings" : meetings,
    "email_conversation_id": None,
    "participants": []
  }

  # store back event data into database
  database.data["events"][name] = event
