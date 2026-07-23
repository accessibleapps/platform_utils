from pathlib import Path

import platform_utils


def test_package_declares_inline_types() -> None:
    package_path = Path(platform_utils.__file__).parent

    assert (package_path / "py.typed").is_file()
