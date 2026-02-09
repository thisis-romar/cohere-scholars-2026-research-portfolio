"""Core functionality for the new project."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Greeting:
    """Structured representation of a greeting message."""

    message: str
    timestamp: datetime

    def format(self) -> str:
        """Return the greeting message decorated with its timestamp."""
        return f"[{self.timestamp.isoformat()}] {self.message}"


def greet(name: str, *, at: datetime | None = None) -> Greeting:
    """Create a :class:`Greeting` for ``name``.

    Parameters
    ----------
    name:
        The recipient of the greeting.
    at:
        Optional datetime to associate with the greeting. Defaults to ``datetime.utcnow()``.
    """

    timestamp = at or datetime.utcnow()
    message = f"Welcome to the new project, {name}!"
    return Greeting(message=message, timestamp=timestamp)
