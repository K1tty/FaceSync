from user_photo import UserPhoto


class User:
	name: str = ''
	username: str = ''
	photo: UserPhoto = None
	position: str = ''
	department: str = ''
	phone: str = ''

	def print(self):
		print('---> ' + self.username)
		print('  name: ' + self.name)
		print('  username: ' + self.username)
		if self.photo:
			print('  photo: ' + self.photo.filename)
		print('  position: ' + self.position)
		print('  department: ' + self.department)
		print('  phone: ' + self.phone)