"""add bills table

Revision ID: 7a537fd6f51b
Revises: c01f971085c8
Create Date: 2019-04-24 09:33:23.469295

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7a537fd6f51b'
down_revision = 'c01f971085c8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('email', sa.VARCHAR(length=254), nullable=False),
    sa.Column('username', sa.VARCHAR(length=128), nullable=False),
    sa.Column('password_hash', sa.VARCHAR(length=128), nullable=True),
    sa.Column('registered_at', sa.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###
