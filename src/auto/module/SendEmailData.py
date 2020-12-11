# -*- coding: utf-8 -*-
"""Module Import

Name: SendEmailData

Sends the email data stored on the `email_message` input parameter to
the `recipient`.
"""
from common.msgraph import (
  initialize_account
)

def perform(flow, config, database, logger, **kwargs):

  # first check if the email really must be triggered
  if not database.params["trigger_email"]:
    logger.info("No email to be triggered...")
    logger.info("Finishing execution.")
    return

  # initialize account and mailbox
  account = initialize_account(config, logger)
  mailbox = account.mailbox()

  # compile new message
  message = mailbox.new_message()
  message.to.add([database.params["recipient"]])
  # message.sender.address = config.get_email("jenkins")
  message.subject = database.params["email_subject"]
  message.body    = database.params["email_message"]

  # add attachments
  if database.params["attachments"]:
    [
      message.attachments.add(attachment)
      for attachment in database.params["attachments"]
    ]

  # send message
  message.send()
