from typing import List
from ldap3 import *
from user import User
from user_photo import UserPhoto


class ActiveDirectory:
	def __init__(self, server: str, login: str, password: str):
		domain_user = 'BLACKWOOD\\' + login
		server = Server(host=server, get_info='ALL')
		self.__connection = Connection(server, user=domain_user, password=password, read_only=True, auto_bind=True)

	def get_attribute_safe(self, att, default=''):
		return att[0] if len(att) > 0 else default

	def save_temp_photo(self, bytes):
		tmp_file = tempfile.TemporaryFile(suffix='.jpg')
		with Image.open(io.BytesIO(bytes)) as photo:
				with photo.convert('RGB').resize((400, 400), Image.LANCZOS) as photo_rgb:
					photo_rgb.save(tmp_file, "JPEG")
					return tmp_file

		return None

	def __ad_entry_to_user(self, e):
		user = User()
		user.name = self.get_attribute_safe(e.cn)
		user.username = self.get_attribute_safe(e.sAMAccountName).lower()
		user.phone = self.get_attribute_safe(e.mobile)
		user.position = self.get_attribute_safe(e.title)
		user.department = self.get_attribute_safe(e.department)

		photo_bytes = self.get_attribute_safe(e.thumbnailPhoto, None)
		if photo_bytes:
			user.photo = UserPhoto(photo_bytes)

		return user

	def get_users(self, usernames: List[str] = []) -> User:
		attributes = attributes=['cn', 'sAMAccountName', 'mobile', 'thumbnailPhoto', 'title', 'department']
		query = 'OU=All Users,OU=Users,OU=intern.blackwood.gg,DC=intern,DC=blackwood,DC=gg'

		if usernames:
			for username in usernames:
				filter = '(&(objectCategory=Person)(sAMAccountName={}))'.format(username)
				self.__connection.search(query, filter, attributes=attributes)
				if len(self.__connection.entries) == 1:
					e = self.__connection.entries[0]
					yield self.__ad_entry_to_user(e)
		else:
			filter = '(&(objectCategory=Person)(sAMAccountName=*))'
			self.__connection.search(query, filter, attributes=attributes)
			self.__connection.entries.sort(key = lambda e: self.get_attribute_safe(e.cn))

			for e in self.__connection.entries:
				yield self.__ad_entry_to_user(e)