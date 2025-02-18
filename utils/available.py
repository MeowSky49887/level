import typer

import os
import re
import yaml

import validators
from packaging.version import Version

from settings import VERSIONS_FILE, CONFIG_FILE, BIN_DIR, CORE_DIR, EXE_7Z
from utils.get import getLink

def availableInstaller(language, major, minor, patch):
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
        
    if language in languages.keys():
        base_urls = languages[language]["versions_url"]
        pattern = languages[language]["versions_pattern"]["patch"].format(major=major, minor=minor, patch=patch) if patch != -1 else \
                  languages[language]["versions_pattern"]["minor"].format(major=major, minor=minor) if minor != -1 else \
                  languages[language]["versions_pattern"]["major"].format(major=major) if major != -1 else \
                  languages[language]["versions_pattern"]["none"]
    else:
        raise ValueError("Unsupported language")

    versions = []
    for url in base_urls:
        versions += getLink(url, pattern)

    version_list = sorted(
        [Version(match.group(1)) for version in versions if (match := re.search(r"(\d+\.\d+\.\d+)", version))],
        reverse=True
    )

    if not version_list:
        return None

    for latest_version in version_list:
        download_urls = languages[language]["download_url"]
        x64_pattern = languages[language]["download_pattern"]["x64"].format(latest_version=latest_version)
        x86_pattern = languages[language]["download_pattern"]["x86"].format(latest_version=latest_version)
        x64_file = []
        x86_file = []
        for url in download_urls:
            x64_file += getLink(url.format(latest_version=latest_version), x64_pattern)
            x86_file += getLink(url.format(latest_version=latest_version), x86_pattern)
        
        available_links = {}
        if len(x64_file) > 0 and validators.url(x64_file[0]):
            available_links["x64"] = x64_file[0]
        if len(x86_file) > 0 and validators.url(x86_file[0]):
            available_links["x86"] = x86_file[0]

        if available_links:
            return available_links, latest_version

    return None
