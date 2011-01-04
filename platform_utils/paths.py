import platform
import os
import sys

from functools import wraps

def merge_paths(func):
 @wraps(func)
 def merge_paths_wrapper(*a, **k):
  return os.path.join(func(**k), *a).encode('UTF-8')
 return merge_paths_wrapper

@merge_paths
def app_data_path(app_name=None):
 """Cross-platform method for determining where to put application data."""
 """Requires the name of the application"""
 plat = platform.system()
 if plat == 'Windows':
  import ctypes
  path = ctypes.create_unicode_buffer(260)
  if ctypes.windll.shell32.SHGetFolderPathW(0, 0x001a, 0, 0, ctypes.byref(path)) != 0:
 		raise ctypes.WinError()
  path = path.value
 elif plat == 'Darwin':
  path = os.path.join(os.path.expanduser('~'), 'Library', 'Application Support')
 elif plat == 'Linux':
  path = os.path.expanduser('~')
  app_name = '.%s' % app_name.replace(' ', '_')
 return os.path.join(path, app_name)
