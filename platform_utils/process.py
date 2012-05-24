import platform
import ctypes
import os
import signal

_system = platform.system()

def kill_windows_process(pid):
 PROCESS_TERMINATE = 1
 handle = ctypes.windll.kernel32.OpenProcess(PROCESS_TERMINATE, False, pid)
 ctypes.windll.kernel32.TerminateProcess(handle, -1)
 ctypes.windll.kernel32.CloseHandle(handle)

def kill_unix_process(pid):
 try:
  os.kill(pid, signal.SIGKILL)
 except OSError:
  pass

def kill_process(pid):
 if pid < 0:
  return
 elif _system == "windows":
  kill_windows_process(pid)
 elif _system == "Darwin":
  kill_unix_process(pid)
