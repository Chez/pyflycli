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
    config_code = _init_config_file()
    if config_code != SUCCESS:
        return config_code
    database_code = _init_database(db_path)
    if database_code != SUCCESS:
        return database_code
    return SUCCESS

def _init_config_file() -> int:
    try:
        CONFIG_DIR_PATH.mkdir(exist_ok=True)
    except OSError:
        return DIR_ERROR
    try:
        CONFIG_FILE_PATH.touch(exist_ok=True)
    except OSError:
        return FILE_ERROR
    return SUCCESS

def _init_database(db_path: str) -> int:
    """
    Gets one entry from Response table.
    """
    try:
        asdb = AsyncDatabaseHandler()
        return SUCCESS if asdb.run("ping_db") else DB_READ_ERROR
    except OSError:
        return DB_READ_ERROR