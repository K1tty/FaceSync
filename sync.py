#!/usr/bin/env python3

"""
Usage:
    sync.py --help
    sync.py <admin-login> <admin-password> [options] [<username>...]

Options:
    -h --help                          Show this screen
    <admin-login>                      Admin username to login to AD/Jira/Confluence/Mattermost
    <admin-password>                   Admin password to login to AD/Jira/Confluence/Mattermost
    --ad-url <ad-url>                  ActiveDirectory server URL [default: kiewnad01.intern.blackwood.gg]
    --jira-url <jira-url>              Jira server URL [default: http://jira]
    --confluence-url <confluence-url>  Confluence server URL [default: http://confluence]
    --mattermost-url <mattermost-url>  Mattermost server URL [default: https://matter.blackwood.gg]
    --skip-jira                        Skip sync to Jira
    --skip-confluence                  Skip sync to Confluence
    --skip-mattermost                  Skip sync to Mattermost
"""

import os
import re
import logging
from docopt import docopt
from typing import Callable
from user import User
from logger import Logger
from active_directory import ActiveDirectory
from jira_sync import JiraSync
from confluence_sync import ConfluenceSync
from mattermost_sync import MattermostSync
from colorclass import Color


def safe_create(system: str, creator):
	try:
		logger.info('Connecting to %s ... ' % system, newLine=False)
		instance = creator()
		logger.info(Color('{autogreen}Succeed{/green}'))
		return instance
	except:
		logger.info(Color('{autored}Failed{/red}'))
		return None

if __name__ == '__main__':
	logging.disable(logging.CRITICAL)   # suppress error logging to stdout from third-party modules

	logger = Logger()
	logger.log_separator()

	args = docopt(__doc__)
	admin_login = args['<admin-login>']
	admin_password = args['<admin-password>']
	ad_url = args['--ad-url']
	jira_url = args['--jira-url']
	confluence_url = args['--confluence-url']
	mattermost_url = args['--mattermost-url']
	skip_jira = args['--skip-jira']
	skip_confluence = args['--skip-confluence']
	skip_mattermost = args['--skip-mattermost']
	usernames = args['<username>']

	ad = safe_create('Active Directory', lambda: ActiveDirectory(ad_url, admin_login, admin_password))

	if ad:
		users = ad.get_users(usernames)

		jira = safe_create('Jira', lambda: JiraSync(jira_url, admin_login, admin_password)) if not skip_jira else None
		confluence = safe_create('Confluence', lambda: ConfluenceSync(confluence_url, admin_login, admin_password)) if not skip_confluence else None
		mattermost = safe_create('Mattermost', lambda: MattermostSync(mattermost_url, admin_login, admin_password)) if not skip_mattermost else None

		logger.log_separator()

		for user in users:
			logger.info(Color("Sync user data for '{autoyellow}%s{/yellow}' ..." % user.username))

			if jira:
				jira_success = jira.sync(user)
				logger.log_result('Jira', jira_success)

			if confluence:
				confluence_success = confluence.sync(user)
				logger.log_result('Confluence', confluence_success)

			if mattermost:
				mattermost_photo_success = mattermost.sync_photo(user)
				logger.log_result('Mattermost (photo)', mattermost_photo_success)

				mattermost_title_success = mattermost.sync_title(user)
				logger.log_result('Mattermost (title)', mattermost_title_success)

			del user