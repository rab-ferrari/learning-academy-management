# -*- coding: utf-8 -*-
"""Module Import

Name: GetEmailAd

Retrieves the total event status for an input event and replies
it to the recipient - bot in the input paremeters.
"""
from datetime import (
  datetime
)
from auto.module.generic import (
  email_report
)


def perform(flow, config, database, logger, **kwargs):

  # retrieve list of valid events
  valid_events = [database.params["event"]]

  # call generic email compilation module
  email_report.perform(flow, config, database, logger, "advertising", valid_events)

  # adjust recipient to communications team
  database.params["recipient"] = database.params["recipient"]
