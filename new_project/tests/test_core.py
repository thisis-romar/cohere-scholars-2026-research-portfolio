from datetime import datetime

from new_project.core import Greeting, greet


def test_greet_returns_greeting_with_expected_message():
    timestamp = datetime(2024, 1, 1)
    greeting = greet("Researcher", at=timestamp)

    assert isinstance(greeting, Greeting)
    assert greeting.message == "Welcome to the new project, Researcher!"
    assert greeting.timestamp == timestamp
    assert greeting.format() == "[2024-01-01T00:00:00] Welcome to the new project, Researcher!"
