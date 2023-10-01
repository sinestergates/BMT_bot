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

                
                
