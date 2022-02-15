"""This module provides the Pyfly CLI."""
import time
from typing import List, Optional
from webbrowser import get
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
    """List all responses flights."""
    handler =  AsyncDatabaseHandler()
    all_responses = handler.run("get_all_responses")
    all_flights = handler.run("get_all_flights")
    if len(all_responses) == 0:
        typer.secho(
            "There are no Response in the DB yet", fg=typer.colors.RED
        )
        raise typer.Exit()
    
    console.print("\n[bold green]Responses[/bold green]!", "✈")
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("id #", style="dim", width=6)
    table.add_column("Time Aquired", min_width=20)
    table.add_column("Most Recent", min_width=12, justify="right")
   
    limit = 10
    for response in all_responses[::-1][:limit]:
        c = "green" if response.id == all_responses[-1].id else "white"
        is_done_str = '✅' if response.id == all_responses[-1].id else '❌'
        table.add_row(str(response.id), f'[{c}]{response.time_created}[/{c}]', is_done_str) 
    
    console.print(table)
  

    console.print("\n[bold green]Flights[/bold green]!", "✈")
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("id", style="dim", width=6)
    table.add_column("response_id", width=12)
    table.add_column("identification", min_width=6)
    table.add_column("airplane_name", min_width=20)
    table.add_column("airplane_code", min_width=6, justify="right")

    limit = 10
    for flight in all_flights[::-1][:limit]:
        c = "white"
        table.add_row(f'[{c}]{flight.id}[/{c}]', f'[green]{flight.response_id}[/green]', f'[{c}]{flight.identification}[/{c}]', f'[{c}]{flight.airline_name}[/{c}]',  f'[{c}]{flight.airplane_code}[/{c}]') 
        
    console.print(table)



