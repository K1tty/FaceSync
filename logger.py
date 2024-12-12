import os
import sys
from colorclass import Color, Windows, toggles


class Logger:
	def __init__(self):
		self.__init_colors()

	def __init_colors(self):
		if os.name == 'nt':
			Windows.enable(reset_atexit=True)

		if not sys.stdout.isatty():
			toggles.disable_all_colors()

	def info(self, message: str, newLine: bool = True):
		end_value = '\n' if newLine else ''
		print(message, end = end_value)

	def error(self, message: str):
		self.info(Color('{autored}%s{/red}' % message))

	def log_result(self, service: str, success: bool) -> None:
		success_str = Color('{autogreen}success{/green}') if success else Color('{autored}failed{/red}')
		print('    %s: %s' % (service, success_str))

	def log_separator(self):
		print('---------------------------------------------')