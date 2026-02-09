"""Command-line entry point for the new project."""

from __future__ import annotations

import argparse
from datetime import datetime

from .core import greet


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Demo CLI for the new project")
    parser.add_argument("name", help="Name of the person to greet")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    greeting = greet(args.name, at=datetime.utcnow())
    print(greeting.format())
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
