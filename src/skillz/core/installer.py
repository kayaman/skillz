"""Install skill folders to target directories."""

from __future__ import annotations

import shutil
from pathlib import Path

from skillz.console import info, success, warning
from skillz.core.config import SKILL_FILENAME, global_skills_dir, project_skills_dir
from skillz.core.hash import hash_directory
from skillz.core.lockfile import add_entry
from skillz.models import SkillLockEntry, SkillSource


def install_skill(
    skill_dir: Path,
    source: SkillSource,
    *,
    global_install: bool = False,
    cwd: Path | None = None,
) -> list[str]:
    """Install skill(s) from a fetched directory.

    If skill_dir contains multiple subdirectories with SKILL.md, installs all of them.
    Returns list of installed skill names.
    """
    target_base = global_skills_dir() if global_install else project_skills_dir(cwd)
    target_base.mkdir(parents=True, exist_ok=True)

    installed: list[str] = []

    if (skill_dir / SKILL_FILENAME).exists():
        _install_single(skill_dir, target_base, source)
        installed.append(skill_dir.name)
    else:
        for child in sorted(skill_dir.iterdir()):
            if child.is_dir() and (child / SKILL_FILENAME).exists():
                _install_single(child, target_base, source)
                installed.append(child.name)

    if not installed:
        warning("No skills found to install.")

    return installed


def _install_single(skill_dir: Path, target_base: Path, source: SkillSource) -> None:
    """Install a single skill directory."""
    name = skill_dir.name
    dest = target_base / name

    if dest.exists():
        info(f"Updating existing skill '{name}'...")
        shutil.rmtree(dest)
    else:
        info(f"Installing skill '{name}'...")

    shutil.copytree(skill_dir, dest)

    folder_hash = hash_directory(dest)
    skill_path = f"skills/{name}/{SKILL_FILENAME}"
    entry = SkillLockEntry.create(source, skill_path, folder_hash)
    add_entry(target_base, name, entry)

    scope = "global" if "home" in str(target_base) else "project"
    success(f"Installed '{name}' ({scope}) → {dest}")
