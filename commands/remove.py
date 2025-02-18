import typer

import os
import re
import json

from settings import VERSIONS_FILE, CONFIG_FILE, BIN_DIR, CORE_DIR, EXE_7Z

def app(
    target: str = typer.Argument(..., help="Language and Version (language@version) or valid full path to remove")
):
    if not os.path.exists(VERSIONS_FILE):
        typer.echo("No versions.json found.")
        raise typer.Exit(code=1)

    with open(VERSIONS_FILE, "r") as f:
        versions = json.load(f)

    if re.match(r"^[a-zA-Z]+@[0-9]+\.[0-9]+\.[0-9]+$", target):
        language, version = target.split("@")

        if language not in versions:
            typer.echo(f"No installed versions found for {language}.")
            raise typer.Exit(code=1)

        new_versions_list = [entry for entry in versions[language] if entry["version"] != version]

        if len(new_versions_list) == len(versions[language]):
            typer.echo(f"Version {version} not found for {language}.")
            raise typer.Exit(code=1)

        versions[language] = new_versions_list
        if not versions[language]:  
            del versions[language]

        with open(VERSIONS_FILE, "w") as f:
            json.dump(versions, f, indent=4)

        typer.echo(f"Removed {language}@{version} from versions.json.")
    else:
        try:
            target_path = os.path.abspath(target)
        except Exception:
            typer.echo("Invalid path format.")
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
            