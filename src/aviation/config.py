"""This module provides the PyFly config functionality."""
import typer

from aviation.database import AsyncDatabaseHandler, DummyAsyncDatabaseHandler
from aviation.errors import *


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
        db_init_error = asdb.run("is_awake")
        if db_init_error:
            try:
                log.postgres_fail()
                dh = DummyAsyncDatabaseHandler()
                dh.run("parse_data")
                log.success_local_db()
            except:
                log.db_unhealthy()       
                raise typer.Exit(1)
        log.db_healthy()
    except OSError:
        return DB_READ_ERROR
    return SUCCESS
