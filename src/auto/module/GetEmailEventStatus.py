# -*- coding: utf-8 -*-
"""Module Import

Name: GetEmailEventStatus

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
    if database.get_start_date(event) > datetime.now()
  ]

  # call generic email compilation module
  email_report.perform(flow, config, database, logger, "report", valid_events)
