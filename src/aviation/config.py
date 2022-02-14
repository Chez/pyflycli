"""This module provides the  PyFly config functionality."""
import typer

from pathlib import Path

from aviation.database import AsyncDatabaseHandler

from aviation.errors import *

def init_app(db_path: str) -> int:
    """Initialize the application."""
    config_code = _init_database()
    if config_code != SUCCESS:
        return config_code
    return SUCCESS

def _init_database() -> int:
    asdb = AsyncDatabaseHandler()
    try:
        db_init_error = asdb.run("is_awake")
        if db_init_error:
            typer.secho(
                "[INFO] Failed to init db.",
                fg=typer.colors.RED,
            )
            raise typer.Exit(1)
        responses = asdb.run("get_all_responses")
        typer.secho(
            f"[INFO] Successful db connection. Total Responses: {len(responses)}", fg=typer.colors.GREEN)
    except OSError:
        return DB_READ_ERROR
    return SUCCESS
