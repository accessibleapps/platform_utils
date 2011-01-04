import ctypes
import platform
import os

TYPES = {
 'Windows': (ctypes.LibraryLoader(ctypes.WinDLL), ctypes.WINFUNCTYPE),
 'Linux': (ctypes.LibraryLoader(ctypes.CDLL), ctypes.CFUNCTYPE),
 'Darwin': (ctypes.LibraryLoader(ctypes.CDLL), ctypes.CFUNCTYPE),
}

def load_library(library, lib_path="../lib"):
 loader = TYPES[platform.system()][0]
 path = os.path.join(lib_path, library)
 try:
  loaded = loader.LoadLibrary(path)
 except OSError:
  if platform.system == 'Linux' and not path.endswith('64'):
   path = '%s64' % path
   loaded = loader.LoadLibrary(path)
 return loaded

def get_functype():
 return TYPES[platform.system()][1]
