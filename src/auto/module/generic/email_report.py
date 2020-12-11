# -*- coding: utf-8 -*-
"""Generic Module - Email Report Compilation

Takes two additional arguments to determine the report type
and a list of valid events that must be retained per report.
"""
from datetime import (
  datetime
)
from common.templates import (
  _EMAIL,
  _EMAIL_DEFAULT_EMPTY_BODY,
)


def perform(flow, config, database, logger, report_type, valid_events, **kwargs):

  # turn on the email trigger by default
  database.params["trigger_email"] = True

  # compile the partial message bodies for all events in the database
  event_partial_bodies = {}
  for event in database.data["events"]:
    body = _EMAIL[report_type]["body"](**database.get_status_report_params(event))
    event_partial_bodies[event] = body

  head = _EMAIL[report_type]["head"]
  tail = _EMAIL[report_type]["tail"]

  # compile a default empty body if there were no valid events
  if not valid_events:
    database.params["trigger_email"] = False
    body = _EMAIL_DEFAULT_EMPTY_BODY

  # otherwise compile the email body normally
  else:
    database.params["trigger_email"] = True
    body = "".join([
      event_partial_bodies[event]
      for event in event_partial_bodies
      if event in valid_events
    ])

  # merge the whole message
  email_message = (head + body + tail)

  # check if email trigger must be forced
  if _EMAIL[report_type]["force_trigger"] is True:
    database.params["trigger_email"] = True

  # check if the art must be attached
  database.params["attachments"] = []
  if _EMAIL[report_type]["attach_art"] is True:
    database.params["attachments"] = [
      database.data["events"][event]["art"]
      for event in valid_events
    ]

  # update the parameters to communicate with other modules
  database.params["event_report_bodies"] = event_partial_bodies
  database.params["email_message"]       = email_message
  database.params["email_subject"]       = _EMAIL[report_type]["subject"]
  database.params["email_attachment"]    = None
