"""Detect active AI agent from project and home directory markers."""

from __future__ import annotations

from pathlib import Path

from skillz.models import AgentInfo

_AGENT_MARKERS: list[tuple[str, str, str]] = [
    (".cursor", "Cursor", ".cursor/rules/"),
    (".claude", "Claude Code", ".claude/"),
    (".codex", "Codex", ".codex/"),
    (".github/copilot", "GitHub Copilot", ".github/copilot/"),
    (".amp", "Amp", ".amp/"),
    (".cline", "Cline", ".cline/"),
    (".continue", "Continue", ".continue/"),
    (".kiro", "Kiro", ".kiro/"),
]


def detect_agents(cwd: Path | None = None) -> list[AgentInfo]:
    """Detect which AI agents are active in the project or home directory."""
    search_dirs = [cwd or Path.cwd(), Path.home()]
    found: list[AgentInfo] = []
    seen: set[str] = set()

    for base in search_dirs:
        for marker, name, skills_dir in _AGENT_MARKERS:
            if (base / marker).exists() and name not in seen:
                found.append(AgentInfo(name=name, skills_dir=skills_dir, marker=marker))
                seen.add(name)

    return found


def detect_primary_agent(cwd: Path | None = None) -> AgentInfo | None:
    """Return the first detected agent, or None."""
    agents = detect_agents(cwd)
    return agents[0] if agents else None
