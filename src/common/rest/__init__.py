# -*- coding: utf-8 -*-
"""Rest API Handling

Declares class for rest API modularization and allows other inherited
classes to already access and return standardized output data without
worrying about the request at all.
"""
import requests
from requests.auth import HTTPDigestAuth


class Rest:
  """Rest API Requests

  Its methods implements generic rest API requests given a
  secret token, url, payload and other parameters.

  Attributes:
    config (:obj:`config.Config`): Config handler
    logger (:obj:`logging.Logger`): Log handler
    headers (dict): Rest API request header
  """

  def __init__(self, config, logger):
    """Rest API Abstract Class Constructor

    Initializes oauth token attributes.

    Note:
      Inherited classes must initialize the headers attribute
      with the appropriate token before performing any requests.

    Args:
      config (:obj:`config.Config`): Initializes attribute
      logger (:obj:`logging.Logger`): Initializes attribute
    """
    self.config   = config
    self.logger   = logger
    self.headers  = {
      "Content-Type": "application/json; charset=utf-8",
      "auth-key": None
    }

  def request(self, url, payload=None, **kwargs):
    """Rest API Request

    Performs a generic request based on the `payload`.

    Args:
      url (str): Url where requests must be performed
      payload (dict): Request arguments

    Raises:
      (Exception): If the request returned any failure

    Returns:
      (dict): Data retrieved from API request
    """
    if payload is None:
      payload = {}

    try:
      request = requests.get(url=url, headers=self.headers, params=payload)
      return request.json()
    except Exception:
      raise
