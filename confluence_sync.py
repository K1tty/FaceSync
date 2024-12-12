import os
import xmlrpc.client
from user import User


class ConfluenceSync:
	def __init__(self, server: str, login: str, password: str):
		self.__server = xmlrpc.client.ServerProxy(server + '/rpc/xmlrpc')
		self.__token = self.__server.confluence1.login(login, password)

	def sync(self, user: User) -> bool:
		if user.photo == None:
			return True

		photo_name = os.path.basename(user.photo.filename)
		photo_data = open(user.photo.filename, 'rb').read()

		try:
			return self.__server.confluence1.addProfilePicture(self.__token, user.username, photo_name, 'image/jpeg', photo_data)
		except:
			return False