from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker


class OperationsDB:
    def __init__(self, async_session: sessionmaker, Object):
        self.object = Object
        self.async_session = async_session

    async def add_in_db(self):
        async with self.async_session() as session:
            try:
                async with session.begin():
                    session.add(self.object)
                    await session.flush()
                    await session.refresh(self.object)
            except SQLAlchemyError as e:
                error = str(e.__cause__)
                print('Error add in db', error)
                
                
"""class OperationsDB:
    def __init__(self, async_session: sessionmaker, Object):
        self.object = Object
        self.async_session = async_session

    async def add_in_db(self) -> None:
        async with self.async_session() as session:
            try:
                async with session.begin():
                    session.add(self.object)
                    await session.flush()
                    await session.refresh(self.object)
            except SQLAlchemyError as e:
                error = str(e.__cause__)
                print('Error add in db', error)

    async def get_elem_by_id(self, _id: int) -> None:
        result = await self.async_session().execute(
            select(self.object).filter_by(
                id=_id
            )
        )
        answer = result.all()
        return answer

    async def get_all_elements(self) -> None:
        result = await self.async_session().execute(
            select(self.object)
        )
        answer = result.all()
        return answer"""
