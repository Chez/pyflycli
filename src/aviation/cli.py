"""This module provides the Pyfly CLI."""
from typing import List, Optional

import typer

from rich.console import Console
from rich.table import Table

from aviation.errors import *
from aviation.config import *
from aviation.database import *

console = Console()

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
    """Initialize the Pyfly app."""
    app_init_error = init_app(db_path)
    if app_init_error:
        typer.secho(
            f'[INFO] Creating app failed with "{DB_READ_ERROR}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho("[INFO] Application initialized.", fg=typer.colors.GREEN)


@app.command(name="list")
def list_all() -> None:
    """List all to-dos."""
    handler =  AsyncDatabaseHandler()
    all_responses = handler.run("get_all_responses")
    if len(all_responses) == 0:
        typer.secho(
            "There are no Response in the DB yet", fg=typer.colors.RED
        )
        raise typer.Exit()
    
    console.print("[bold magenta]Todos[/bold magenta]!", "💻")

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=6)
    table.add_column("Todo", min_width=20)
    table.add_column("Category", min_width=12, justify="right")
    table.add_column("Done", min_width=12, justify="right")
    
    
    console.print(table)



    # typer.secho("\nto-do list:\n", fg=typer.colors.BLUE, bold=True)
    # columns = (
    #     "ID.  ",
    #     "| Priority  ",
    #     "| Done  ",
    #     "| Description  ",
    # )
    # headers = "".join(columns)
    # typer.secho(headers, fg=typer.colors.BLUE, bold=True)
    # typer.secho("-" * len(headers), fg=typer.colors.BLUE)
    # for id, todo in enumerate(todo_list, 1):
    #     desc, priority, done = todo.values()
    #     typer.secho(
    #         f"{id}{(len(columns[0]) - len(str(id))) * ' '}"
    #         f"| ({priority}){(len(columns[1]) - len(str(priority)) - 4) * ' '}"
    #         f"| {done}{(len(columns[2]) - len(str(done)) - 2) * ' '}"
    #         f"| {desc}",
    #         fg=typer.colors.BLUE,
    #     )
    # typer.secho("-" * len(headers) + "\n", fg=typer.colors.BLUE)



# @app.command(name="list")
# def list_all() -> None:
#     """List all to-dos."""
#     todoer = get_todoer()
#     todo_list = todoer.get_todo_list()
#     if len(todo_list) == 0:
#         typer.secho(
#             "There are no tasks in the to-do list yet", fg=typer.colors.RED
#         )
#         raise typer.Exit()
#     typer.secho("\nto-do list:\n", fg=typer.colors.BLUE, bold=True)
#     columns = (
#         "ID.  ",
#         "| Priority  ",
#         "| Done  ",
#         "| Description  ",
#     )
#     headers = "".join(columns)
#     typer.secho(headers, fg=typer.colors.BLUE, bold=True)
#     typer.secho("-" * len(headers), fg=typer.colors.BLUE)
#     for id, todo in enumerate(todo_list, 1):
#         desc, priority, done = todo.values()
#         typer.secho(
#             f"{id}{(len(columns[0]) - len(str(id))) * ' '}"
#             f"| ({priority}){(len(columns[1]) - len(str(priority)) - 4) * ' '}"
#             f"| {done}{(len(columns[2]) - len(str(done)) - 2) * ' '}"
#             f"| {desc}",
#             fg=typer.colors.BLUE,
#         )
#     typer.secho("-" * len(headers) + "\n", fg=typer.colors.BLUE)
