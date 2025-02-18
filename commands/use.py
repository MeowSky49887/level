import typer
import click

import os
import re
import json
import yaml
import _winapi

from pathlib import Path

from settings import VERSIONS_FILE, CONFIG_FILE, BIN_DIR, CORE_DIR, EXE_7Z
from utils.env import globalPath, localPath

def app(
    target: str = typer.Argument(..., help="Language@Version (e.g., python@3.10.5) or a full path")
):
    if not os.path.exists(CONFIG_FILE):
        typer.echo(typer.rich_utils.rich_format_error(click.ClickException("Config file not found.")))
        raise typer.Exit(code=1)

    try:
        with open(CONFIG_FILE, 'r') as f:
            config = yaml.safe_load(f)
        languages = config["languages"]
    except Exception as e:
        typer.echo(typer.rich_utils.rich_format_error(click.ClickException("Failed to read config file.")))
        raise typer.Exit(code=1)
    
    if not os.path.exists(VERSIONS_FILE):
        typer.echo(typer.rich_utils.rich_format_error(click.ClickException("No versions.json found.")))
        raise typer.Exit(code=1)

    with open(VERSIONS_FILE, "r") as f:
        versions = json.load(f)

    selected_version = None
    selected_language = None
    core_lang_path = None

    if re.match(r"^[a-zA-Z]+@[0-9]+\.[0-9]+\.[0-9]+$", target):
        language, version = target.split("@")

        if language not in versions:
            typer.echo(typer.rich_utils.rich_format_error(click.ClickException(f"No versions found for language: {language}")))
            raise typer.Exit(code=1)

        for entry in versions[language]:
            if entry["version"] == version:
                selected_version = entry["path"]
                selected_language = language
                break

        if not selected_version:
            typer.echo(typer.rich_utils.rich_format_error(click.ClickException(f"Version {version} not found for {language}.")))
            raise typer.Exit(code=1)

    else:
        target_path = os.path.abspath(target)

        found = False
        for lang, entries in versions.items():
            for entry in entries:
                if entry["path"] == target_path:
                    selected_version = entry["path"]
                    selected_language = lang
                    found = True
                    break
            if found:
                break

        if not selected_version:
            typer.echo(typer.rich_utils.rich_format_error(click.ClickException(f"Path {target_path} is not registered in versions.json.")))
            raise typer.Exit(code=1)

    core_lang_path = os.path.abspath(os.path.join(CORE_DIR, selected_language))

    if not os.path.exists(CORE_DIR):
        os.makedirs(CORE_DIR)

    if os.path.exists(core_lang_path) or os.path.islink(core_lang_path):
        os.remove(core_lang_path)

    try:
        _winapi.CreateJunction(selected_version, core_lang_path)
        typer.echo(f"Symlink created at {core_lang_path}")
    except Exception as e:
        typer.echo(typer.rich_utils.rich_format_error(click.ClickException(f"Failed to create symlink: {e}")))
        raise typer.Exit(code=1)
    
    try:
        for path in languages[selected_language]["path"]:
            exe_path = os.path.abspath(os.path.join(core_lang_path, path))
            globalPath(exe_path)
            localPath(exe_path)
    except Exception as e:
        typer.echo(typer.rich_utils.rich_format_error(click.ClickException(f"Failed to init path: {e}")))
        raise typer.Exit(code=1)
    
    typer.echo(f"Now using {selected_language}@{Path(selected_version).name}.")
