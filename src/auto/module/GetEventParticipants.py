# -*- coding: utf-8 -*-
"""Module Import

Name: GetEventParticipants

Retrieves the correct Sympla event identifier from the event name and
with it retrieves, compiles and stores the list of active participants
in the database.
"""
from common.rest.sympla import (
  Sympla
)
from common.params import (
  _RESPONSE_STATUS_PENDING
)


def perform(flow, config, database, logger, **kwargs):

  # initialize sympla data handler
  sympla = Sympla(config, logger)

  # retrieve event data for desired event
  event_name = database.params["event"]
  event_data = sympla.get_event(event_name)
  event_id   = event_data["id"]

  # update database event_id
  database.data["events"][event_name]["sympla_id"]  = event_data["id"]
  database.data["events"][event_name]["sympla_url"] = event_data["url"]

  # get (relevant) event participants data
  sympla_participants = sympla.get_participants(event_data["id"])
  sympla_participants    = [{
      "first_name": participant["first_name"],
      "last_name" : participant["last_name"],
      "email"     : participant["email"],
      "status"    : _RESPONSE_STATUS_PENDING
    }
    for participant in sympla_participants
  ]

  # overwrite sympla participants back into database
  database.data["events"][event_name]["participants"] = sympla_participants
