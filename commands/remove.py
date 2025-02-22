import typer
import click

import os
import re
import json

from settings import VERSIONS_FILE, CONFIG_FILE, BIN_DIR, CORE_DIR, EXE_7Z

def app(
    path: str = typer.Argument(..., help="Valid full path to remove")
):
    if not os.path.exists(VERSIONS_FILE):
        typer.echo(typer.rich_utils.rich_format_error(click.ClickException("No versions.json found.")))
        raise typer.Exit(code=1)

    with open(VERSIONS_FILE, "r") as f:
        versions = json.load(f)

    target_path = os.path.abspath(path)

    if not os.path.exists(target_path):
        typer.echo(typer.rich_utils.rich_format_error(click.ClickException(f"The specified path does not exist: {target_path}")))
        raise typer.Exit(code=1)

    removed = False

    for language, entries in list(versions.items()):
        new_entries = [entry for entry in entries if os.path.abspath(entry["path"]) != target_path]
        if len(new_entries) != len(entries):
            versions[language] = new_entries
            removed = True

        if not versions[language]:  
            del versions[language]

    if removed:
        with open(VERSIONS_FILE, "w") as f:
            json.dump(versions, f, indent=4)
        typer.echo(f"Removed path {target_path} from versions.json.")
    else:
        typer.echo(f"Path {target_path} not found in versions.json.")
            