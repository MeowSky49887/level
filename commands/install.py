import typer

import os
import re
import json
import yaml

from settings import VERSIONS_FILE, CONFIG_FILE, BIN_DIR, CORE_DIR, EXE_7Z
from utils.available import availableInstaller
from utils.get import getFile

def app(
    lang_ver: str = typer.Argument(..., help="Language and Version to install (language@version)"),  
    path: str = typer.Option(BIN_DIR, "--path", "-p", help="Base install directory (default: ./bin)"),
    arch: str = typer.Option("x64", "--arch", "-a", help="Architecture to use (x64 or x86, default: x64)")
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
    
    if arch not in ["x64", "x86"]:
        typer.echo("Invalid architecture. Please specify 'x64' or 'x86'.")
        raise typer.Exit(code=1)

    if re.match(r"[a-zA-Z]+@[0-9]+\.[0-9]+\.[0-9]+", lang_ver):
        language, version = lang_ver.split("@")
        major, minor, patch = version.split(".")
    elif re.match(r"[a-zA-Z]+@[0-9]+\.[0-9]+", lang_ver):
        language, version = lang_ver.split("@")
        major, minor = version.split(".")
        patch = -1
    elif re.match(r"[a-zA-Z]+@[0-9]+", lang_ver):
        language, version = lang_ver.split("@")
        major = version
        minor, patch = -1, -1
    elif re.match(r"[a-zA-Z]+", lang_ver):
        language = lang_ver
        major, minor, patch = -1, -1, -1
    else:
        typer.echo("Invalid command format.")
        raise typer.Exit(code=1)
    
    latest, full_version = availableInstaller(language, major, minor, patch)
    
    if not latest:
        typer.echo("No matching language with specified version found.")
        raise typer.Exit(code=1)

    if arch not in latest:
        typer.echo(f"{language} does not have a {arch} version available.")
        raise typer.Exit(code=1)

    url = latest[arch]
    install_path = os.path.abspath(os.path.join(path, language, f"{language}-{full_version}"))
    label = f"Downloading {language}@{full_version}({arch})"

    typer.echo(f"Fetching file from {url}")

    getFile(url, install_path, label)
        
    try:
        exec(languages[language]["post_install"])
    except Exception as e:
        typer.echo(f"Post-installation for {language} failed: {e}")

    if not os.path.exists(VERSIONS_FILE):
        versions = {}
    else:
        with open(VERSIONS_FILE, "r") as f:
            versions = json.load(f)
    
    if language not in versions:
        versions[language] = []

    data = {"version": str(full_version), "path": os.path.abspath(install_path), "source": "level"}
    if data not in versions[language]:
        versions[language].append(data)
    
    with open(VERSIONS_FILE, "w") as f:
        json.dump(versions, f, indent=4)
    
    typer.echo(f"Updated {VERSIONS_FILE} with {language} {full_version}.")
