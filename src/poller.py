# -*- coding: utf-8 -*-
"""Poller Script

Opens the client account mailbox, looks for emails that satisfy the
job triggering condition and passes on the requirements to trigger
the main app.py job if necessary.
"""
import os
import json
import argparse
import html2text
import common.trace
import common.config
import common.params
import common.msgraph

# initialize parameters and main objects
common.params.initialize(__file__)
bat_file = os.path.join(common.params._PATH_STAGING, "app_command.bat")

# remove any previous app command files
try:
  os.remove(bat_file)
except:
  OSError

config    = common.config.Config()
logger    = common.trace.create(common.params._LOG_MAIN, console=True)
logger.info(f"Initializing {common.params._JOB_NAME} version ({common.params._VERSION})")

# declare only an environment argument
parser = argparse.ArgumentParser()
parser.add_argument(
  "environment",
  choices=config.get_env_options(),
  help="Target environment"
)
args = parser.parse_args()

# log selected environment
config.set_environment(args.environment)
logger.info(f"Environment set to {config.env}")

# declare ms graph account and look into mailbox
account = common.msgraph.initialize_account(config, logger)
mailbox = account.mailbox()
inbox   = mailbox.inbox_folder()

# define query - look for messages that satisfy the trigger regex
query = inbox.new_query().on_attribute("subject").contains(config.secrets["jenkins.trigger"])

# run the command for the first message it finds and end the program afterwards
for message in inbox.get_messages(limit=100, query=query):
  logger.info(f"Message {message} found! Start processing...")

  # store the email body data as a json file (for now it HAS to be correct)
  body = html2text.html2text(message.body)
  json_data = json.loads(body)

  # store the sender email as a parameter
  json_data["recipient"] = message.sender.address

  # dump the json file into the staging/input file
  with open(common.params._PATH_PARAMS, "w") as json_file:
    json.dump(json_data, json_file)

  # compile the command to be executed - also expected in the "json email data"
  output_command = f"call python app.py {config.env} -flow {json_data['flow']}"

  # write command to bat file
  with open(bat_file, "w") as f:
    f.write(output_command)

  # move message to archived folder and end execution
  # message.move(mailbox.archive_folder())
  return

# if the execution gets here, no files were found
logger.info("No new emails...")
