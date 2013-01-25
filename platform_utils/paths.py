import inspect
import platform
import os
import sys
import string
import unicodedata


def app_data_path(app_name=None):
 """Cross-platform method for determining where to put application data."""
 """Requires the name of the application"""
 plat = platform.system()
 if plat == 'Windows':
  import winpaths
  path = winpaths.get_appdata()
 elif plat == 'Darwin':
  path = os.path.join(os.path.expanduser('~'), 'Library', 'Application Support')
 elif plat == 'Linux':
  path = os.path.expanduser('~')
  app_name = '.%s' % app_name.replace(' ', '_')
 return os.path.join(path, app_name)

def prepare_app_data_path(app_name):
 """Creates the application's data directory, given its name."""
 dir = app_data_path(app_name)
 if not os.path.exists(dir):
  os.makedirs(dir)
 return dir

def embedded_data_path():
 if platform.system() == 'Darwin' and is_frozen():
  return os.path.abspath(os.path.join(app_path(), '..', 'Resources'))
 return app_path()

def is_frozen():
 """Return a bool indicating if application is compressed"""
 import imp
 return hasattr(sys, 'frozen') or imp.is_frozen("__main__")

def get_executable():
 if is_frozen():
  return sys.executable
 return sys.argv[0]

def get_module():
 """Hacky method for deriving the caller of this function's module."""
 return inspect.stack()[2][1]

def app_path():
 """Always determine the path to the main module, even when run with py2exe or otherwise frozen"""
 return os.path.abspath(os.path.dirname(get_executable()))

def module_path():
 return os.path.abspath(os.path.dirname(get_module()))

def executable_path():
 return os.path.join(app_path(), get_executable())

def documents_path():
 """On windows, returns the path to My Documents. On OSX, returns the user's Documents folder. For anything else, returns the user's home directory."""
 plat = platform.system()
 if plat == 'Windows':
  import winpaths
  path = winpaths.get_my_documents()
 elif plat == 'Darwin':
  path = os.path.join(os.path.expanduser('~'), 'Documents')
 else:
  path = os.path.expanduser('~')
 return path

def safe_filename(filename):
 """Given a filename, returns a safe version with no characters that would not work on different platforms."""
 SAFE_FILE_CHARS = "'-_.() "
 filename = unicode(filename)
 valid_chars = "%s%s%s" % (SAFE_FILE_CHARS, string.ascii_letters, string.digits)
 cleanedFilename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore')
 return ''.join(c for c in cleanedFilename if c in valid_chars)

def ensure_path(path):
 if not os.path.exists(path):
  os.makedirs(path)
