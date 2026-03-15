"""Rich console output helpers."""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.theme import Theme

theme = Theme(
    {
        "info": "cyan",
        "success": "bold green",
        "warning": "bold yellow",
        "error": "bold red",
        "skill": "bold magenta",
    }
)

console = Console(theme=theme)
err_console = Console(stderr=True, theme=theme)


def info(message: str) -> None:
    console.print(f"[info]ℹ[/info] {message}")


def success(message: str) -> None:
    console.print(f"[success]✓[/success] {message}")


def warning(message: str) -> None:
    err_console.print(f"[warning]⚠[/warning] {message}")


def error(message: str) -> None:
    err_console.print(f"[error]✗[/error] {message}")


def skill_panel(name: str, description: str) -> None:
    console.print(Panel(description, title=f"[skill]{name}[/skill]", border_style="magenta"))
