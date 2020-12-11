# -*- coding: utf-8 -*-
"""Flow Import

Name: RequestEventStatus

Activities performed:
  - updates the json file - mostly participants and their status
  - parses all events and retains only the "future" ones
  - compiles an email message using ad template (to send to communications team)
  - sends the email to the recipient found in the input.json file 
"""


def update_params(module, config, flow, database, logger, **kwargs):
  pass
