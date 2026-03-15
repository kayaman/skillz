"""Tests for hash.py."""

from __future__ import annotations

from pathlib import Path

from skillz.core.hash import hash_directory


class TestHashDirectory:
    def test_deterministic(self, sample_skill: Path) -> None:
        h1 = hash_directory(sample_skill)
        h2 = hash_directory(sample_skill)
        assert h1 == h2

    def test_sha256_length(self, sample_skill: Path) -> None:
        h = hash_directory(sample_skill)
        assert len(h) == 64

    def test_changes_on_content_change(self, sample_skill: Path) -> None:
        h1 = hash_directory(sample_skill)
        (sample_skill / "SKILL.md").write_text("changed content")
        h2 = hash_directory(sample_skill)
        assert h1 != h2

    def test_changes_on_new_file(self, sample_skill: Path) -> None:
        h1 = hash_directory(sample_skill)
        (sample_skill / "new-file.md").write_text("new content")
        h2 = hash_directory(sample_skill)
        assert h1 != h2

    def test_ignores_dotfiles(self, sample_skill: Path) -> None:
        h1 = hash_directory(sample_skill)
        (sample_skill / ".gitignore").write_text("*.pyc")
        h2 = hash_directory(sample_skill)
        assert h1 == h2

    def test_empty_dir(self, tmp_path: Path) -> None:
        empty = tmp_path / "empty"
        empty.mkdir()
        h = hash_directory(empty)
        assert len(h) == 64
