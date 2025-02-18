import typer

import os
import re
import subprocess
import json
import yaml

from settings import VERSIONS_FILE, CONFIG_FILE, BIN_DIR, CORE_DIR, EXE_7Z

def app(
    path: str = typer.Argument(..., help="Path to add (must contain node, python, or php executable)")
):
    if not os.path.exists(CONFIG_FILE):
        typer.echo("Config file not found.")
        raise typer.Exit(code=1)

    try:
        with open(CONFIG_FILE, 'r') as f:
            config = yaml.safe_load(f)
        languages = config["languages"]
    except Exception as e:
        typer.echo(f"Failed to read config file at {CONFIG_FILE}.")
        raise typer.Exit(code=1)
    
    abs_path = os.path.abspath(path)

    if not os.path.exists(abs_path):
        typer.echo(f"The specified path does not exist: {abs_path}")
        raise typer.Exit(code=1)

    detected_lang = None
    detected_version = None
    exe_path = None

    for lang in languages:
        if os.path.isfile(os.path.join(abs_path, languages[lang]["file"])):
            detected_lang = lang

    if not detected_lang:
        typer.echo("No recognized language executable (node.exe, python.exe, php.exe) found in the given path.")
        raise typer.Exit(code=1)

    try:
        exe_path = os.path.join(abs_path, languages[detected_lang]["file"])
        command = languages[detected_lang]["version_command"]
        pattern = languages[detected_lang]["version_pattern"]

        result = subprocess.run([exe_path, command], capture_output=True, text=True, check=True)
        output = result.stdout.strip() or result.stderr.strip()
        detected_version = re.search(pattern, output).group(1)
    except Exception as e:
        typer.echo(f"Error detecting version: {e}")
        raise typer.Exit(code=1)

    if not detected_version:
        typer.echo("Unable to extract version from the executable.")
        raise typer.Exit(code=1)

    if not os.path.exists(VERSIONS_FILE):
        versions = {}
    else:
        with open(VERSIONS_FILE, "r") as f:
            versions = json.load(f)

    if detected_lang not in versions:
        versions[detected_lang] = []

    new_entry = {
        "version": detected_version,
        "path": abs_path,
        "source": "external"
    }

    if new_entry not in versions[detected_lang]:
        versions[detected_lang].append(new_entry)

    with open(VERSIONS_FILE, "w") as f:
        json.dump(versions, f, indent=4)

    typer.echo(f"Added {detected_lang}@{detected_version} with path: {abs_path}")
    