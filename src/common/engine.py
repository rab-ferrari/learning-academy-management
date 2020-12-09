# -*- coding: utf-8 -*-
"""Main Engine and Thread Initialization

Implements thread module initialization by calling a single thread function.
"""
import os
import importlib
import common.trace
import common.params

_AUTO_MODULE_PATH = "auto.module"
_AUTO_FLOW_PATH   = "auto.flow"


class Engine:
  """Main Engine - Flow Execution

  Implements a standard initialization for all flows/modules.

  Attributes:
    config (:obj:`common.config.Config`): Configuration information handling
    flow (:obj:`common.flow.Flow`): Flow handling
    logger (:obj:`logging.Logger`): Log handler
  """

  def __init__(self, config, flow, database, logger):
    """Engine Class Constructor

    Initializes the class attributes.
    """
    self.config   = config
    self.flow     = flow
    self.logger   = logger
    self.database = database

  def start(self):
    """Engine Main Executor

    Executes all initialized flows by iterating over them and sequentially
    executing each module.

    Raises:
      Exception: If there was some execution error on the main thread
    """

    success = True
    flows   = self.flow.get_active_flows()
    self.logger.info(f"Will execute {len(flows)} flows...")

    # iterate over rows
    for flow in flows:

      # initialize current row attributes
      modules = self.flow.get_flow_modules(flow)
      self.flow.start_flow(flow)
      self.logger.info(common.params._FLOW_MESSAGE_START.format(flow))
      self.logger.info(f"Flow {flow}: Will execute {len(modules)} modules...")

      # import flow transition module
      module_id   = f"{_AUTO_FLOW_PATH}.{flow}"
      module_spec = importlib.util.find_spec(module_id)

      self.logger.info(f"Importing module {module_id}")
      if module_spec is None:
        self.logger.error(f"{module_id} NOT FOUND!")
        return

      flow_transition_module = importlib.import_module(module_id)
      self.logger.info(f"{module_id} imported.")

      # call generic module work function to assign which module to run
      for module in modules:

        # keep running next modules while
        if self.flow.flow_is_running(flow):
          module_work(module, flow, self.config, self.flow, self.database, self.logger)
        else:
          success = False
          self.flow.finish_flow(flow, success=False)
          self.logger.info(common.params._FLOW_MESSAGE_ERROR.format(flow))
          break

        # run flow transition module
        flow_transition_module.update_params(
          module,
          self.config,
          self.flow,
          self.database,
          self.logger
        )
        self.logger.info(common.params._FLOW_TRANSITION_MESSAGE.format(flow, module))

      # log final flow message
      self.logger.info(common.params._FLOW_MESSAGE_SUCCESS.format(flow))
      self.flow.finish_flow(flow, success=True)

    # log final engine message and raise error if there was a failure
    self.logger.info(f"Finished all flows.")
    if success is False:
      raise ValueError


def module_work(module, flow, config, flow_handler, database, main_logger):
  """Module Importing and Execution

  """
  logger = common.trace.create(
    os.path.join(common.params._LOG_PATH_MODULES, f"{flow}.{module}.log")
  )
  main_logger.info(common.params._MODULE_MESSAGE_START.format(module))
  logger.info     (common.params._MODULE_MESSAGE_START.format(module))

  try:
    module_id   = f"{_AUTO_MODULE_PATH}.{module}"
    module_spec = importlib.util.find_spec(module_id)

    # import module
    logger.info(f"Importing module {module_id}")
    if module_spec is None:
      logger.error(f"{module_id} NOT FOUND!")
      raise ValueError

    imported_module = importlib.import_module(module_id)
    logger.info(f"{module_id} imported - starting module operations...")
    imported_module.perform(flow_handler, config, database, logger)

  except Exception:
    main_logger.error(common.params._MODULE_MESSAGE_ERROR.format(module))
    logger.error     (common.params._MODULE_MESSAGE_ERROR.format(module))
    main_logger.warning(f"Interruped execution - flow {flow} - caused by module {module}")
    flow_handler.stop_flow_failure(flow)
    return

  main_logger.info(common.params._MODULE_MESSAGE_SUCCESS.format(module))
  logger.info     (common.params._MODULE_MESSAGE_SUCCESS.format(module))
