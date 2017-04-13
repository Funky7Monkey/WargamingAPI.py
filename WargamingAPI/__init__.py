


__title__ = 'WargamingAPI'
__author__ = 'Funky7Monkey'
__license__ = 'MIT'
__copyright__ = 'Copyright 2017 Funky7Monkey'
__version__ = '0.1.0'

from .WargamingAPI import WoT_PC_Client, WoT_Blitz_Client, WoT_Console_Client
from .utils import *
from .errors import *
import enums

VersionInfo = namedtuple('VersionInfo', 'major minor maintenance releaselevel serial')

version_info = VersionInfo(major=0, minor=1, maintenance=0, releaselevel='final', serial=0)