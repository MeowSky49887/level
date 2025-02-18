import typer

import subprocess

def globalPath(target):
    try:
        get_script = """
        [System.Environment]::GetEnvironmentVariable(
            'Path', 
            [System.EnvironmentVariableTarget]::User)
        """

        current_path = subprocess.check_output(
            ["powershell", "-Command", get_script],
            stderr=subprocess.STDOUT
        ).decode("utf-8").strip()

        if target not in current_path.split(";"):
            if current_path:
                new_path = current_path + ";" + target
            else:
                new_path = target

            set_script = f"""
            [System.Environment]::SetEnvironmentVariable(
                'Path', 
                '{new_path}',
                [System.EnvironmentVariableTarget]::User)
            """

            subprocess.check_call(
                ["powershell", "-Command", set_script],
                stderr=subprocess.STDOUT
            )

        typer.echo(f"Add path to global env successfully: {target}")
    except subprocess.CalledProcessError as e:
        typer.echo(f"Error occurred: {e.output.decode('utf-8')}")
        raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f"An unexpected error occurred: {str(e)}")
        raise typer.Exit(code=1)
    
def localPath(target):
    try:
        get_script = "$Env:Path"

        current_path = subprocess.check_output(
            ["powershell", "-Command", get_script],
            stderr=subprocess.STDOUT
        ).decode("utf-8").strip()

        if target not in current_path.split(";"):
            if current_path:
                new_path = current_path + ";" + target
            else:
                new_path = target

            set_script = f"$Env:Path = '{new_path}'"

            subprocess.check_call(
                ["powershell", "-Command", set_script],
                stderr=subprocess.STDOUT
            )

        typer.echo(f"Add path to local env successfully: {target}")
    except subprocess.CalledProcessError as e:
        typer.echo(f"Error occurred: {e.output.decode('utf-8')}")
        raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f"An unexpected error occurred: {str(e)}")
        raise typer.Exit(code=1)