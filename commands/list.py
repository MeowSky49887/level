import typer
import click

import os
import json

from settings import VERSIONS_FILE, CONFIG_FILE, BIN_DIR, CORE_DIR, EXE_7Z

def app():
    if not os.path.exists(VERSIONS_FILE):
        typer.echo(typer.rich_utils.rich_format_error(click.ClickException("No versions.json found.")))
        raise typer.Exit(code=1)
    
    with open(VERSIONS_FILE, "r") as f:
        versions = json.load(f)
    
    typer.echo("Installed languages and versions:")
    for language, versions_list in versions.items():
        typer.echo(f"\n{language}:")
        for entry in versions_list:
            typer.echo(f"  - {entry['version']} (Path: {entry['path']})")
