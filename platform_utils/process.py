from __future__ import annotations

import ctypes
import os
import platform
import signal


def kill_windows_process(pid: int) -> None:
    PROCESS_TERMINATE = 1
    SYNCHRONIZE = 1048576
    handle = ctypes.windll.kernel32.OpenProcess(
        PROCESS_TERMINATE | SYNCHRONIZE, False, pid
    )
    ctypes.windll.kernel32.TerminateProcess(handle, -1)
    ctypes.windll.kernel32.WaitForSingleObject(handle, 1000)
    ctypes.windll.kernel32.CloseHandle(handle)


def kill_unix_process(pid: int) -> None:
    try:
        os.kill(pid, getattr(signal, 'SIGKILL', 9))
    except OSError:
        pass


def kill_process(pid: int) -> None:
    """Forcefully kills a process."""
    if pid < 0:
        return
    if platform.system() == "Windows":
        kill_windows_process(pid)
    else:
        kill_unix_process(pid)
