"""skillz init — scaffold a new SKILL.md template."""

from __future__ import annotations

from pathlib import Path

import typer

from skillz.console import error, success
from skillz.core.config import SKILL_FILENAME

_TEMPLATE = """\
---
name: {name}
description: Brief description of what this skill does and when to use it.
---

# {title}

## When to Use

Use this skill when...

## Instructions

1. Step one
2. Step two
3. Step three
"""


def init(
    name: str = typer.Argument(None, help="Skill name (defaults to current directory name)"),
    directory: Path = typer.Option(".", "--dir", "-d", help="Output directory"),
) -> None:
    """Scaffold a new SKILL.md template."""
    if name is None:
        name = Path.cwd().name

    skill_dir = directory / name if directory != Path(".") else Path(name)
    skill_dir.mkdir(parents=True, exist_ok=True)

    skill_file = skill_dir / SKILL_FILENAME
    if skill_file.exists():
        error(f"{skill_file} already exists. Use a different name or directory.")
        raise typer.Exit(1)

    title = name.replace("-", " ").replace("_", " ").title()
    skill_file.write_text(_TEMPLATE.format(name=name, title=title))
    (skill_dir / "references").mkdir(exist_ok=True)

    success(f"Created {skill_file}")
    success(f"Edit {skill_file} to add your skill instructions.")
