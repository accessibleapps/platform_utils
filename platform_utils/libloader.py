import ctypes
import collections
import platform
import os

TYPES = {
 'Linux': (ctypes.LibraryLoader(ctypes.CDLL), ctypes.CFUNCTYPE, {'x86': '.so', 'x86_64': '.so64'}),
 'Darwin': (ctypes.LibraryLoader(ctypes.CDLL), ctypes.CFUNCTYPE, '.dylib'),
}
if platform.system() == 'Windows':
 TYPES['Windows'] = (ctypes.LibraryLoader(ctypes.WinDLL), ctypes.WINFUNCTYPE, '.dll')

class LibraryLoadError(Exception): pass

def load_library(library, lib_path=None):
 if isinstance(lib_path, basestring):
  lib_path = [lib_path]
 for p in lib_path:
  path = os.path.join(p, library)
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
 elif isinstance(ext, collections.Mapping):
  return '%s%s' % (path, ext[platform.machine()])
 
def _do_load(file):
 loader = TYPES[platform.system()][0] 
 return loader.LoadLibrary(file)

def get_functype():
 return TYPES[platform.system()][1]
