
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, selectinload
from decorators import check_users
import settings
from models import Teachers, TrainingGroups, Tasks

engine = create_async_engine(settings.SQL_ALCHEMY_DB, echo=True)
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

bot = Bot(token=settings.TOKEN)
dp = Dispatcher(bot)

@dp.callback_query_handler(Text(startswith="_lesson_"))
async def choose_lesons(call: types.CallbackQuery):
    print('lessons_choose')
    t = await async_session().execute(
        select(Tasks).filter_by(id=2))
    result = t.scalar()
    with open(f"{result.name}.txt", "wb") as f:
        f.write(result.file)
    print('resultresult', result.file)
    await call.message.answer_document(open(f"{result.name}.txt", "rb"))

@dp.callback_query_handler(Text(startswith="_groups_"))
async def choose_groups(call: types.CallbackQuery):
    groups = int(call.data.replace('_groups_', ''))
    '''file_for_add = open("test.txt", "rb").read()
    file = Tasks(name='tes1t', file=file_for_add)
    file_add = OperationsDB(
        async_session,
        Object=file
    )
    await file_add.add_in_db()
    print('filefile', file)'''

    t = await async_session().execute(
        select(TrainingGroups).filter_by(id=groups).options(
            selectinload(TrainingGroups.lesson)))
    result = t.scalar()
    keyboard = types.InlineKeyboardMarkup()
    for lesson in result.lesson:
        keyboard.add(types.InlineKeyboardButton(text=lesson.name,
                                                callback_data=f"_lesson_{lesson.id}"))
    await call.message.answer("Выберите урок", reply_markup=keyboard)


@dp.callback_query_handler(Text(startswith="_teachers_"))
async def choose_teachers(call: types.CallbackQuery):
    teachers = int(call.data.replace('_teachers_', ''))
    t = await async_session().execute(
        select(Teachers).filter_by(id=teachers).options(
            selectinload(Teachers.groups)))
    result = t.scalar()
    keyboard = types.InlineKeyboardMarkup()
    for group in result.groups:
        keyboard.add(types.InlineKeyboardButton(text=group.name,
                                                callback_data=f"_groups_{group.id}"))
    await call.message.answer("Выберите группу", reply_markup=keyboard)


@dp.message_handler(commands=['start', 'help'])
@check_users
async def send_welcome(message: types.Message):
    """
    This handler will be called when client send `/start` or `/help` commands.
    """
    q = select(Teachers)
    result = await async_session().execute(q)
    answer = result.all()
    keyboard = types.InlineKeyboardMarkup()
    for i in answer:
        full_name = f"{i[0].last_name} {i[0].first_name} {i[0].middle_name}"
        keyboard.add(types.InlineKeyboardButton(text=full_name,
                                                callback_data=f"_teachers_{i[0].id}"))
    await message.answer("Выберите преподавателя", reply_markup=keyboard)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
