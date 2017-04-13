from enum import Enum

class Region(Enum):
	EU   = 1
	NA   = 2
	RU   = 3
	ASIA = 4

	def domain(self):
		if self.name == 'NA':
			return 'com'
		else:
			return self.name.lower()

class Platform(Enum):
	XBOX = 1
	PS4  = 2