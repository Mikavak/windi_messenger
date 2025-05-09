"""Add new line in model chat

Revision ID: 4b13e16ffa02
Revises: 682be9758e5f
Create Date: 2025-05-09 14:15:17.262042

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4b13e16ffa02'
down_revision: Union[str, None] = '682be9758e5f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Сначала добавляем nullable колонку
    op.add_column('chat', sa.Column('creator_id', sa.Integer(), nullable=True))

    # Получаем первого пользователя в базе как дефолтного создателя
    op.execute('UPDATE chat SET creator_id = (SELECT id FROM "user" LIMIT 1)')

    # Меняем колонку на NOT NULL
    op.alter_column('chat', 'creator_id', nullable=False)

    # Добавляем внешний ключ к таблице пользователей
    op.create_foreign_key(
        'fk_chat_creator',
        'chat',
        'user',
        ['creator_id'],
        ['id']
    )


def downgrade():
    # Удаляем внешний ключ
    op.drop_constraint('fk_chat_creator', 'chat', type_='foreignkey')

    # Удаляем колонку
    op.drop_column('chat', 'creator_id')
