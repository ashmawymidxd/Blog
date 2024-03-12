"""Changs

Revision ID: 9e2fe0290a98
Revises: 0d126bf27605
Create Date: 2024-03-12 19:25:51.772987

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '9e2fe0290a98'
down_revision = '0d126bf27605'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('password')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password', mysql.VARCHAR(length=100), nullable=True))

    # ### end Alembic commands ###