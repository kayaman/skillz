"""skillz update — re-fetch skills that have changed upstream."""

from __future__ import annotations

import typer

from skillz.console import error, info, success, warning
from skillz.core.config import global_skills_dir, project_skills_dir
from skillz.core.git import cleanup_temp, fetch_skill
from skillz.core.hash import hash_directory
from skillz.core.installer import install_skill
from skillz.core.lockfile import read_lockfile
from skillz.core.source_parser import parse_source


def update(
    name: str = typer.Argument(None, help="Skill name to update (all if omitted)"),
    global_install: bool = typer.Option(False, "--global", "-g", help="Update global skills"),
) -> None:
    """Check for updates and re-fetch changed skills."""
    skills_dir = global_skills_dir() if global_install else project_skills_dir()
    lock = read_lockfile(skills_dir)

    if not lock.skills:
        warning("No skills installed.")
        return

    targets = {name: lock.skills[name]} if name else lock.skills
    if name and name not in lock.skills:
        error(f"Skill '{name}' not found in lockfile.")
        raise typer.Exit(1)

    updated_count = 0
    for skill_name, entry in targets.items():
        if entry.source_type != "github":
            info(f"Skipping '{skill_name}' (local source)")
            continue

        info(f"Checking '{skill_name}'...")
        try:
            source = parse_source(f"{entry.source}@{skill_name}")
            tmp_path = fetch_skill(source)
            new_hash = hash_directory(tmp_path)

            if new_hash != entry.skill_folder_hash:
                info(f"'{skill_name}' has changes, updating...")
                install_skill(tmp_path, source, global_install=global_install)
                updated_count += 1
            else:
                info(f"'{skill_name}' is up to date.")

            cleanup_temp(tmp_path)
        except Exception as exc:
            warning(f"Failed to update '{skill_name}': {exc}")

    if updated_count:
        success(f"Updated {updated_count} skill(s).")
    else:
        info("All skills are up to date.")
