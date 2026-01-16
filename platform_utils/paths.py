from __future__ import annotations

import inspect
import os
import platform
import subprocess
import sys
from types import ModuleType
from typing import Optional, Union

import platformdirs

from . import _winpaths


def is_frozen() -> bool:
    """ """
    # imp was removed in Python 3.12, but _imp still contains is_frozen.
    # This is what cffi (https://cffi.readthedocs.io) uses.
    import _imp

    return (
        hasattr(sys, "frozen")
        or "__compiled__" in globals()
        or _imp.is_frozen("__main__")
    )


plat: str = platform.system()
is_windows: bool = plat == "Windows"
is_mac: bool = plat == "Darwin"
is_linux: bool = plat == "Linux"
is_pyinstaller: bool = is_frozen() and getattr(sys, "_MEIPASS", False)


try:
    unicode  # type: ignore[name-defined]
except NameError:
    unicode = str


def app_data_path(app_name: str) -> str:
    """Cross-platform method for determining where to put application data.

    Args:
      app_name:  (Default value = None)

    Returns:

    """
    """Requires the name of the application"""
    if is_windows:
        # Use roaming=True to match winpaths.get_appdata() behavior (AppData\Roaming)
        path = platformdirs.user_data_dir(roaming=True)
    elif is_mac:
        path = os.path.join(os.path.expanduser(
            "~"), "Library", "Application Support")
    elif is_linux:
        path = os.path.expanduser("~")
        app_name = ".%s" % app_name.replace(" ", "_")
    else:
        raise RuntimeError("Unsupported platform")
    return os.path.join(path, app_name)


def prepare_app_data_path(app_name: str) -> str:
    """Creates the application's data directory, given its name.

    Args:
      app_name:

    Returns:

    """
    dir_path = app_data_path(app_name)
    return ensure_path(dir_path)


def embedded_data_path() -> str:
    """Return the path where embedded data files are stored.

    On Mac py2app bundles, this is Contents/Resources.
    On Windows py2exe/PyInstaller, this is the executable directory.
    """
    if is_mac and is_frozen():
        # sys.executable is in Contents/MacOS/python
        # Data files are in Contents/Resources
        exedir = os.path.dirname(sys.executable)  # Contents/MacOS
        bundle_contents = os.path.dirname(exedir)  # Contents
        return os.path.join(bundle_contents, "Resources")
    return app_path()


def get_executable() -> str:
    """Returns the full executable path/name if frozen, or the full path/name of the main module if not."""
    if is_frozen():
        if not is_mac:
            return sys.executable
        # On Mac, sys.executable points to python. We want the full path to the exe we ran.
        exedir = os.path.abspath(os.path.dirname(sys.executable))
        items = os.listdir(exedir)
        if "python" in items:
            items.remove("python")
        return os.path.join(exedir, items[0]) if items else sys.executable
    # Not frozen
    try:
        import __main__

        return os.path.abspath(__main__.__file__)
    except AttributeError:
        return sys.argv[0]


def get_module(level: int = 2) -> str:
    """Hacky method for deriving the caller of this function's module.

    Args:
      level:  (Default value = 2)

    Returns:

    """
    module: Optional[ModuleType] = inspect.getmodule(inspect.stack()[level][0])
    if module is None or module.__file__ is None:
        raise RuntimeError(f"Cannot determine module at stack level {level}")
    return module.__file__


def executable_directory() -> str:
    """Always determine the directory of the executable, even when run with py2exe or otherwise frozen"""
    if is_pyinstaller:
        return getattr(sys, '_MEIPASS', '')
    executable = get_executable()
    path = os.path.abspath(os.path.dirname(executable))
    return path


def app_path() -> str:
    """ """
    path = executable_directory()
    return path


def is_interactive() -> bool:
    """Returns True if the script is being ran from the interactive interpreter.
        Can be useful for providing additional information when debugging.

    Args:

    Returns:

    """
    import __main__

    return not hasattr(__main__, "__file__")


def module_path(level: int = 2) -> str:
    """

    Args:
      level:  (Default value = 2)

    Returns:


    """
    return os.path.abspath(os.path.dirname(get_module(level)))


def documents_path() -> str:
    """Cross-platform method for getting the user's Documents directory."""
    return platformdirs.user_documents_dir()


def safe_filename(filename: Union[str, bytes]) -> str:
    """Given a filename, returns a safe version with no characters that would not work on different platforms.

    Args:
      filename:

    Returns:

    """
    SAFE_FILE_CHARS = "'-_.()[]{}!@#$%^&+=`~ "
    filename = unicode(filename)
    new_filename = "".join(
        c for c in filename if c in SAFE_FILE_CHARS or c.isalnum())
    # Windows doesn't like directory names ending in space, macs consider filenames beginning with a dot as hidden, and windows removes dots at the ends of filenames.
    return new_filename.strip(" .")


def ensure_path(path: str) -> str:
    """Ensure existence of a path by creating all subdirectories.

    Args:
      path:

    Returns:

    """
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def start_file(path: str) -> None:
    """

    Args:
      path:

    Returns:

    """
    if is_windows:
        os.startfile(path)
    else:
        subprocess.Popen(["open", path])


def get_applications_path() -> Optional[str]:
    """Return the system applications directory."""
    if is_mac:
        return "/Applications"
    return _winpaths.get_program_files()
