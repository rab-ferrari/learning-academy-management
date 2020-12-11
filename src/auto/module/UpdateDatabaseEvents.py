# -*- coding: utf-8 -*-
"""Module Import

Name: UpdateDatabaseEvents

TODO:
  Note that we have multiple "classes" (email meetings) linked to a single
  "event" (course). The user confirmation is given by "event", so additional
  specification is required to determine the system behavior when, for example,
  the student accepts one "class" but declines another (and other such cases).

For each and every event:
  - Access sympla and update participant list with new participants;
  - Look for updated replies and update them in the base;
"""
# from auto.module.CreateEmailEvent import (
#   perform as perform_GetEventParticipants
# )
from auto.module import (
  GetEventParticipants,
  CreateEmailEvent,
)
from common.params import (
  _RESPONSE_STATUS,
  _RESPONSE_STATUS_PENDING
)


def perform(flow, config, database, logger, **kwargs):

  # store original event parameter
  original_event = database.get_event_input()

  for event_name in database.data["events"]:

    database.set_event_input(event_name)
    GetEventParticipants.perform(flow, config, database, logger, **kwargs)

    classes = CreateEmailEvent.perform(flow, config, database, logger, **kwargs)

    # loop over the event (course) events (classes)
    for meeting in classes:
      for attendee in meeting.attendees:
        if attendee.response_status is not None:
          if attendee.response_status.status is not None:
            database.set_participant_status(
              event_name,
              attendee.address,
              _RESPONSE_STATUS[attendee.response_status.status]
            )
