"""Integration tests for the list command."""

from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from skillz.cli import app
from skillz.core.lockfile import add_entry
from skillz.models import SkillLockEntry

runner = CliRunner()


class TestListSkills:
    def test_empty_list(self, tmp_path: Path, monkeypatch: object) -> None:
        import pytest

        mp = pytest.MonkeyPatch()  # noqa: N806
        mp.chdir(tmp_path)
        fake_global = tmp_path / "fake_global" / ".agents" / "skills"
        mp.setattr("skillz.commands.list.global_skills_dir", lambda: fake_global)
        result = runner.invoke(app, ["list"])
        assert "No skills installed" in result.output
        mp.undo()

    def test_list_with_skills(self, tmp_path: Path) -> None:
        import pytest

        mp = pytest.MonkeyPatch()  # noqa: N806
        mp.chdir(tmp_path)

        skills_dir = tmp_path / ".agents" / "skills"
        skills_dir.mkdir(parents=True)
        entry = SkillLockEntry(
            source="kayaman/skills",
            sourceType="github",
            sourceUrl="https://github.com/kayaman/skills.git",
            skillPath="skills/semver/SKILL.md",
            skillFolderHash="abc123",
            installedAt="2026-03-15T00:00:00.000Z",
            updatedAt="2026-03-15T00:00:00.000Z",
        )
        add_entry(skills_dir, "semver", entry)

        result = runner.invoke(app, ["list"])
        assert "semver" in result.output
        assert "kayaman/skills" in result.output
        mp.undo()

    def test_list_json_output(self, tmp_path: Path) -> None:
        import pytest

        mp = pytest.MonkeyPatch()  # noqa: N806
        mp.chdir(tmp_path)

        skills_dir = tmp_path / ".agents" / "skills"
        skills_dir.mkdir(parents=True)
        entry = SkillLockEntry(
            source="test/repo",
            sourceType="github",
            sourceUrl="",
            skillPath="skills/test/SKILL.md",
            skillFolderHash="xyz",
            installedAt="2026-01-01T00:00:00.000Z",
            updatedAt="2026-01-01T00:00:00.000Z",
        )
        add_entry(skills_dir, "test-skill", entry)

        result = runner.invoke(app, ["list", "--json"])
        assert result.exit_code == 0
        mp.undo()
