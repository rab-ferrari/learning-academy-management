# -*- coding: utf-8 -*-
"""Module Import

Name: AlertEventStatusCritical

Retrieves the overall event status of events that will happen in exactly 3 days.
"""
from auto.module.generic import (
  email_report
)


def perform(flow, config, database, logger, **kwargs):

  # retrieve list of valid events
  valid_events = [
    event
    for event in database.data["events"]
    if int(config.get_alert_info("critical_days")) == database.get_start_delay(event)
  ]

  # call generic email compilation module
  email_report.perform(flow, config, database, logger, "alert_critical", valid_events)
