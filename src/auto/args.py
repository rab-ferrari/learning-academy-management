# -*- coding: utf-8 -*-
"""Argument Processing

TODO: documentation
"""
import logging
import argparse

import common.trace

_ALLOWED_LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR"]


class Args:
  """Command Line Argument Handling

  The arguments are defined using the `argparse` package. Immediately after parsing
  the arguments, it defined the modules that must be executed.

  Attributes:
    args (:obj:`argparser.parser.parse_args`): Contains all cmd line arguments
  """

  def __init__(self, config, flow):
    """Args Class Constructor

    Instantiates, fetches from command line, applies rules and initializes all
    argument values for the program.

    Args:
      config (:obj:`common.config.Config`): Configuration handling
      flow (:obj:`common.flow.Flow`): Flow and module handling
    """
    parser = argparse.ArgumentParser()

    # required arguments
    parser.add_argument(
      "environment",
      choices=config.get_env_options(),
      help="Target environment"
    )

    # module selection arguments
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
      "-flow",
      nargs="+",
      default=[],
      choices=flow.get_flows(),
      help="Executed selected flows"
    )
    group.add_argument(
      "-module",
      nargs="+",
      default=[],
      choices=flow.get_modules(),
      help="Execute selected modules"
    )

    # secrets file path
    parser.add_argument(
      "-secrets_file",
      dest="secrets_file",
      action="store",
      help="Path of secrets file (shhh)"
    )

    # debug arguments
    parser.add_argument(
      "-loglevel",
      choices=_ALLOWED_LOG_LEVELS,
      action="store",
      default="INFO",
      help="Logging level"
    )

    # parse arguments
    self.args = parser.parse_args()

    # initialize logger configurations
    common.trace._LOG_LEVEL = logging._nameToLevel[self.args.loglevel]

    # initialize selected environment and remove all other ones
    config.set_environment(self.args.environment)
    config.limit_env_options([self.args.environment])

    # activate enabled flows
    for flow_entry in self.args.flow:
      flow.activate_flow(flow_entry)

    # generate a flow with enabled modules and activate it
    if self.args.module:
      flow.generate_activate_flow(self.args.module)
