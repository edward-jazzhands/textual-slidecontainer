"""Textual-SlideContainer
Copyright (c) 2025 Edward Jazzhands.
Licensed under the MIT License.

To use:
```
from textual_slidecontainer import SlideContainer
```

Package standards:
- Type Checking (Pyright and MyPy) - strict
- Linting - Ruff
- Formatting - Black - max 110 characters / line
"""

from importlib.metadata import version as get_version
from textual_slidecontainer.slidecontainer import SlideContainer

__all__ = [
    "SlideContainer",
]
__version__ = get_version("textual_slidecontainer")
