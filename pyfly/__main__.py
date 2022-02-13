"""RP To-Do entry point script."""

from pyfly import cli, __app_name__

import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from sqlmodel import create_engine, SQLModel, Session, Field, select

from .fake_models import *

class AsyncDatabase:
    
    async def async_main(self):
        engine = create_async_engine(
            "postgresql+asyncpg://postgres:password@localhost/foo",
            echo=True,
        )
        print(engine)
        # async with engine.begin() as conn:
        #     await conn.run_sync(SQLModel.metadata.drop_all)
        #     await conn.run_sync(SQLModel.metadata.create_all)

        # expire_on_commit=False will prevent attributes from being expired
        # after commit.
        async_session = sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )

        async with async_session() as session:
            async with session.begin():
                result = await session.execute(select(Response))
                r = result.scalars().all()
                print(r)
                # stmt = select(A).options(selectinload(A.bs)
                # result = await session.execute(stmt)
        
        # MUST dispose     
        await engine.dispose()

    def run(self):
        print("running")
        return asyncio.run(self.async_main()) 


def main():
    print("starting main..")
    cli.app(prog_name=__app_name__)


if __name__ == "__main__":
    asdb = AsyncDatabase()
    asdb.run()
    
    main()