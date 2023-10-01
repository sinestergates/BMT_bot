from pydantic import BaseModel
from sqlalchemy import select
from DB_operations import OperationsDB
from models import Users


class UsersValid(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str


def check_users(func):
    async def wrapper(*args):
        from main import async_session
        result = await async_session().execute(select(Users).filter_by(id_tg=int(args[0]['from']['id'])))
        answer = result.all()
        if not answer:
            user = Users(
                id_tg=args[0]['from']['id'],
                first_name=args[0]['from']['first_name'],
                last_name=args[0]['from']['last_name'],
                username=args[0]['from']['username']
            )
            user_add = OperationsDB(
                async_session,
                Object=user
            )
            await user_add.add_in_db()
        await func(*args)
    return wrapper
