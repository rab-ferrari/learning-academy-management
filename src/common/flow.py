# -*- coding: utf-8 -*-
"""Flow File and Execution Handling

Implements flow asset parsing and handling methods.
"""

import os
import json

import common.params

# flow statuses
_FLOW_INACTIVE  = "INACTIVE"
_FLOW_ACTIVE    = "ACTIVE"
_FLOW_RUNNING   = "RUNNING"
_FLOW_FAILURE   = "FAILURE"
_FLOW_SUCCESS   = "SUCCESS"

# custom flow alias
_FLOW_CUSTOM    = "CustomFlow"


class Flow:
  """Flow File Handling

  Parses the flows and modules files and stores its information.

  Attributes:
    flows (list): Dict options with available flows
    modules (list): Available modules
    status (dict): Status of all flows
    params (dict): Module and flow parameters
  """

  def __init__(self, flows_file=None, modules_file=None):
    """Flow Class Constructor

    Initializes the class attributes. Dependencies files must be correctly
    configured in their respective common.params attributes.

    Args:
      flows_file (str): Path to flows file if non-default
      modules_file (str): Path to modules file if non-default
    """

    # initialize flows and modules file paths
    if flows_file is None:
      flows_file    = common.params._PATH_FLOWS
    if modules_file is None:
      modules_file  = common.params._PATH_MODULES

    # import modules
    self.modules = {}
    with open(modules_file) as json_file:
      self.modules = json.load(json_file)

    # import flows
    self.flows = []
    with open(flows_file) as json_file:
      self.flows = json.load(json_file)

    # TODO: check and raise error if a flow contains an inexistent module

    # initialize status attribute for all flows
    self.status = {flow:_FLOW_INACTIVE for flow in self.flows}

  def get_modules(self):
    """Module Retrieval

    Returns:
      (list): Available modules
    """
    return self.modules

  def get_flows(self):
    """Flow Retrieval

    Returns:
      (list): Available flows
    """
    return self.flows

  def get_flow_modules(self, flow):
    """Flow Modules Retrieval

    Args:
      flow (str): Flow to have its modules retrieved

    Returns:
      (list): Modules contained in the flow passed as argument
    """
    return self.flows[flow]

  def activate_flow(self, flow):
    """Activate Flow

    Enables the execution for a flow of modules.

    Args:
      flow (str): Flow to be activated
    """
    self.status[flow] = _FLOW_ACTIVE

  def generate_activate_flow(self, modules):
    """Generate and 

    Returns:
      (list): Available flows
    """
    self.flows[_FLOW_CUSTOM]  = modules
    self.status[_FLOW_CUSTOM] = _FLOW_ACTIVE

  def flow_is_active(self, flow):
    """Flow Active

    Args:
      flow (str): Flow to be checked

    Returns:
      (bool): Flag indicating if flow is active
    """
    return self.status[flow] == _FLOW_ACTIVE

  def get_active_flows(self):
    """Retrieve Active Flows

    Returns:
      (list): Active Flows
    """
    return [flow for flow in self.flows if self.flow_is_active(flow)]

  def start_flow(self, flow):
    """Initialize Flow

    Initializes the flow execution flag.

    Args:
      flow (str): Flow to be executed
    """
    self.status[flow] = _FLOW_RUNNING

  def flow_is_running(self, flow):
    """Flow Being Executed

    Args:
      flow (str): Flow to be checked

    Returns:
      (bool): Flag indicating if flow is currently executing
    """
    return self.status[flow] == _FLOW_RUNNING

  def finish_flow(self, flow, success=True):
    """Finish Flow

    Args:
      flow (str): Flow to be executed
    """
    self.status[flow] = _FLOW_SUCCESS if success is True else _FLOW_FAILURE

  def stop_flow_failure(self, flow):
    """Stop Flow Execution - Failure

    Args:
      flow (str): Flow to be stopped
    """
    self.finish_flow(flow, success=False)
