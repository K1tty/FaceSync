import os
import io
import tempfile
from PIL import Image


class UserPhoto:
	SIZE_IN_PIXELS = 400

	def __init__(self, photo_bytes: bytes):
		with tempfile.TemporaryFile(suffix='.jpg', delete=False) as tmp_file:
			photo_img = self.normalize_photo(photo_bytes)
			photo_img.save(tmp_file, "JPEG")
			photo_img.close()
			self.filename = tmp_file.name

	def __del__(self):
		os.remove(self.filename)

	def check_size_valid(self, width, height):
		if width != height:
			raise Exception('Photo must be square')

		if width < self.SIZE_IN_PIXELS:
			raise Exception('Photo must be at least {}x{} size'.format(self.SIZE_IN_PIXELS, self.SIZE_IN_PIXELS))

	def normalize_photo(self, photo_bytes: bytes) -> Image:
		with Image.open(io.BytesIO(photo_bytes)) as photo:
			self.check_size_valid(photo.width, photo.height)
			return photo.convert('RGB').resize((self.SIZE_IN_PIXELS, self.SIZE_IN_PIXELS), Image.LANCZOS)
					