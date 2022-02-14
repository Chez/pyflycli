"""This module provides the Pyfly CLI."""
from typing import List, Optional

import typer

(
    SUCCESS,
    DIR_ERROR,
    FILE_ERROR,
    DB_READ_ERROR,
    DB_WRITE_ERROR,
    JSON_ERROR,
    ID_ERROR
) = range(7)

ERRORS = {
    DIR_ERROR: "config directory error",
    FILE_ERROR: "config file error",
    DB_READ_ERROR: "database read error",
    DB_WRITE_ERROR: "database write error",
    ID_ERROR: "to-do id error",
}
from .config import *
from .database import *

app = typer.Typer()

@app.command()
def init(
    db_path: str = typer.Option(
        str(DEFAULT_DB_FILE_PATH),
        "--db-path",
        "-db",
        prompt="to-do database location?",
    ),
) -> None:  # sourcery skip: use-named-expression
    """Initialize the Pyfly database."""
    app_init_error = init_app(db_path)
    if app_init_error:
        typer.secho(
            f'[INFO] Creating app failed with "{DB_READ_ERROR}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho("[INFO] Application initialized.", fg=typer.colors.GREEN)

# def get_todoer() -> rptodo.Todoer:
#     if config.CONFIG_FILE_PATH.exists():
#         db_path = database.get_database_path(config.CONFIG_FILE_PATH)
#     else:
#         typer.secho(
#             'Config file not found. Please, run "rptodo init"',
#             fg=typer.colors.RED,
#         )
#         raise typer.Exit(1)
#     if db_path.exists():
#         return rptodo.Todoer(db_path)
#     else:
#         typer.secho(
#             'Database not found. Please, run "rptodo init"',
#             fg=typer.colors.RED,
#         )
#         raise typer.Exit(1)

@app.command(name="list")
def list_all() -> None:
    """List all to-dos."""
    todoer = get_todoer()
    todo_list = todoer.get_todo_list()
    if len(todo_list) == 0:
        typer.secho(
            "There are no tasks in the to-do list yet", fg=typer.colors.RED
        )
        raise typer.Exit()
    typer.secho("\nto-do list:\n", fg=typer.colors.BLUE, bold=True)
    columns = (
        "ID.  ",
        "| Priority  ",
        "| Done  ",
        "| Description  ",
    )
    headers = "".join(columns)
    typer.secho(headers, fg=typer.colors.BLUE, bold=True)
    typer.secho("-" * len(headers), fg=typer.colors.BLUE)
    for id, todo in enumerate(todo_list, 1):
        desc, priority, done = todo.values()
        typer.secho(
            f"{id}{(len(columns[0]) - len(str(id))) * ' '}"
            f"| ({priority}){(len(columns[1]) - len(str(priority)) - 4) * ' '}"
            f"| {done}{(len(columns[2]) - len(str(done)) - 2) * ' '}"
            f"| {desc}",
            fg=typer.colors.BLUE,
        )
    typer.secho("-" * len(headers) + "\n", fg=typer.colors.BLUE)

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return