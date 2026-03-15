"""skillz remove — uninstall a skill."""

from __future__ import annotations

import shutil

import typer

from skillz.console import error, info, success, warning
from skillz.core.config import global_skills_dir, project_skills_dir
from skillz.core.lockfile import remove_entry


def remove(
    name: str = typer.Argument(help="Name of the skill to remove"),
    global_install: bool = typer.Option(False, "--global", "-g", help="Remove from global skills"),
) -> None:
    """Remove an installed skill."""
    skills_dir = global_skills_dir() if global_install else project_skills_dir()
    skill_path = skills_dir / name

    if not skill_path.exists():
        error(f"Skill '{name}' not found in {'global' if global_install else 'project'} scope.")
        raise typer.Exit(1)

    info(f"Removing skill '{name}'...")
    shutil.rmtree(skill_path)
    removed = remove_entry(skills_dir, name)

    if removed:
        success(f"Removed '{name}' and cleaned lockfile.")
    else:
        warning(f"Removed '{name}' directory but it was not in the lockfile.")
