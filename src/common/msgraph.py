# -*- coding: utf-8 -*-
"""MS Graph API Handling

Declares an O365 Account class already initialized. Since we already use a modularized
package, we don't need to modularize much further. It gives direct access to various
Microsoft products - many of which are already integrated and used within Flex such as:
  - Outlook
  - Office (Excel, Work, Access etc.)
  - Teams
  - Yammer

Note:
  Instructions on how to configure your account linked to Microsoft Azure can be found
  on https://pypi.org/project/O365/
"""

from O365 import Account


def initialize_account(config, logger):
  """Initialized Account

  Returns:
    (:obj:`O365.Account`): MS Graph modularized account
  """
  credentials = (config.secrets["msgraph.cliend_id"], config.secrets["msgraph.secret"])
  return Account(credentials)
