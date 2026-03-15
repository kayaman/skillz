"""Paths, defaults, and constants."""

from __future__ import annotations

from pathlib import Path

LOCKFILE_NAME = ".skill-lock.json"
SKILL_FILENAME = "SKILL.md"
SKILLS_DIR_NAME = "skills"
AGENTS_DIR = ".agents"

DEFAULT_REF = "main"
SKILL_SEARCH_DIRS = ["skills", "."]


def global_skills_dir() -> Path:
    return Path.home() / AGENTS_DIR / SKILLS_DIR_NAME


def project_skills_dir(cwd: Path | None = None) -> Path:
    base = cwd or Path.cwd()
    return base / AGENTS_DIR / SKILLS_DIR_NAME


def global_lockfile() -> Path:
    return Path.home() / AGENTS_DIR / LOCKFILE_NAME


def project_lockfile(cwd: Path | None = None) -> Path:
    base = cwd or Path.cwd()
    return base / AGENTS_DIR / LOCKFILE_NAME
