"""Parse skill source strings into SkillSource objects."""

from __future__ import annotations

import re
from pathlib import Path

from skillz.models import SkillSource, SourceType


def parse_source(raw: str) -> SkillSource:
    """Parse a source string into a SkillSource.

    Supported formats:
        owner/repo@skill        — specific skill from a repo
        owner/repo@skill#ref    — specific skill at a git ref
        owner/repo              — all skills from a repo
        ./local/path            — local directory
        /absolute/path          — local directory
    """
    raw = raw.strip()

    if raw.startswith(("./", "../", "/")) or Path(raw).is_dir():
        return SkillSource(
            source_type=SourceType.LOCAL,
            local_path=Path(raw).resolve(),
            skill=Path(raw).name,
        )

    ref = "main"
    if "#" in raw:
        raw, ref = raw.rsplit("#", 1)

    match = re.match(r"^(?:github:)?([^/@]+)/([^/@]+)(?:@(.+))?$", raw)
    if not match:
        msg = (
            f"Invalid source format: '{raw}'. "
            "Expected: owner/repo, owner/repo@skill, or a local path."
        )
        raise ValueError(msg)

    owner, repo, skill = match.group(1), match.group(2), match.group(3) or ""
    return SkillSource(owner=owner, repo=repo, skill=skill, ref=ref)
