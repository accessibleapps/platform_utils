# Replacement for py2exe distributed module
# Avoids the use of the standard py2exe console.
# Just import this file and it should go away
from __future__ import annotations

import sys
from typing import Any

if hasattr(sys, "frozen"):  # true only if we are running as a py2exe app

    class Blackhole(object):
        """Mock file object that does nothing."""

        def write(self, text: Any) -> None:
            pass

        def flush(self) -> None:
            pass

        def isatty(self) -> bool:
            return False

    sys.stdout = Blackhole()  # type: ignore[assignment]
    sys.stderr = Blackhole()  # type: ignore[assignment]
    del Blackhole
    del sys
