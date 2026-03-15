"""Git operations for fetching skills from GitHub."""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

from skillz.console import error, info
from skillz.core.config import SKILL_FILENAME, SKILL_SEARCH_DIRS
from skillz.models import SkillSource


def _run_git(args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )


def fetch_skill(source: SkillSource) -> Path:
    """Clone a repo and extract the skill folder(s). Returns path to the skill directory."""
    tmp_dir = Path(tempfile.mkdtemp(prefix="skillz-"))

    try:
        result = _run_git(
            [
                "clone",
                "--depth",
                "1",
                "--single-branch",
                "--branch",
                source.ref,
                source.repo_url,
                str(tmp_dir / "repo"),
            ]
        )
        if result.returncode != 0:
            error(f"git clone failed: {result.stderr.strip()}")
            raise RuntimeError(f"Failed to clone {source.repo_url}: {result.stderr.strip()}")

        repo_dir = tmp_dir / "repo"
        return _locate_skill(repo_dir, source, tmp_dir)
    except Exception:
        shutil.rmtree(tmp_dir, ignore_errors=True)
        raise


def _locate_skill(repo_dir: Path, source: SkillSource, tmp_dir: Path) -> Path:
    """Find the skill folder inside a cloned repo."""
    if source.skill:
        for search_dir in SKILL_SEARCH_DIRS:
            candidate = repo_dir / search_dir / source.skill
            if candidate.is_dir() and (candidate / SKILL_FILENAME).exists():
                dest = tmp_dir / source.skill
                shutil.copytree(candidate, dest)
                shutil.rmtree(repo_dir, ignore_errors=True)
                return dest

        error(f"Skill '{source.skill}' not found in {source.display_name}")
        raise FileNotFoundError(f"Skill '{source.skill}' not found in repo")

    skills_found: list[Path] = []
    for search_dir in SKILL_SEARCH_DIRS:
        search_path = repo_dir / search_dir
        if not search_path.is_dir():
            continue
        for child in search_path.iterdir():
            if child.is_dir() and (child / SKILL_FILENAME).exists():
                skills_found.append(child)

    if not skills_found:
        if (repo_dir / SKILL_FILENAME).exists():
            skill_name = source.repo
            dest = tmp_dir / skill_name
            shutil.copytree(repo_dir, dest, ignore=shutil.ignore_patterns(".git"))
            shutil.rmtree(repo_dir, ignore_errors=True)
            return dest
        error(f"No skills found in {source.display_name}")
        raise FileNotFoundError("No SKILL.md files found in repo")

    result_dir = tmp_dir / "_all_skills"
    result_dir.mkdir()
    for skill_dir in skills_found:
        shutil.copytree(skill_dir, result_dir / skill_dir.name)
    shutil.rmtree(repo_dir, ignore_errors=True)
    info(f"Found {len(skills_found)} skills: {', '.join(s.name for s in skills_found)}")
    return result_dir


def cleanup_temp(path: Path) -> None:
    """Remove a temporary directory created by fetch_skill."""
    parent = path.parent if path.name != path.parent.name else path
    if str(parent).startswith(tempfile.gettempdir()):
        shutil.rmtree(parent, ignore_errors=True)
