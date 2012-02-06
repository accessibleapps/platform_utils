import ctypes

def kill_windows_process(pid):
 PROCESS_TERMINATE = 1
 handle = ctypes.windll.kernel32.OpenProcess(PROCESS_TERMINATE, False, pid)
 ctypes.windll.kernel32.TerminateProcess(handle, -1)
 ctypes.windll.kernel32.CloseHandle(handle)
