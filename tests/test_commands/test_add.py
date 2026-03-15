"""Integration tests for the add command."""

from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from skillz.cli import app
from skillz.core.config import SKILL_FILENAME
from skillz.core.lockfile import read_lockfile

runner = CliRunner()


class TestAddLocal:
    def test_add_local_skill(self, sample_skill: Path, tmp_path: Path, monkeypatch: object) -> None:
        project = tmp_path / "project"
        project.mkdir()
        import pytest

        mp = pytest.MonkeyPatch()  # noqa: N806
        mp.chdir(project)

        result = runner.invoke(app, ["add", str(sample_skill), "-y"])
        assert result.exit_code == 0
        assert "Installed" in result.output

        installed = project / ".agents" / "skills" / "sample-skill"
        assert installed.exists()
        assert (installed / SKILL_FILENAME).exists()

        lock = read_lockfile(project / ".agents" / "skills")
        assert "sample-skill" in lock.skills
        mp.undo()

    def test_add_nonexistent_local_path(self) -> None:
        result = runner.invoke(app, ["add", "./nonexistent-skill", "-y"])
        assert result.exit_code == 1


class TestAddGitHub:
    def test_add_invalid_source(self) -> None:
        result = runner.invoke(app, ["add", "not-valid", "-y"])
        assert result.exit_code == 1
        assert "Invalid source format" in result.output
