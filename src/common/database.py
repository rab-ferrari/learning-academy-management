# -*- coding: utf-8 -*-
"""Database Data Handling

Implements persistent data handling. To simplify the initial implementation
and since large volumes of data aren't expected, the data is simply stored
on an external json file and imported/edited on each execution.
"""
import os
import json
import shutil
import common.params
from datetime import (
  datetime
)
from common.params import (
  _PATH_DATABASE,
  _PATH_PARAMS,
  _PATH_STAGING,
  _PATH_ARTS,
  _RESPONSE_STATUS_DECLINED,
  _RESPONSE_STATUS_PENDING,
  _RESPONSE_STATUS_TENTATIVE,
  _RESPONSE_STATUS_CONFIRMED,
)


class Database:
  """Database Handling

  Imports json data, stores it and implements retrieval/set methods.
  The `data` attribute will be a 'public attribute' and will be accessed
  directly through the class instance.

  The program input parameters will also be available on the params json
  file, but these are expected not to be persistent and change with every
  execution. the `params` attribute will also be public.

  Attributes:
    data_file (str): Path to data file for persistent storage
    data (dict): Dict options with available flows
  """

  def __init__(self, data_file=None, params_file=None):
    """Database Class Constructor

    Initializes the class attributes.

    Args:
      data_file (str): Path to database file if non-default
      params_file (str): Path to params if non-default
    """
    # initialize database and params file paths
    if data_file is None:
      data_file   = common.params._PATH_DATABASE
    self.data_file = data_file
    if params_file is None:
      params_file = common.params._PATH_PARAMS

    # import data
    self.data = {}
    with open(self.data_file) as json_file:
      self.data = json.load(json_file)

    # import params
    self.params = {}
    with open(params_file) as json_file:
      self.params = json.load(json_file)

    # look for any image files - if found, store on arts path
    self.art = None
    for source_file in os.listdir(common.params._PATH_STAGING):
      if source_file.endswith(".png"):
        target_file = os.path.join(common.params._PATH_ARTS, "art.png")
        shutil.move(os.path.join(common.params._PATH_STAGING, source_file), target_file)
        self.art = target_file
        break

    # TODO: debug only - hard coded art
    self.art = os.path.join(common.params._PATH_ARTS, "art.png")

  def __del__(self):
    """Database Class Destructor

    Writes back the data content to the persistent json file.
    """
    with open(self.data_file, "w") as json_file:
      json.dump(self.data, json_file, indent=2)

  def get_event_input(self):
    """Get Event Input

    Returns:
      (str): Event passed as input parameter
    """
    return self.params["event"]

  def set_event_input(self, event):
    """Set Event Input

    Args:
      event (str): Event to be setted as input parameter
    """
    self.params["event"] = event

  def get_capacity(self, event):
    """Get Event Capacity

    Args:
      event (str): Event identifier

    Returns:
      (int): Event capacity
    """
    return self.data["events"][event]["capacity"]

  def get_participant_emails(self, event):
    """Get Participant Emails

    Args:
      event (str): Event identifier

    Returns:
      (list): Participant emails for a given event
    """
    return [
      participant["email"]
      for participant in self.data["events"][event]["participants"]
    ]

  def get_teacher_emails(self, event):
    """Get Teacher Emails

    Args:
      event (str): Event identifier

    Returns:
      (list): Participant emails for a given event
    """
    return [
      teacher["email"]
      for teacher in self.data["events"][event]["teachers"]
    ]

  def get_participants(self, event):
    """Get Participants Data

    Args:
      event (str): Event identifier

    Returns:
      (tuple): Participant emails and names
    """
    return [
      (f"{participant['first_name']} {participant['last_name']}", participant["email"])
      for participant in self.data["events"][event]["participants"]
    ]

  def get_teachers(self, event):
    """Get Teacher Data

    Args:
      event (str): Event identifier

    Returns:
      (tuple): Teacher emails and names
    """
    return [
      (f"{teacher['first_name']} {teacher['last_name']}", teacher["email"])
      for teacher in self.data["events"][event]["teachers"]
    ]

  def set_participant_status(self, event, email, status):
    """Set Participant Status

    Updates the participant status for a given event and email.

    Args:
      event (str): Event identifier
      email (str): Participant email
      status (str): New participant status
    """
    for participant in self.data["events"][event]["participants"]:
      if participant["email"] == email:
        participant["status"] = status

  def get_meeting_datetime(self, meeting):
    """Get Meeting Datetime

    Args:
      meeting (str): Meeting identifier

    Returns:
      (datetime): Meeting datetime
    """
    return datetime.strptime(meeting["datetime"], "%Y-%m-%d %H:%M:%S")

  def get_start_date(self, event):
    """Get Start Date

    Retrieve the first class date for an event.

    Args:
      event (str): Event identifier

    Returns:
      (datetime): First meeting date
    """
    return min([
      self.get_meeting_datetime(meeting)
      for meeting in self.data["events"][event]["meetings"]
    ])

  def get_start_delay(self, event):
    """Get Start Delay

    Args:
      event (str): Event identifier

    Returns:
      (int): Delay in days for the event to begin
    """
    return (self.get_start_date(event) - datetime.now()).days

  def get_participants_by_status(self, event, status):
    """Get Participants by Status

    Args:
      event (str): Event identifier
      status (str): Status identifier

    Returns:
      (list): Compiled name + email of participants for each status
    """
    return [
      participant
      for participant in self.data["events"][event]["participants"]
      if participant["status"] == status
    ]

  def compile_participants_reference(self, participants):
    """Get Participants Reference

    Args:
      participants (list): Generic list of participants (list of dicts)

    Returns:
      (list): List of strings containing the participants "name + <email>"
    """
    return [
      f"{participant['first_name']} {participant['last_name']} &#60;{participant['email']}&#62;"
      for participant in participants
    ]

  def get_event_occupancy(self, event):
    """Get Event Occupancy

    Args:
      event (str): Event identifier

    Returns:
      (dict): event occupancy by status (including 'open' and 'total' slots)
    """
    occupancy = {
      status: len(self.get_participants_by_status(event, status))
      for status in [
        _RESPONSE_STATUS_DECLINED,
        _RESPONSE_STATUS_PENDING,
        _RESPONSE_STATUS_TENTATIVE,
        _RESPONSE_STATUS_CONFIRMED
      ]
    }
    total_slots = self.data["events"][event]["capacity"]
    occupancy["open_slots"]   = total_slots - sum([
      occupancy[status] for status in occupancy
    ])
    occupancy["total_slots"]  = total_slots
    return occupancy

  def get_status_report_params(self, event):
    """Get Status Report Parameters

    Args:
      event (str): Event identifier

    Returns:
      (dict): Parameters used in the main status report
    """
    slot_params = self.get_event_occupancy(event)

    # evaluate open slots percentage
    open_percentage = round(
      (slot_params["open_slots"] / self.get_capacity(event)) * 100,
      2
    )

    # retrieve compiled lists of participants (and teacher)
    tentative_list  = self.get_participants_by_status(event, _RESPONSE_STATUS_TENTATIVE)
    tentative_list  = self.compile_participants_reference(tentative_list)
    canceled_list   = self.get_participants_by_status(event, _RESPONSE_STATUS_DECLINED)
    canceled_list   = self.compile_participants_reference(canceled_list)
    teacher         = self.compile_participants_reference(self.data["events"][event]["teachers"])[0]

    params = {}
    params["event_name"]    = event
    params["event_url"]     = self.data["events"][event]["sympla_url"]
    params["teacher"]       = teacher
    params["start_date"]    = self.get_start_date(event)
    params["days_to_start"] = self.get_start_delay(event)
    params["total_spots"]   = self.data["events"][event]["capacity"]
    params["open_spots"]    = slot_params["open_slots"]
    params["confirmations"] = slot_params[_RESPONSE_STATUS_CONFIRMED]
    params["tentatives"]    = slot_params[_RESPONSE_STATUS_TENTATIVE]
    params["canceled"]      = slot_params[_RESPONSE_STATUS_DECLINED]
    params["pending"]       = slot_params[_RESPONSE_STATUS_PENDING]
    params["open_percentage"] = open_percentage
    params["tentative_list"]  = tentative_list
    params["canceled_list"]   = canceled_list

    return params
