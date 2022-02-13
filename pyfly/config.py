"""This module provides the RP To-Do config functionality."""
import configparser
from pathlib import Path

import typer

from pyfly import DB_READ_ERROR, DB_WRITE_ERROR, DIR_ERROR, FILE_ERROR, SUCCESS, __app_name__

CONFIG_DIR_PATH = Path(typer.get_app_dir(__app_name__))
CONFIG_FILE_PATH = CONFIG_DIR_PATH / "config.ini"

from pyfly.database import AsyncDatabaseHandler


def init_app(db_path: str) -> int:
    """Initialize the application."""
    config_code = _init_database()
    if config_code != SUCCESS:
        return config_code
    return SUCCESS

def _init_database() -> int:
    """Initialize DB by getting one entry from Response table."""
    asdb = AsyncDatabaseHandler()
    try:
        response = asdb.run("get_response")
        if not response:
            typer.secho(
                "Connection exists and tables have been created -- but database is empty",
                fg=typer.colors.RED,
            )
    except OSError:
        return DB_READ_ERROR
    return SUCCESS