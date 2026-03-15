"""skillz add — install a skill from GitHub or local path."""

from __future__ import annotations

import typer

from skillz.console import error, info, success
from skillz.core.agents import detect_primary_agent
from skillz.core.git import cleanup_temp, fetch_skill
from skillz.core.installer import install_skill
from skillz.core.source_parser import parse_source
from skillz.models import SourceType


def add(
    source: str = typer.Argument(help="Skill source: owner/repo@skill, owner/repo, or local path"),
    global_install: bool = typer.Option(
        False, "--global", "-g", help="Install to ~/.agents/skills/"
    ),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompt"),
) -> None:
    """Install a skill from GitHub or a local path."""
    try:
        parsed = parse_source(source)
    except ValueError as e:
        error(str(e))
        raise typer.Exit(1) from None

    agent = detect_primary_agent()
    if agent:
        info(f"Detected agent: {agent.name}")

    scope = "globally (~/.agents/skills/)" if global_install else "to project (.agents/skills/)"
    info(f"Installing {parsed.display_name} {scope}")

    if not yes:
        typer.confirm("Proceed?", default=True, abort=True)

    if parsed.source_type == SourceType.LOCAL:
        if parsed.local_path is None or not parsed.local_path.is_dir():
            error(f"Local path does not exist: {parsed.local_path}")
            raise typer.Exit(1)
        installed = install_skill(parsed.local_path, parsed, global_install=global_install)
    else:
        tmp_path = fetch_skill(parsed)
        try:
            installed = install_skill(tmp_path, parsed, global_install=global_install)
        finally:
            cleanup_temp(tmp_path)

    if installed:
        success(f"Installed {len(installed)} skill(s): {', '.join(installed)}")
