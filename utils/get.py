import typer
import click
from tqdm import tqdm

import os
import re
import subprocess

import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

from settings import VERSIONS_FILE, CONFIG_FILE, BIN_DIR, CORE_DIR, EXE_7Z

def getLink(url, regex=".*"):
    fetch = requests.get(url)
    soup = BeautifulSoup(fetch.content, 'html.parser')
    
    links = soup.find_all("a", href=True)

    return [
        urljoin(url, link['href']) for link in links
        if re.fullmatch(regex, link['href'])
    ]

def getFile(url, path, label):
    def isArchive(file_path):
        try:
            result = subprocess.run(
                [EXE_7Z, 't', file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if "Everything is Ok" in result.stdout:
                return True
            else:
                return False
        except Exception as e:
            print(f"Error occurred while running 7-Zip: {e}")
            return False

    try:
        local_file_path = os.path.abspath(os.path.join(path, "../", os.path.basename(url)))
        os.makedirs(path, exist_ok=True)

        with requests.get(url, stream=True) as response:
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))

            with open(local_file_path, "wb") as file:
                with tqdm(
                    total=total_size,
                    unit='B',
                    unit_scale=True,
                    unit_divisor=1024,
                    desc=label,
                    bar_format="{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} {rate_fmt}",
                    colour="#afebb4"
                ) as progress_bar:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            file.write(chunk)
                            progress_bar.update(len(chunk))

    except requests.RequestException as e:
        typer.echo(typer.rich_utils.rich_format_error(click.ClickException(f"Download failed: {e}")))
        raise typer.Exit(code=1)

    if os.path.exists(path) and os.listdir(path):
        typer.echo(typer.rich_utils.rich_format_error(click.ClickException(f"Installation path {path} is not empty.")))
        raise typer.Exit(code=1)

    try:
        typer.echo(f"Extracting {local_file_path}...")

        with tqdm(
            total=100,
            desc="Extracting",
            bar_format="{desc}: {percentage:3.0f}%|{bar}|",
            colour="#7db4eb"
        ) as progress_bar:
            extract_command = [
                EXE_7Z, "x",
                local_file_path,
                "-bsp1",
                f"-o{path}"
            ]
            with subprocess.Popen(extract_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as proc:
                while True:
                    line = proc.stdout.readline()
                    if not line:
                        break
                    if "%" in line:
                        try:
                            percentage = int(line.split("%")[0].strip())
                            progress_bar.n = percentage
                            progress_bar.refresh()
                        except ValueError:
                            pass
                proc.wait()

                if proc.returncode != 0:
                    typer.echo(typer.rich_utils.rich_format_error(click.ClickException(f"Extraction failed: {proc.stderr.read()}")))
                    raise typer.Exit(code=1)

            extracted_items = os.listdir(path)
            if len(extracted_items) == 1:
                sub = os.path.join(path, extracted_items[0])

                if os.path.isfile(sub) and not os.path.isdir(sub):
                    if isArchive(sub):
                        progress_bar.reset()

                        nested_extract_command = [
                            EXE_7Z, "x",
                            sub,
                            "-bsp1",
                            f"-o{path}"
                        ]
                        with subprocess.Popen(nested_extract_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as nested_proc:
                            while True:
                                line = nested_proc.stdout.readline()
                                if not line:
                                    break
                                if "%" in line:
                                    try:
                                        percentage = int(line.split("%")[0].strip())
                                        progress_bar.n = percentage
                                        progress_bar.refresh()
                                    except ValueError:
                                        pass
                            nested_proc.wait()

                            if nested_proc.returncode != 0:
                                typer.echo(typer.rich_utils.rich_format_error(click.ClickException(f"Extraction failed: {nested_proc.stderr.read()}")))
                                raise typer.Exit(code=1)

                        os.remove(sub)

        typer.echo(f"Extracted to {path}")

    except Exception as e:
        typer.echo(typer.rich_utils.rich_format_error(click.ClickException(f"Extraction failed: {e}")))
        raise typer.Exit(code=1)
    finally:
        if os.path.exists(local_file_path):
            os.remove(local_file_path)
