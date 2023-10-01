"""add table init

Revision ID: ffe393be5ece
Revises: 
Create Date: 2023-08-14 11:14:24.111136

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'ffe393be5ece'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('id_tg', sa.Integer(), nullable=True),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('middle_name', sa.String(), nullable=True),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('last_login', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id_tg'),
    sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_Users_id'), 'Users', ['id'], unique=False)
    op.create_table('lessons',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_lessons_id'), 'lessons', ['id'], unique=False)
    op.create_table('tasks',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('file', postgresql.BYTEA(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tasks_id'), 'tasks', ['id'], unique=False)
    op.create_table('teachers',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('middle_name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_teachers_id'), 'teachers', ['id'], unique=False)
    op.create_table('training_groups',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_training_groups_id'), 'training_groups', ['id'], unique=False)
    op.create_table('ItemLessonTask',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('TasksId', sa.Integer(), nullable=True),
    sa.Column('LessonsId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['LessonsId'], ['lessons.id'], ),
    sa.ForeignKeyConstraint(['TasksId'], ['tasks.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ItemTeachersLessons',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('TeachersId', sa.Integer(), nullable=True),
    sa.Column('LessonsId', sa.Integer(), nullable=True),
    sa.Column('TrainingGroupsId', sa.Integer(), nullable=True),
    sa.Column('endDate', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['LessonsId'], ['lessons.id'], ),
    sa.ForeignKeyConstraint(['TeachersId'], ['teachers.id'], ),
    sa.ForeignKeyConstraint(['TrainingGroupsId'], ['training_groups.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ItemTeachersLessons')
    op.drop_table('ItemLessonTask')
    op.drop_index(op.f('ix_training_groups_id'), table_name='training_groups')
    op.drop_table('training_groups')
    op.drop_index(op.f('ix_teachers_id'), table_name='teachers')
    op.drop_table('teachers')
    op.drop_index(op.f('ix_tasks_id'), table_name='tasks')
    op.drop_table('tasks')
    op.drop_index(op.f('ix_lessons_id'), table_name='lessons')
    op.drop_table('lessons')
    op.drop_index(op.f('ix_Users_id'), table_name='Users')
    op.drop_table('Users')
    # ### end Alembic commands ###
