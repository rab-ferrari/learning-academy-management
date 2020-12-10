# -*- coding: utf-8 -*-
"""Module Import

Name: CreateEventDatabase

TODO: describe
"""
from O365 import Account


def perform(flow, config, database, logger, **kwargs):
  pass
  account = Account(('4167c9fc-6e68-4036-ad9a-f16e0ec3d5b3', 'hWW18TXAUs4bboh~CJsRGP5_e94-1D-_uV'))
  mailbox = account.mailbox()

  inbox = mailbox.inbox_folder()

  for message in inbox.get_messages():
    print(message)
