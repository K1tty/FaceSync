import os
import tempfile
from jira import JIRA
from jira import JIRAError
from user import User
from PIL import Image

class JiraSync:
	def __init__(self, server: str, login: str, password: str):
		self.__jira = JIRA(server=server, auth=(login, password), max_retries=0)

	def __cleanup_old_avatars(self, user: User):
		avatars = self.__jira.user_avatars(user.username)
		for avatar in avatars['custom']:
			self.__jira.delete_user_avatar(user.username, avatar['id'])

	def sync(self, user: User) -> bool:
		if user.photo == None:
			return False

		try:
			self.__cleanup_old_avatars(user)
			
			photo_data = open(user.photo.filename, 'rb').read()

			cropping_props = self.__jira.create_temp_user_avatar(user.username, user.photo.filename, 0, photo_data, 'image/jpeg')
			cropping_props['cropperOffsetX'] = 0
			cropping_props['cropperOffsetY'] = 0
			cropping_props['cropperWidth'] = user.photo.SIZE_IN_PIXELS
			cropping_props['needsCropping'] = True

			avatar_props = self.__jira.confirm_user_avatar(user.username, cropping_props)
			self.__jira.set_user_avatar(user.username, avatar_props['id'])

			return True
		except JIRAError:
			return False