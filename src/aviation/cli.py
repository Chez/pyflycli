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
def init():
    """Initialize the Pyfly app."""
    message = "[INFO] Application status: "
    app_init_error = init_app()
    if app_init_error:
        status = typer.style("bad", fg=typer.colors.RED, bold=True)
        typer.echo(message + status)
        raise typer.Exit(1)
    status = typer.style("good", fg=typer.colors.GREEN, bold=True)
    typer.echo(message + status)

@app.command(name="responses")
def list_all_responses() -> None:
    """List all Responses."""
    handler =  AsyncDatabaseHandler()
    all_responses = handler.run("get_all_responses")
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
        is_most_recent = '✅' if response.id == all_responses[-1].id else '❌'
        table.add_row(str(response.id), f'[{c}]{response.time_created}[/{c}]', is_most_recent) 
    
    console.print(table)
  
@app.command(name="flights")
def list_all_flights() -> None:
    """List all DetailedFlights."""
    handler =  AsyncDatabaseHandler()
    all_flights = handler.run("get_all_flights")
    if len(all_flights) == 0:
        typer.secho(
            "There are no Flights in the DB yet", fg=typer.colors.RED
        )
        raise typer.Exit()
    
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



