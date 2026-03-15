"""Pydantic models for skillz."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path

from pydantic import BaseModel, Field


class SourceType(StrEnum):
    GITHUB = "github"
    LOCAL = "local"


class SkillSource(BaseModel):
    """Parsed skill source reference."""

    owner: str = ""
    repo: str = ""
    skill: str = ""
    ref: str = "main"
    source_type: SourceType = SourceType.GITHUB
    local_path: Path | None = None

    @property
    def display_name(self) -> str:
        if self.source_type == SourceType.LOCAL:
            return str(self.local_path)
        if self.skill:
            return f"{self.owner}/{self.repo}@{self.skill}"
        return f"{self.owner}/{self.repo}"

    @property
    def repo_url(self) -> str:
        return f"https://github.com/{self.owner}/{self.repo}.git"


class SkillLockEntry(BaseModel):
    """Single skill entry in the lockfile."""

    source: str
    source_type: str = "github"
    source_url: str = ""
    skill_path: str = Field(alias="skillPath", default="")
    skill_folder_hash: str = Field(alias="skillFolderHash", default="")
    installed_at: str = Field(alias="installedAt", default="")
    updated_at: str = Field(alias="updatedAt", default="")

    model_config = {"populate_by_name": True}

    @classmethod
    def create(cls, source: SkillSource, skill_path: str, folder_hash: str) -> SkillLockEntry:
        now = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        return cls(
            source=f"{source.owner}/{source.repo}" if source.owner else str(source.local_path),
            source_type=source.source_type.value,
            source_url=source.repo_url if source.source_type == SourceType.GITHUB else "",
            skillPath=skill_path,
            skillFolderHash=folder_hash,
            installedAt=now,
            updatedAt=now,
        )


class SkillLock(BaseModel):
    """The .skill-lock.json file structure (v3 compatible with vercel-labs/skills)."""

    version: int = 3
    skills: dict[str, SkillLockEntry] = Field(default_factory=dict)


class AgentInfo(BaseModel):
    """Detected AI agent information."""

    name: str
    skills_dir: str
    marker: str

    @property
    def display(self) -> str:
        return f"{self.name} ({self.skills_dir})"
