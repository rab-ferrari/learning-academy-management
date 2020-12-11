# -*- coding: utf-8 -*-
"""Module Import

Name: CreateEmailEvent

TODO: describe
  - retrieve participants

    - create Event
    - create Atendees --> link to event
    - send invite (?)

  # - compile (meeting) email --> calendar event + add attendees + send invite
  # - send

https://github.com/O365/python-o365/blob/master/O365/message.py
https://github.com/O365/python-o365/blob/master/O365/calendar.py
"""
from datetime import (
  datetime,
  timedelta
)
from O365 import Account
from O365.calendar import (
  Attendees
)
from common.msgraph import (
  initialize_account
)
from common.templates import (
  _EMAIL
)



def perform(flow, config, database, logger, **kwargs):

  # retrieve event
  event_name   = database.get_event_input()

  # retrieve participants (plus teachers)
  participants = database.get_participants(event_name) + database.get_teachers(event_name)

  # initialize account
  account = initialize_account(config, logger)

  events = []

  # loop over meetings required for the course
  for meeting in database.data["events"][event_name]["meetings"]:

    # create timezone datetime
    event_datetime = database.get_meeting_datetime(meeting)
    event_datetime = config.get_timezone("default").localize(event_datetime)
    event_endtime  = event_datetime + timedelta(hours=int(config.get_event_info("class_duration_hours")))

    # calendar instance
    schedule  = account.schedule()
    calendar  = schedule.get_default_calendar()

    # event already exists and we just have to retrieve it from our calendar
    if meeting["email_scheduled"] is True:
      logger.info(f"Meeting for event {event_name} at {datetime} already scheduled!")
      logger.info(f"Skipping...")
      logger.info(f"Will update existing event...")

      # look for meeting that satisfies class name and start/end time
      query = calendar.new_query()
      query = query.on_attribute("subject").equals(event_name)
      query = query.chain("and").on_attribute("start").equals(event_datetime)
      query = query.chain("and").on_attribute("end").equals(event_endtime)

      # retrieve first (and hopefully only) event found
      for item in calendar.get_events(query=query):
        event = item
        break

    # new event must be created
    else:
      event = calendar.new_event()
      event.subject   = event_name
      event.location  = "TBD"
      event.body = _EMAIL["meeting_request"]["body"].format(
        event_name,
        meeting["datetime"],
        config.get_email("adm_name")
      )
      event.start  = event_datetime
      event.end    = event_endtime
      event.remind_before_minutes = config.get_event_info("class_reminder_minutes")

    # add event participants - for old/new events in case there are new participants
    event.attendees.add(participants)

    # remove event participants if they aren't on the list anymore
    registered_participants = (
      database.get_participant_emails(event_name) +
      database.get_teacher_emails(event_name)
    )
    for participant in event.attendees:
      if participant.address not in registered_participants:
        event.attendees.remove(participant)

    # save event
    event.save()
    logger.info(f"Updated event {event_name}.")

    # set scheduled flag
    meeting["email_scheduled"] = True

    # append event objects to module output - so it can be used by other modules
    events.append(event)

  return events
