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

def perform(flow, config, database, logger, **kwargs):

  # initialize sympla data handler
  sympla = Sympla(config, logger)

  # retrieve event data for desired event
  event_name = database.params["event"]
  event_data = sympla.get_event(event_name)
  event_id   = event_data["id"]

  # update database event_id
  database.data["events"][event_name]["sympla_id"] = event_id

  # get (relevant) event participants data
  participants  = sympla.get_participants(event_id)
  participants  = [{
      "first_name": participant["first_name"],
      "last_name" : participant["last_name"],
      "email"     : participant["email"]
    }
    for participant in participants
  ]

  # store participants data back into database
  database.data["events"][event_name]["participants"] = participants
