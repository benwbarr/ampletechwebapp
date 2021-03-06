"""added username

Revision ID: 118cef2a93bd
Revises: 1325c24effc3
Create Date: 2021-09-27 13:12:48.631779

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '118cef2a93bd'
down_revision = '1325c24effc3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('username', sa.String(length=20), nullable=False))
    op.create_unique_constraint(None, 'users', ['username'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'username')
    # ### end Alembic commands ###
