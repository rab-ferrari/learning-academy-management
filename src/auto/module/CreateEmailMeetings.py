# -*- coding: utf-8 -*-
"""Module Import

Name: CreateEventDatabase

TODO: describe
  - retrieve participants
  - compile (meeting) email --> calendar event + add attendees + send invite
  - send

https://github.com/O365/python-o365/blob/master/O365/message.py
https://github.com/O365/python-o365/blob/master/O365/calendar.py
"""
from O365 import Account
from O365.message import (
  MeetingMessageType
)
from common.msgraph import (
  initialize_account
)
from common.templates import (
  _EMAIL
)



def perform(flow, config, database, logger, **kwargs):

  # TODO: retrieve participants
  participants = []

  # retrieve event
  event   = database.get_event_input()

  # initialize account
  account = initialize_account(config, logger)

  # loop over meetings required for the course
  for meeting in database.data["events"][event]["meetings"]:
    datetime = meeting["datetime"]

    if meeting["email_scheduled"] is True:
      logger.info(f"Meeting for event {event} at {datetime} already scheduled!")
      break

    # compile message
    message = account.new_message()

    message.to.add(participants)
    message.sender.address = config.get_email("adm")
    message.body = _EMAIL["meeting_request"]["body"].format(event, datetime, config.get_email("adm_name"))
    # message.meeting_message_type = MeetingMessageType.MeetingRequest
    print(message.to_api_data())

    # meeting["email_scheduled"] = True
    break
