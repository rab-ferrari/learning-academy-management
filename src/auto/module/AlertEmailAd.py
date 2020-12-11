# -*- coding: utf-8 -*-
"""Module Import

Name: GetEmailCommunications

Retrieves the total event status for all registered events
that haven't occurred yet.
"""
from datetime import (
  datetime
)
from auto.module.generic import (
  email_report
)


def perform(flow, config, database, logger, **kwargs):

  # retrieve list of valid events
  valid_events = [
    event
    for event in database.data["events"]
    if int(config.get_alert_info("default_days")) == database.get_start_delay(event)
  ]

  # skip email trigger if there are no events to be advertised
  if not valid_events:
    database.params["trigger_email"] = False
    return

  # call generic email compilation module
  email_report.perform(flow, config, database, logger, "advertising", valid_events)

  # adjust recipient to communications team
  database.params["recipient"] = config.get_email("communications")
