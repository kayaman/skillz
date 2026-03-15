"""Tests for lockfile.py."""

from __future__ import annotations

import json
from pathlib import Path

from skillz.core.lockfile import add_entry, read_lockfile, remove_entry, write_lockfile
from skillz.models import SkillLock, SkillLockEntry


class TestReadLockfile:
    def test_missing_file_returns_empty(self, tmp_path: Path) -> None:
        lock = read_lockfile(tmp_path / "skills")
        assert lock.version == 3
        assert lock.skills == {}

    def test_reads_existing(self, tmp_path: Path) -> None:
        lockfile = tmp_path / ".skill-lock.json"
        lockfile.write_text(
            json.dumps(
                {
                    "version": 3,
                    "skills": {
                        "semver": {
                            "source": "kayaman/skills",
                            "sourceType": "github",
                            "sourceUrl": "https://github.com/kayaman/skills.git",
                            "skillPath": "skills/semver/SKILL.md",
                            "skillFolderHash": "abc123",
                            "installedAt": "2026-01-01T00:00:00.000Z",
                            "updatedAt": "2026-01-01T00:00:00.000Z",
                        }
                    },
                }
            )
        )
        lock = read_lockfile(tmp_path / "skills")
        assert "semver" in lock.skills
        assert lock.skills["semver"].source == "kayaman/skills"
        assert lock.skills["semver"].skill_folder_hash == "abc123"


class TestWriteLockfile:
    def test_creates_file(self, tmp_path: Path) -> None:
        lock = SkillLock(
            skills={
                "test": SkillLockEntry(
                    source="test/repo",
                    sourceType="github",
                    sourceUrl="https://github.com/test/repo.git",
                    skillPath="skills/test/SKILL.md",
                    skillFolderHash="def456",
                    installedAt="2026-01-01T00:00:00.000Z",
                    updatedAt="2026-01-01T00:00:00.000Z",
                )
            }
        )
        write_lockfile(tmp_path / "skills", lock)
        lockfile = tmp_path / ".skill-lock.json"
        assert lockfile.exists()
        data = json.loads(lockfile.read_text())
        assert data["version"] == 3
        assert data["skills"]["test"]["source"] == "test/repo"
        assert data["skills"]["test"]["skillFolderHash"] == "def456"

    def test_roundtrip(self, tmp_path: Path) -> None:
        lock = SkillLock(
            skills={
                "roundtrip": SkillLockEntry(
                    source="a/b",
                    sourceType="github",
                    sourceUrl="https://github.com/a/b.git",
                    skillPath="skills/roundtrip/SKILL.md",
                    skillFolderHash="xyz",
                    installedAt="2026-02-01T00:00:00.000Z",
                    updatedAt="2026-02-01T00:00:00.000Z",
                )
            }
        )
        write_lockfile(tmp_path / "skills", lock)
        loaded = read_lockfile(tmp_path / "skills")
        assert loaded.skills["roundtrip"].source == "a/b"
        assert loaded.skills["roundtrip"].skill_folder_hash == "xyz"


class TestAddEntry:
    def test_adds_new_entry(self, tmp_path: Path) -> None:
        entry = SkillLockEntry(
            source="test/repo",
            sourceType="github",
            sourceUrl="",
            skillPath="skills/new/SKILL.md",
            skillFolderHash="hash1",
            installedAt="2026-01-01T00:00:00.000Z",
            updatedAt="2026-01-01T00:00:00.000Z",
        )
        add_entry(tmp_path / "skills", "new", entry)
        lock = read_lockfile(tmp_path / "skills")
        assert "new" in lock.skills

    def test_updates_existing_preserves_installed_at(self, tmp_path: Path) -> None:
        first = SkillLockEntry(
            source="test/repo",
            sourceType="github",
            sourceUrl="",
            skillPath="skills/existing/SKILL.md",
            skillFolderHash="hash1",
            installedAt="2025-01-01T00:00:00.000Z",
            updatedAt="2025-01-01T00:00:00.000Z",
        )
        add_entry(tmp_path / "skills", "existing", first)

        second = SkillLockEntry(
            source="test/repo",
            sourceType="github",
            sourceUrl="",
            skillPath="skills/existing/SKILL.md",
            skillFolderHash="hash2",
            installedAt="2026-06-01T00:00:00.000Z",
            updatedAt="2026-06-01T00:00:00.000Z",
        )
        add_entry(tmp_path / "skills", "existing", second)
        lock = read_lockfile(tmp_path / "skills")
        assert lock.skills["existing"].installed_at == "2025-01-01T00:00:00.000Z"
        assert lock.skills["existing"].skill_folder_hash == "hash2"


class TestRemoveEntry:
    def test_removes_existing(self, tmp_path: Path) -> None:
        entry = SkillLockEntry(
            source="test/repo",
            sourceType="github",
            sourceUrl="",
            skillPath="skills/gone/SKILL.md",
            skillFolderHash="hash1",
            installedAt="2026-01-01T00:00:00.000Z",
            updatedAt="2026-01-01T00:00:00.000Z",
        )
        add_entry(tmp_path / "skills", "gone", entry)
        assert remove_entry(tmp_path / "skills", "gone") is True
        lock = read_lockfile(tmp_path / "skills")
        assert "gone" not in lock.skills

    def test_returns_false_for_missing(self, tmp_path: Path) -> None:
        assert remove_entry(tmp_path / "skills", "nope") is False
