"""Tests for source_parser.py."""

from __future__ import annotations

from pathlib import Path

import pytest

from skillz.core.source_parser import parse_source
from skillz.models import SourceType


class TestParseSource:
    def test_owner_repo_at_skill(self) -> None:
        result = parse_source("kayaman/skills@semver")
        assert result.owner == "kayaman"
        assert result.repo == "skills"
        assert result.skill == "semver"
        assert result.ref == "main"
        assert result.source_type == SourceType.GITHUB

    def test_owner_repo_only(self) -> None:
        result = parse_source("vercel-labs/agent-skills")
        assert result.owner == "vercel-labs"
        assert result.repo == "agent-skills"
        assert result.skill == ""
        assert result.source_type == SourceType.GITHUB

    def test_owner_repo_at_skill_with_ref(self) -> None:
        result = parse_source("kayaman/skills@semver#v2")
        assert result.owner == "kayaman"
        assert result.repo == "skills"
        assert result.skill == "semver"
        assert result.ref == "v2"

    def test_github_prefix(self) -> None:
        result = parse_source("github:kayaman/skills@semver")
        assert result.owner == "kayaman"
        assert result.repo == "skills"
        assert result.skill == "semver"

    def test_local_relative_path(self, tmp_path: Path) -> None:
        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        result = parse_source(str(skill_dir))
        assert result.source_type == SourceType.LOCAL
        assert result.local_path == skill_dir
        assert result.skill == "my-skill"

    def test_local_dot_slash(self) -> None:
        result = parse_source("./my-skill")
        assert result.source_type == SourceType.LOCAL

    def test_local_absolute(self) -> None:
        result = parse_source("/tmp/my-skill")
        assert result.source_type == SourceType.LOCAL

    def test_invalid_format(self) -> None:
        with pytest.raises(ValueError, match="Invalid source format"):
            parse_source("not-a-valid-source")

    def test_whitespace_stripped(self) -> None:
        result = parse_source("  kayaman/skills@semver  ")
        assert result.owner == "kayaman"
        assert result.skill == "semver"

    def test_display_name_full(self) -> None:
        result = parse_source("kayaman/skills@semver")
        assert result.display_name == "kayaman/skills@semver"

    def test_display_name_repo_only(self) -> None:
        result = parse_source("kayaman/skills")
        assert result.display_name == "kayaman/skills"

    def test_repo_url(self) -> None:
        result = parse_source("kayaman/skills@semver")
        assert result.repo_url == "https://github.com/kayaman/skills.git"
