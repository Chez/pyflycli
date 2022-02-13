"""This module provides the RP To-Do database functionality."""
import os
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from sqlmodel import create_engine, SQLModel, Session, select

import asyncio

import configparser
import json
from pathlib import Path
from typing import Any, Dict, List, NamedTuple

from pyfly import DB_READ_ERROR, DB_WRITE_ERROR, JSON_ERROR, SUCCESS

from .fake_models import *


DEFAULT_DB_FILE_PATH = "/home/batman/Desktop/py/pyflycli/pyfly/default.json"


class AsyncDatabaseHandler:
    
    def __init__(self, uri: str="postgresql+asyncpg://postgres:password@localhost/foo") -> None:
        self.uri = uri
        self.engine = create_async_engine(self.uri, echo=True)


    async def create_tables(self):        
        """
        NOT BEING USED YET BC PULLING DATA FROM EXISTING FLIGHT DB. MIGHT NOT NEED THIS AT ALL ACTUALLY.
        """
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.drop_all)
            await conn.run_sync(SQLModel.metadata.create_all)
    
    async def async_main(self):
        async_session = sessionmaker(
            self.engine, expire_on_commit=False, class_=AsyncSession
        )

        async with async_session() as session:
            async with session.begin():
                result = await session.execute(select(Response))
                r = result.scalars().all()
                print(r)
        
        # MUST dispose     
        await self.engine.dispose()

    def run(self):
        print("running")
        return asyncio.run(self.async_main()) 
    

def get_database_path(config_file: Path) -> Path:
    """Return the current path to the to-do database."""
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return Path(config_parser["General"]["database"])
    
def init_database(db_path: Path) -> int:
    """Create the to-do database."""
    try:
        db_path.write_text("[]")  # Empty to-do list
        return SUCCESS
    except OSError:
        return DB_WRITE_ERROR

class DBResponse(NamedTuple):
    todo_list: List[Dict[str, Any]]
    error: int

    
class DatabaseHandler:
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path

    def read_todos(self) -> DBResponse:
        try:
            with self._db_path.open("r") as db:
                try:
                    return DBResponse(json.load(db), SUCCESS)
                except json.JSONDecodeError:  # Catch wrong JSON format
                    return DBResponse([], JSON_ERROR)
        except OSError:  # Catch file IO problems
            return DBResponse([], DB_READ_ERROR)

    def write_todos(self, todo_list: List[Dict[str, Any]]) -> DBResponse:
        try:
            with self._db_path.open("w") as db:
                json.dump(todo_list, db, indent=4)
            return DBResponse(todo_list, SUCCESS)
        except OSError:  # Catch file IO problems
            return DBResponse(todo_list, DB_WRITE_ERROR)
