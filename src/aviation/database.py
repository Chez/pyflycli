"""This module provides the OPyFly database functionality."""
import os
from pathlib import Path
from typing import Any, Dict, List
import asyncio
import asyncer 
import anyio

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import select

# https://github.com/tiangolo/sqlmodel/issues/189
from sqlmodel.sql.expression import Select, SelectOfScalar
SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore

from aviation.models import *
from aviation.errors import *


class CRUDer:
    
    async def get_one_response(self, session):
        async with session() as session:
            async with session.begin():         
                return await session.execute(select(Response))

    async def get_all_responses(self, session):
        async with session() as session:
            async with session.begin():
                return await session.execute(select(Response))
            
    async def get_all_flights(self, session):
        async with session() as session:
            async with session.begin():
                return await session.execute(select(DetailedFlight))
            
class AsyncDatabaseHandler:
    
    def __init__(self, uri: str="postgresql+asyncpg://postgres:password@localhost/foo", crud: CRUDer = CRUDer()) -> None:
        self.uri = uri
        self.crud = crud
        self.engine = self.create_async_engine(self.uri, echo=False)
        
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
    
    async def get_all_flights(self):
        session = self.get_async_session()
        result = await self.crud.get_all_flights(session)
        flights = result.scalars().all()
        await self.engine.dispose()
        return flights
    
    def run(self, operation):
        return asyncio.run(getattr(self, operation)())
    
    

