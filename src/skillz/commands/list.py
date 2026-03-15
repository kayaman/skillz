"""skillz list — show installed skills."""

from __future__ import annotations

import json

import typer
from rich.table import Table

from skillz.console import console, info, warning
from skillz.core.config import global_skills_dir, project_skills_dir
from skillz.core.lockfile import read_lockfile


def list_skills(
    global_only: bool = typer.Option(False, "--global", "-g", help="Show only global skills"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
) -> None:
    """List installed skills (project + global)."""
    rows: list[dict[str, str]] = []

    if not global_only:
        project_dir = project_skills_dir()
        if project_dir.exists():
            lock = read_lockfile(project_dir)
            for name, entry in lock.skills.items():
                rows.append(
                    {
                        "name": name,
                        "source": entry.source,
                        "scope": "project",
                        "installed": entry.installed_at[:10] if entry.installed_at else "",
                    }
                )

    global_dir = global_skills_dir()
    if global_dir.exists():
        lock = read_lockfile(global_dir)
        for name, entry in lock.skills.items():
            rows.append(
                {
                    "name": name,
                    "source": entry.source,
                    "scope": "global",
                    "installed": entry.installed_at[:10] if entry.installed_at else "",
                }
            )

    if not rows:
        warning("No skills installed.")
        return

    if json_output:
        console.print_json(json.dumps(rows))
        return

    table = Table(title="Installed Skills")
    table.add_column("Name", style="magenta bold")
    table.add_column("Source")
    table.add_column("Scope", style="cyan")
    table.add_column("Installed")

    for row in rows:
        table.add_row(row["name"], row["source"], row["scope"], row["installed"])

    console.print(table)
    info(f"{len(rows)} skill(s) installed")
