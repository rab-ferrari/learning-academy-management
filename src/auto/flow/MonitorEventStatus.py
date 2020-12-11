# -*- coding: utf-8 -*-
"""Flow Import

Name: MonitorEventStatus

Flow prepared to be deployed in a daily execution job. Activities performed:
  - update event database - mostly participant status
  - run alert event status and send email if required
  - run critical alert event status and send email if required
  - sends the email to the recipient found in the input.json file 
"""


def update_params(module, config, flow, database, logger, **kwargs):
  pass
