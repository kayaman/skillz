"""skillz find — search GitHub for repos containing SKILL.md."""

from __future__ import annotations

import httpx
import typer
from rich.table import Table

from skillz.console import console, error, info, warning


def find(
    query: str = typer.Argument(help="Search query (e.g. 'react testing', 'deploy')"),
    limit: int = typer.Option(10, "--limit", "-n", help="Max results to show"),
) -> None:
    """Search GitHub for repos containing agent skills."""
    search_query = f"SKILL.md in:path {query}"
    url = "https://api.github.com/search/code"
    params = {"q": search_query, "per_page": min(limit, 30)}
    headers = {"Accept": "application/vnd.github.v3+json"}

    info(f"Searching GitHub for skills matching '{query}'...")

    try:
        resp = httpx.get(url, params=params, headers=headers, timeout=15)
    except httpx.HTTPError as exc:
        error(f"GitHub API request failed: {exc}")
        raise typer.Exit(1) from None

    if resp.status_code == 403:
        warning("GitHub API rate limit reached. Try again later or set GITHUB_TOKEN.")
        raise typer.Exit(1)

    if resp.status_code != 200:
        error(f"GitHub API returned {resp.status_code}: {resp.text[:200]}")
        raise typer.Exit(1)

    data = resp.json()
    items = data.get("items", [])

    if not items:
        warning(f"No skills found matching '{query}'.")
        return

    seen: set[str] = set()
    table = Table(title=f"Skills matching '{query}'")
    table.add_column("Install with", style="green")
    table.add_column("Repository")
    table.add_column("Path")

    for item in items[:limit]:
        repo_full = item["repository"]["full_name"]
        path = item["path"]

        parts = path.split("/")
        skill_name = ""
        for i, part in enumerate(parts):
            if part == "SKILL.md" and i > 0:
                skill_name = parts[i - 1]
                break

        if not skill_name or skill_name in seen:
            continue
        seen.add(f"{repo_full}@{skill_name}")

        install_cmd = f"skillz add {repo_full}@{skill_name}"
        table.add_row(install_cmd, repo_full, "/".join(parts[:-1]))

    if table.row_count == 0:
        warning("Found results but couldn't extract skill names.")
        return

    console.print(table)
    info("Install with: skillz add <source>")
