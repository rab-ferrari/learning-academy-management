# -*- coding: utf-8 -*-
"""Module Import

Name: UpdateEmailEvents

The `CreateEmailEvent` module checks already checks and updates an event if
its already created.

To update all events, we simply call that module for each event in the database:
the "event is already created" section will always be executed in this case as
the expected behavior.
"""
from auto.module import (
  CreateEmailEvent
)

def perform(flow, config, database, logger, **kwargs):

  # store original event parameter
  original_event = database.get_event_input()

  for event_name in database.data["events"]:

    database.set_event_input(event_name)
    CreateEmailEvent.perform(flow, config, database, logger, **kwargs)

  # save back the original input
  database.set_event_input(original_event)
