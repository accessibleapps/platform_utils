from __future__ import absolute_import, annotations, unicode_literals

try:
    import winreg as winreg
except ImportError:
    import winreg

SHELL_REGKEY: str = r"Directory\shell"


def context_menu_integrate(item_key_name: str, item_display_text: str, item_command: str) -> None:
    """Creates an item that will appear in the standard windows context menu."""
    app_menu_key = winreg.OpenKey(
        winreg.HKEY_CLASSES_ROOT, SHELL_REGKEY, 0, winreg.KEY_WRITE
    )
    menu_item_key = winreg.CreateKey(app_menu_key, item_key_name)
    winreg.SetValueEx(menu_item_key, None, None, winreg.REG_SZ, item_display_text)
    item_command_key = winreg.CreateKey(menu_item_key, "command")
    winreg.SetValueEx(item_command_key, None, None, winreg.REG_SZ, item_command)
