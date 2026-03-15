from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture
def tmp_project(tmp_path: Path) -> Path:
    """Create a temporary project directory with .agents/skills/ structure."""
    skills_dir = tmp_path / ".agents" / "skills"
    skills_dir.mkdir(parents=True)
    return tmp_path


@pytest.fixture
def tmp_global(tmp_path: Path) -> Path:
    """Create a temporary global skills directory."""
    skills_dir = tmp_path / ".agents" / "skills"
    skills_dir.mkdir(parents=True)
    return tmp_path


@pytest.fixture
def sample_skill(tmp_path: Path) -> Path:
    """Create a sample skill directory with SKILL.md."""
    skill_dir = tmp_path / "sample-skill"
    skill_dir.mkdir()
    skill_md = skill_dir / "SKILL.md"
    skill_md.write_text(
        "---\nname: sample-skill\n"
        "description: A sample skill for testing.\n---\n\n"
        "# Sample Skill\n\nThis is a test skill.\n"
    )
    refs = skill_dir / "references"
    refs.mkdir()
    (refs / "example.md").write_text("# Reference\n\nSome reference content.\n")
    return skill_dir
