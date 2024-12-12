import mattermostdriver
from user import User


class MattermostSync:
	def __init__(self, server: str, login: str, password: str):
		self.__api = mattermostdriver.Driver({'url': server.replace('https://', ''), 'login_id': login, 'password': password, 'port': 443})
		self.__api.login()

	def __get_userid(self, user: User) -> int:
		response = self.__api.users.get_user_by_username(user.username)
		return response['id']

	def sync_photo(self, user: User) -> bool:
		if user.photo == None:
			return False

		try:
			user_id = self.__get_userid(user)
			self.__api.users.set_user_profile_image(user_id, {'image': open(user.photo.filename, 'rb')})
			return True
		except:
			return False

	def sync_title(self, user: User) -> bool:
		try:
			user_id = self.__get_userid(user)
			self.__api.users.patch_user(user_id, options = {'position': user.position})
			return True
		except:
			return False
