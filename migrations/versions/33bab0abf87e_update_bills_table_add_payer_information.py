"""update bills table: add payer information

Revision ID: 33bab0abf87e
Revises: 7a537fd6f51b
Create Date: 2019-04-24 17:52:41.138104

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '33bab0abf87e'
down_revision = '7a537fd6f51b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('bill_details', 'is_payer')
    op.add_column('bills', sa.Column('payer_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'bills', 'users', ['payer_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'bills', type_='foreignkey')
    op.drop_column('bills', 'payer_id')
    op.add_column('bill_details', sa.Column('is_payer', sa.BOOLEAN(), nullable=True))
    # ### end Alembic commands ###
