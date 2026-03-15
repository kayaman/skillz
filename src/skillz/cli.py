"""Skillz CLI — Agent skills package manager."""

from __future__ import annotations

import typer

from skillz import __version__
from skillz.commands.add import add
from skillz.commands.find import find
from skillz.commands.init import init
from skillz.commands.list import list_skills
from skillz.commands.remove import remove
from skillz.commands.update import update

app = typer.Typer(
    name="skillz",
    help="Agent skills package manager — install, manage, and discover AI agent skills.",
    no_args_is_help=True,
)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"skillz {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        False, "--version", "-V", callback=_version_callback, is_eager=True, help="Show version"
    ),
) -> None:
    """Skillz — Agent skills package manager."""


app.command(name="add")(add)
app.command(name="list")(list_skills)
app.command(name="ls")(list_skills)
app.command(name="remove")(remove)
app.command(name="rm")(remove)
app.command(name="update")(update)
app.command(name="init")(init)
app.command(name="find")(find)
