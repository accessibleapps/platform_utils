import ctypes
import collections
import platform
import os

TYPES = {
 'Linux': {
  'loader': ctypes.LibraryLoader(ctypes.CDLL),
  'functype': ctypes.CFUNCTYPE,
  'prefix': 'lib',
  'extension': '.so'
 },
 'Darwin': {
  'loader': ctypes.LibraryLoader(ctypes.CDLL),
  'functype': ctypes.CFUNCTYPE,
  'prefix': 'lib',
  'extension': '.dylib'
 },
}
if platform.system() == 'Windows':
 TYPES['Windows'] = {
  'loader': ctypes.LibraryLoader(ctypes.WinDLL),
  'functype': ctypes.WINFUNCTYPE,
  'prefix': "",
  'extension': '.dll'
 }

class LibraryLoadError(Exception): pass

def load_library(library, x86_path='.', x64_path='.', *args, **kwargs):
 library = '%s%s' % (TYPES[platform.system()]['prefix'], library)
 if platform.machine() == 'x86':
  path = os.path.join(x86_path, library)
 elif platform.machine() == 'x86_64':
  path = os.path.join(x64_path, library)
 lib = _find_lib(path)
 lib = _do_load(lib, *args, **kwargs)
 if lib is not None:
  return lib
 raise LibraryLoadError('unable to load %r. Provided library path: %r' % (library, path))

def _find_lib(path):
 ext = TYPES[platform.system()]['extension']
 return '%s%s' % (path, ext)
 
def _do_load(file, *args, **kwargs):
 loader = TYPES[platform.system()]['loader'] 
 return loader.LoadLibrary(file, *args, **kwargs)

def get_functype():
 return TYPES[platform.system()]['functype']
