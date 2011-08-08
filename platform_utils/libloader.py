import ctypes
import collections
import platform
import os

TYPES = {
 'Linux': (ctypes.LibraryLoader(ctypes.CDLL), ctypes.CFUNCTYPE, '.so'),
 'Darwin': (ctypes.LibraryLoader(ctypes.CDLL), ctypes.CFUNCTYPE, '.dylib'),
}
if platform.system() == 'Windows':
 TYPES['Windows'] = (ctypes.LibraryLoader(ctypes.WinDLL), ctypes.WINFUNCTYPE, '.dll')

class LibraryLoadError(Exception): pass

def load_library(library, x86_path='.', x64_path='.'):
 if platform.machine() == 'x86':
  path = os.path.join(x86_path, library)
 elif platform.machine() == 'x86_64':
  path = os.path.join(x64_path, library)
 lib = _find_lib(path)
 lib = _do_load(lib)
 if lib is not None:
  return lib
 raise LibraryLoadError('unable to load %r. Provided library path: %r' % (library, path))

def _find_lib(path):
 ext = TYPES[platform.system()][2]
 possible_files = []
 if isinstance(ext, basestring):
  return '%s%s' % (path, ext)
 
def _do_load(file):
 loader = TYPES[platform.system()][0] 
 return loader.LoadLibrary(file)

def get_functype():
 return TYPES[platform.system()][1]
