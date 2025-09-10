"""
Vendored minimal winpaths functionality for cross-platform compatibility.

This module provides Windows system path access with cross-platform fallbacks.
On Windows, it uses the original winpaths logic. On other platforms, it provides
sensible defaults.
"""
from __future__ import annotations

import os
import platform
from typing import Optional

is_windows: bool = platform.system() == "Windows"

if is_windows:
    import ctypes
    from ctypes import windll, wintypes
    
    # Monkeypatch for Python 3 compatibility
    ctypes.wintypes.create_unicode_buffer = ctypes.create_unicode_buffer  # type: ignore[attr-defined]
    
    class PathConstants:
        CSIDL_PROGRAM_FILES = 38
    
    class WinPathsException(Exception):
        pass
    
    def _err_unless_zero(result: int) -> int:
        if result == 0:
            return result
        else:
            raise WinPathsException("Failed to retrieve windows path: %s" % result)
    
    _SHGetFolderPath = windll.shell32.SHGetFolderPathW
    _SHGetFolderPath.argtypes = [wintypes.HWND,
                                ctypes.c_int,
                                wintypes.HANDLE,
                                wintypes.DWORD, wintypes.LPCWSTR]
    _SHGetFolderPath.restype = _err_unless_zero
    
    def _get_path_buf(csidl: int) -> str:
        path_buf = wintypes.create_unicode_buffer(wintypes.MAX_PATH)  # type: ignore[attr-defined]
        result = _SHGetFolderPath(0, csidl, 0, 0, path_buf)
        return str(path_buf.value)
    
    def get_program_files() -> Optional[str]:
        """Returns the Program Files directory appropriate for the current process architecture."""
        return _get_path_buf(PathConstants.CSIDL_PROGRAM_FILES)

else:
    # Non-Windows platforms
    def get_program_files() -> Optional[str]:
        """Returns None on non-Windows platforms as Program Files is a Windows-specific concept."""
        return None