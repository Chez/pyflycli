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
    
    async def get_one_response(self, session):
        async with session() as session:
            async with session.begin():         
                return await session.execute(select(Response))

    async def get_all_responses(self, session):
        async with session() as session:
            async with session.begin():
                return await session.execute(select(Response))

class AsyncDatabaseHandler:
    
    def __init__(self, uri: str="postgresql+asyncpg://postgres:password@localhost/foo", crud: CRUDer = CRUDer()) -> None:
        self.uri = uri
        self.crud = crud
        self.engine = self.create_async_engine(self.uri, echo=False)
        self.ops = {
                "is_awake" : self.is_awake,
                "get_all_responses" : self.get_all_responses    
            }
        
    def create_async_engine(self, uri, echo=True):
        return create_async_engine(uri, echo=echo)
        
    def get_async_session(self):
        return sessionmaker(
            self.engine, expire_on_commit=False, class_=AsyncSession
        )

    async def is_awake(self):
        session = self.get_async_session()
        result = await self.crud.get_one_response(session)
        await self.engine.dispose()
        return SUCCESS if result.scalars().all()[0] else DB_READ_ERROR
    
    async def get_all_responses(self):
        session = self.get_async_session()
        result = await self.crud.get_all_responses(session)
        responses = result.scalars().all()
        await self.engine.dispose()
        return responses

    def run(self, operation):
        print(f"runninng {operation}")
        result = asyncio.run(self.ops[operation]()) # must return to variable!
        return result
    
    