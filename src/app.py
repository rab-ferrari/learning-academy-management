# -*- coding: utf-8 -*-
"""Main App Script

Performs all of the application activities that roughly are:
  1. Initialize main objects and set execution environment
  2. Initialize main engine and launch flows
  3. Finish the execution - raise an error if any error happened
"""

import auto.args
import common.flow
import common.trace
import common.config
import common.params
import common.engine
import common.database
import common.utils.misc

# initialize parameters and main objects
common.params.initialize(__file__)
common.utils.misc.reset_log_dir()

config    = common.config.Config()
database  = common.database.Database()
flow      = common.flow.Flow()
args      = auto.args.Args(config, flow)
logger    = common.trace.create(common.params._LOG_MAIN, console=True)
logger.info(f"Initializing {common.params._JOB_NAME} version ({common.params._VERSION})")

# log selected environment
logger.info(f"Environment set to {config.env}")

# initialize main engine and launch flows
try:
  success = True
  logger.info("Initializing main engine...")
  engine  = common.engine.Engine(config, flow, database, logger)
  engine.start()

except Exception:
  logger.info("Main engine error! Stack trace:", exc_info=True)
  success = False

if success is False:
  raise ValueError
