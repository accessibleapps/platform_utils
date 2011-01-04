import ctypes
import platform
import os

TYPES = {
 'Windows': (ctypes.LibraryLoader(ctypes.WinDLL), ctypes.WINFUNCTYPE, '.dll'),
 'Linux': (ctypes.LibraryLoader(ctypes.CDLL), ctypes.CFUNCTYPE, ['.so', '.so64']),
 'Darwin': (ctypes.LibraryLoader(ctypes.CDLL), ctypes.CFUNCTYPE, '.dylib'),
}

def load_library(library, lib_path="../lib"):
 which = TYPES[platform.system()]
 loader = which[0]
 ext = which[2]
 path = os.path.join(lib_path, library)
 if type(ext) == str:
  return loader.LoadLibrary('%s%s' % (path, ext))
 for n, i in enumerate(ext):
  try:
   loaded = loader.LoadLibrary('%s%s' % (path, ext))
  except OSError:
   if n < len(ext):
    continue
   else:
    raise
 return loaded

def get_functype():
 return TYPES[platform.system()][1]
