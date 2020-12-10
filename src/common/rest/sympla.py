# -*- coding: utf-8 -*-
"""Sympla Rest API Handling

Declares class for standard Sympla requests to be shared among modules.
Documentation available at https://developers.sympla.com.br/api-doc/index.html
"""
from common.rest import (
  Rest
)

_URL_EVENTS       = "https://api.sympla.com.br/public/v3/events"
_URL_PARTICIPANTS = "https://api.sympla.com.br/public/v3/events/{}/participants"


class Sympla(Rest):
  """Sympla Rest API Requests

  Inherits from the abstract class `Rest` and implements standard
  requests.
  """

  def __init__(self, config, logger):
    """Rest API Class Constructor

    Calls parent class constructor - initializes attributes.
    """
    super().__init__(config, logger)
    self.headers = {
      "s_token": self.config.get_secret("sympla.token_value")
    }

  def get_event(self, name):
    """Get Event

    Args:
      name (str): Event name

    Raises:
      (ValueError): When the event for that name can't be found

    Returns:
      (dict): Data regarding the given event
    """
    data = super().request(_URL_EVENTS)
    for event_data in data["data"]:
      if event_data["name"] == name:
        return event_data

    # if flow reaches here, event hasn't been found - raise exception
    raise ValueError("Event name not found!")

  def get_participants(self, event_id):
    """Get Event Participants

    Returns all event participants info for a given event.

    TODO:
      All participants are being retrieved, no "canceled" field was found, but
      this treatment should be done here if available.
    PENDING TEST:
      If canceled participants automatically are removed from the request output.

    Args:
      event_id (int): Sympla internal event id

    Returns:
      (list): Event participants
    """
    data = super().request(_URL_PARTICIPANTS.format(event_id))
    return data["data"]
