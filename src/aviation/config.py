"""This module provides the  PyFly config functionality."""
import typer

from pathlib import Path

from aviation.database import AsyncDatabaseHandler, DummyAsyncDatabaseHandler
from aviation.errors import *


def init_app() -> int:
    """Initialize the application."""
    config_code = _init_database()
    if config_code != SUCCESS:
        return config_code
    return SUCCESS

def _init_database() -> int:
    asdb = AsyncDatabaseHandler()
    try:
        message = "[INFO] Database status: "
        db_init_error = DB_READ_ERROR
        db_init_error = asdb.run("is_awake") # DB_READ_ERROR to simulate failed PG load.
        if db_init_error:
            try:
                status = typer.style("[INFO] PG DB failed.", fg=typer.colors.RED, bold=True)
                typer.echo(message + status)

                dh = DummyAsyncDatabaseHandler()
                dh.run("parse_data")
                status = typer.style("[INFO] Success local DB.", fg=typer.colors.GREEN, bold=True)
                typer.echo(message + status)
            except:
                status = typer.style("bad", fg=typer.colors.RED, bold=True)
                typer.echo(message + status)        
                raise typer.Exit(1)
        status = typer.style("good", fg=typer.colors.GREEN, bold=True)
        typer.echo(message + status)
    except OSError:
        return DB_READ_ERROR
    return SUCCESS