from __future__ import annotations

import platform
from typing import Union


def set_text_windows(text: str) -> None:
    """

    Args:
      text: 

    Returns:

    """
    import win32clipboard
    import win32con

    win32clipboard.OpenClipboard()
    try:
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(text, win32con.CF_UNICODETEXT)
    finally:
        win32clipboard.CloseClipboard()


def set_text_gtk(text: str) -> None:
    """

    Args:
      text: 

    Returns:

    """
    import gtk

    cb = gtk.Clipboard()
    cb.set_text(text)
    cb.store()


def set_text_osx(text: str) -> None:
    """

    Args:
      text: 

    Returns:

    """
    scrap: bool = True
    try:
        import Carbon.Scrap  # type: ignore[import-not-found]
    except ModuleNotFoundError:
        scrap = False
    if scrap:
        Carbon.Scrap.ClearCurrentScrap()  # type: ignore[attr-defined]
        scrap_obj = Carbon.Scrap.GetCurrentScrap()  # type: ignore[attr-defined]
        scrap_obj.PutScrapFlavor("TEXT", 0, text)  # type: ignore[attr-defined]
    else:
        import subprocess

        try:
            encoded_text = text.encode()
        except AttributeError:
            encoded_text = text if isinstance(text, bytes) else text.encode()
        
        s = subprocess.Popen("pbcopy", stdin=subprocess.PIPE)
        s.communicate(encoded_text)


def set_text(text: str) -> None:
    """Copies text to the clipboard.

    Args:
      text: 

    Returns:

    """
    plat = platform.system()
    if plat == "Windows":
        set_text_windows(text)
    elif plat == "Linux":
        set_text_gtk(text)
    elif plat == "Darwin":
        set_text_osx(text)
    else:
        raise NotImplementedError("Cannot set clipboard text on platform %s" % plat)


copy = set_text


def get_text_windows() -> str:
    """ """
    import win32clipboard
    import win32con

    win32clipboard.OpenClipboard()
    try:
        text = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
    finally:
        win32clipboard.CloseClipboard()
    return str(text) if text is not None else ''


def get_text_osx() -> str:
    """ """
    import subprocess

    s = subprocess.Popen("pbpaste", stdout=subprocess.PIPE)
    result = s.communicate()[0]
    try:
        return result.decode()
    except UnicodeDecodeError:
        return result.decode('utf-8', errors='ignore')


def get_text() -> str:
    """ """
    plat = platform.system()
    if plat == "Windows":
        return get_text_windows()
    elif plat == "Darwin":
        return get_text_osx()
    else:
        raise NotImplementedError(
            "Cannot get text from clipboard on platform %s" % plat
        )
