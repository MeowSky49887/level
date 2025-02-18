import typer

import os
import json

from settings import VERSIONS_FILE, CONFIG_FILE, BIN_DIR, CORE_DIR, EXE_7Z

def app():
    if not os.path.exists(VERSIONS_FILE):
        typer.echo("No installed versions found.")
        raise typer.Exit(code=1)
    
    with open(VERSIONS_FILE, "r") as f:
        versions = json.load(f)
    
    if not os.path.exists(VERSIONS_FILE):
        typer.echo("No versions.json found.")
        raise typer.Exit(code=1)
    
    typer.echo("Installed languages and versions:")
    for language, versions_list in versions.items():
        typer.echo(f"\n{language}:")
        for entry in versions_list:
            typer.echo(f"  - {entry['version']} (Path: {entry['path']})")
