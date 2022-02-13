"""This module provides the RP To-Do database functionality."""
import os
import json
from pathlib import Path
from typing import Any, Dict, List, NamedTuple
import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import select

from pyfly import DB_READ_ERROR, DB_WRITE_ERROR, JSON_ERROR, SUCCESS
from .fake_models import *


DEFAULT_DB_FILE_PATH = "/home/batman/Desktop/py/pyflycli/pyfly/default.json"


class CRUDer:
    def __init__(self) -> None:
        pass
    
    async def get_one_response(self, session):
        return await session.execute(select(Response))
                             
    
class AsyncDatabaseHandler:
    
    def __init__(self, uri: str="postgresql+asyncpg://postgres:password@localhost/foo", crud: CRUDer = CRUDer()) -> None:
        self.uri = uri
        self.engine = self.create_async_engine(self.uri, echo=True)
        self.async_session = self.get_async_session()
        self.ops = {
            "get_response" : self.get_response
        }
        self.crud = crud
        self.result = []
        
    def create_async_engine(self, uri, echo=True):
        return create_async_engine(uri, echo=echo)
        
    def get_async_session(self):
        return sessionmaker(
            self.engine, expire_on_commit=False, class_=AsyncSession
        )

    async def get_response(self):
        self.result = []
        async with self.async_session() as session:
            async with session.begin():         
                result = await self.crud.get_one_response(session)
                self.result.append(result.scalars().first())
                
        # MUST dispose     
        await self.engine.dispose()
        
    def run(self, operation):
        print(f"runninng {operation}")
        asyncio.run(self.ops[operation]()) 
        return bool(self.result)


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
