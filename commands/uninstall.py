import typer

import os
import shutil
import re
import json

from settings import VERSIONS_FILE, CONFIG_FILE, BIN_DIR, CORE_DIR, EXE_7Z

def app(
    lang_ver: str = typer.Argument(..., help="Language and Version to uninstall (language@version)")
):  
    if not re.match(r"^[a-zA-Z]+@[0-9]+\.[0-9]+\.[0-9]+$", lang_ver):
        typer.echo("Invalid command format. Expected format: language@version")
        raise typer.Exit(code=1)
    
    language, version = lang_ver.split("@")

    bin_lang_path = os.path.join(BIN_DIR, language)
    if not os.path.exists(bin_lang_path):
        typer.echo(f"No {language} folder found in {BIN_DIR}.")
        raise typer.Exit(code=1)

    lang_ver_path = os.path.join(bin_lang_path, f"{language}-{version}")
    if os.path.exists(lang_ver_path) and os.path.isdir(lang_ver_path):
        try:
            shutil.rmtree(lang_ver_path)
            typer.echo(f"Removed installation at {lang_ver_path}.")
        except Exception as e:
            typer.echo(f"Error removing directory: {e}")
            raise typer.Exit(code=1)
    else:
        typer.echo(f"No {language}-{version} folder found in {bin_lang_path}.")
        raise typer.Exit(code=1)
    
    if not os.path.exists(VERSIONS_FILE):
        typer.echo("No versions.json found.")
        raise typer.Exit(code=1)

    with open(VERSIONS_FILE, "r") as f:
        versions = json.load(f)

    if language not in versions:
        typer.echo(f"No installed versions found for language: {language}")
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
    
    typer.echo(f"Uninstalled {language}@{version} successfully.")
    