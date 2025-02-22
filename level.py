import typer

from commands import install, uninstall, use, list, add, remove

app = typer.Typer()

app.command(name="install", help="Install language at version to bin or specified path.")(install.app)
app.command(name="uninstall", help="Uninstall language at version from bin.")(uninstall.app)
app.command(name="use", help="Use a specific language version or path by creating a symlink.")(use.app)
app.command(name="list", help="List installed language and version from versions.json.")(list.app)
app.command(name="add", help="Add an external path to versions.json.")(add.app)
app.command(name="remove", help="Remove a specific language at version or a external path from versions.json.")(remove.app)

if __name__ == "__main__":
    app()
