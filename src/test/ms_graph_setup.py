from O365 import Account, FileSystemTokenBackend

credentials = ('client_id', 'secret')

# this will store the token under: "my_project_folder/my_folder/my_token.txt".
# you can pass strings to token_path or Path instances from pathlib
token_backend = FileSystemTokenBackend(token_path='my_folder', token_filename='my_token.txt')
account = Account(credentials, token_backend=token_backend)
account.authenticate()
print(account.is_authenticated)

# This account instance tokens will be stored on the token_backend configured before.
# You don't have to do anything more
# ...