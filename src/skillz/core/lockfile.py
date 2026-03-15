"""Read and write .skill-lock.json files."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from skillz.core.config import LOCKFILE_NAME
from skillz.models import SkillLock, SkillLockEntry


def _lockfile_path(base_dir: Path) -> Path:
    parent = base_dir.parent if base_dir.name == "skills" else base_dir
    return parent / LOCKFILE_NAME


def read_lockfile(base_dir: Path) -> SkillLock:
    """Read the lockfile from the given directory. Returns empty lock if not found."""
    path = _lockfile_path(base_dir)
    if not path.exists():
        return SkillLock()
    data = json.loads(path.read_text())
    skills = {}
    for name, entry_data in data.get("skills", {}).items():
        skills[name] = SkillLockEntry(**entry_data)
    return SkillLock(version=data.get("version", 3), skills=skills)


def write_lockfile(base_dir: Path, lock: SkillLock) -> None:
    """Write the lockfile to the given directory."""
    path = _lockfile_path(base_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    data: dict[str, object] = {
        "version": lock.version,
        "skills": {
            name: {
                "source": entry.source,
                "sourceType": entry.source_type,
                "sourceUrl": entry.source_url,
                "skillPath": entry.skill_path,
                "skillFolderHash": entry.skill_folder_hash,
                "installedAt": entry.installed_at,
                "updatedAt": entry.updated_at,
            }
            for name, entry in lock.skills.items()
        },
    }
    path.write_text(json.dumps(data, indent=4) + "\n")


def add_entry(base_dir: Path, name: str, entry: SkillLockEntry) -> None:
    """Add or update a skill entry in the lockfile."""
    lock = read_lockfile(base_dir)
    if name in lock.skills:
        entry.installed_at = lock.skills[name].installed_at
        entry.updated_at = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    lock.skills[name] = entry
    write_lockfile(base_dir, lock)


def remove_entry(base_dir: Path, name: str) -> bool:
    """Remove a skill entry from the lockfile. Returns True if it existed."""
    lock = read_lockfile(base_dir)
    if name not in lock.skills:
        return False
    del lock.skills[name]
    write_lockfile(base_dir, lock)
    return True
