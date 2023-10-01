from sqlalchemy import Column, ForeignKey, Date, Boolean, DateTime, func, LargeBinary, BigInteger
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.testing.schema import Table


Base = declarative_base()

ItemTeachersLesson = Table('ItemTeachersLessons', Base.metadata,
                           Column('id', Integer, primary_key=True),
                           Column('TeachersId', Integer, ForeignKey('teachers.id')),
                           Column('LessonsId', Integer, ForeignKey('lessons.id')),
                           Column('TrainingGroupsId', Integer, ForeignKey('training_groups.id')),
                           Column('endDate', Date))

ItemLessonTask = Table('ItemLessonTask', Base.metadata,
                       Column('id', Integer, primary_key=True),
                       Column('TasksId', Integer, ForeignKey('tasks.id')),
                       Column('LessonsId', Integer, ForeignKey('lessons.id'))
                       )


class Tasks(Base):
    __tablename__ = "tasks"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String, unique=False)
    lesson_id = relationship('Lessons', secondary=ItemLessonTask, back_populates="tasks")
    file = Column(BYTEA)


class Lessons(Base):
    __tablename__ = "lessons"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String, unique=False)
    description = Column(String, unique=False)
    teachers = relationship('Teachers', secondary=ItemTeachersLesson, back_populates="lesson")
    tasks = relationship('Tasks', secondary=ItemLessonTask, back_populates="lesson_id")


class TrainingGroups(Base):
    __tablename__ = "training_groups"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String, unique=False)
    lesson = relationship('Lessons', secondary=ItemTeachersLesson, backref='training_groups')
    teachers = relationship('Teachers', secondary=ItemTeachersLesson, back_populates="groups")


class Teachers(Base):
    __tablename__ = "teachers"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    first_name = Column(String, unique=False)
    last_name = Column(String, unique=False)
    middle_name = Column(String, unique=False)
    lesson = relationship('Lessons', secondary=ItemTeachersLesson, back_populates="teachers")
    groups = relationship('TrainingGroups', secondary=ItemTeachersLesson, back_populates="teachers")


class Users(Base):
    __tablename__ = "Users"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    id_tg = Column(BigInteger, unique=True)
    first_name = Column(String, unique=False)
    last_name = Column(String, unique=False)
    middle_name = Column(String, unique=False)
    username = Column(String, unique=True)
    is_admin = Column(Boolean, unique=False, default=False)
    is_active = Column(Boolean, unique=False, default=True)
    last_login = Column(DateTime(timezone=True), )
