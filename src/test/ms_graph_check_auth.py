from O365 import Account

scopes = [
  'https://graph.microsoft.com/email',
  'https://graph.microsoft.com/Mail.ReadWrite',
  'https://graph.microsoft.com/Mail.Send',
  'https://graph.microsoft.com/offline_access',
  'https://graph.microsoft.com/User.Read'
]  # you can use scope helpers here (see Permissions and Scopes section)

account = Account(('client_id', 'secret'))

if not account.is_authenticated:  # will check if there is a token and has not expired
    # ask for a login
    # console based authentication See Authentication for other flows
    account.authenticate(scopes=scopes)

# now we are autheticated
# use the library from now on

# ...