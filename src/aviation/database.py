"""This module provides the PyFly database functionality."""
import json
from typing import Any, Dict, List
import asyncio

import sqlalchemy
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
            
    async def get_all_detailed(self, session):
        async with session() as session:
            async with session.begin():
                return await session.execute(select(DetailedFlight))
            
    async def get_all_brief(self, session):
        async with session() as session:
            async with session.begin():
                return await session.execute(select(BriefFlight))     
            
    async def crud_create(self, session, response: Response):
        async with session() as session:
            async with session.begin():
                session.add(response)
            await session.commit()                
            return response
        
    async def crud_return(self, session):
        async with session() as session:
            async with session.begin():
                return await session.execute(select(Response))  
                   
                   
class AsyncDatabaseHandler:
    
    def __init__(self, crud: CRUDer = CRUDer()) -> None:
        self.uri = "postgresql+asyncpg://postgres:password@localhost/foo"
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
    
    async def get_all_detailed(self):
        session = self.get_async_session()
        result = await self.crud.get_all_detailed(session)
        flights = result.scalars().all()
        await self.engine.dispose()
        return flights
    
    async def get_all_brief(self):
        session = self.get_async_session()
        result = await self.crud.get_all_brief(session)
        flights = result.scalars().all()
        await self.engine.dispose()
        return flights
    
    def run(self, operation):
        return asyncio.run(getattr(self, operation)())
    
    
class DummyAsyncDatabaseHandler:
    
    def __init__(self, crud: CRUDer = CRUDer()) -> None:
        self.uri = "sqlite+aiosqlite:///./foo_two.db"
        self.crud = crud
        self.engine = self.create_async_engine(self.uri, echo=False)
    
    def create_async_engine(self, uri, echo=True):
        return create_async_engine(uri, echo=echo)

    def get_async_session(self):
        return sessionmaker(
            self.engine, expire_on_commit=False, class_=AsyncSession
        )
        
    async def create_fake_data(self, response):
        session = self.get_async_session()
        await self.create_tables()
        result = await self.crud.crud_create(session, response)
        await self.engine.dispose()
        return result
    
    async def return_fake_data(self):
        session = self.get_async_session()
        result = await self.crud.crud_return(session)
        await self.engine.dispose()
        return result
    
    async def create_tables(self):        
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.drop_all)
            await conn.run_sync(SQLModel.metadata.create_all)
            
    async def parse_data(self):        
        await self.create_tables()
        
        with open('src/aviation/dummy_data.json') as json_file:
            data = json.load(json_file)
            
        r1 = Response(
                name="controller42",
                time_created=datetime.datetime.now(),
                flights=[DetailedFlight(**flight) for flight in data["detailed_out"]],
                briefs=[BriefFlight(**flight) for flight in data["briefs_out"]]
        )  
        created = await self.create_fake_data(r1)
        returned = await self.return_fake_data()
        #print(created, returned)
    
    def run(self, operation):
        return asyncio.run(getattr(self, operation)())

