"""This module provides the  PyFly config functionality."""
import typer

from pathlib import Path

from aviation.database import AsyncDatabaseHandler, DummyAsyncDatabaseHandler
from aviation.errors import *

class Log:
    def good(self):
        message = "[INFO] Database status: "
        status = typer.style("good", fg=typer.colors.GREEN, bold=True)
        
    def success_local_db(self):
        message = "[INFO] Database status: "
        status = typer.style("no postgres. loaded local sqlite db", fg=typer.colors.GREEN, bold=True)
        typer.echo(message + status)

def init_app() -> int:
    """Initialize the application."""
    config_code = _init_database()
    if config_code != SUCCESS:
        return config_code
    return SUCCESS

def _init_database() -> int:
    log = Log()
    asdb = AsyncDatabaseHandler()
    try:
        message = "[INFO] Database status: "
        db_init_error = DB_READ_ERROR
        # db_init_error = asdb.run("is_awake") # DB_READ_ERROR to simulate failed PG load.
        if db_init_error:
            try:
                status = typer.style("postgres db failed.", fg=typer.colors.RED, bold=True)
                typer.echo(message + status)

                dh = DummyAsyncDatabaseHandler()
                dh.run("parse_data")
                
                log.success_local_db()
            except:
                status = typer.style("bad", fg=typer.colors.RED, bold=True)
                typer.echo(message + status)        
                raise typer.Exit(1)
        log.good()
    except OSError:
        return DB_READ_ERROR
    return SUCCESS
