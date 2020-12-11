"""MS Graph API Setup

This setup must be run every 90 days to maintain the MS Graph
authentication working.

Default scopes that should be used are:
  scopes = [
    'https://graph.microsoft.com/Calendars.ReadWrite',
    'https://graph.microsoft.com/email',
    'https://graph.microsoft.com/Mail.ReadWrite',
    'https://graph.microsoft.com/Mail.Send',
    'https://graph.microsoft.com/offline_access',
    'https://graph.microsoft.com/User.Read'
  ]
"""
from O365 import Account
import common.config
import common.params

# initialize parameters
common.params.initialize(__file__)

scopes = [
  "basic",
  "message_all",
  "calendar_all"
]

# instance credentials
config = common.config.Config()

# hard coded 'dev' environment
config.set_environment("dev")

# retrieve secrets
client_id = config.secrets["msgraph.client_id"]
secret    = config.secrets["msgraph.secret"]
credentials = (client_id, secret)

# create account object
account = Account(credentials)

# check if there is a token and has not expired
if not account.is_authenticated:
    
  # ask for a login console based authentication See Authentication for other flows
  account.authenticate(scopes=scopes)

# test the token refresh if you want
# account.connection.refresh_token()
