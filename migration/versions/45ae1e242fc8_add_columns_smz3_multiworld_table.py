"""add columns smz3 multiworld table

Revision ID: 45ae1e242fc8
Revises: 175558ca8e3f
Create Date: 2020-09-20 22:34:40.570880

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '45ae1e242fc8'
down_revision = '175558ca8e3f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('smz3_multiworld', sa.Column('preset', mysql.VARCHAR(length=45), nullable=False))
    op.add_column('smz3_multiworld', sa.Column('randomizer', mysql.VARCHAR(length=45), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('smz3_multiworld', 'randomizer')
    op.drop_column('smz3_multiworld', 'preset')
    # ### end Alembic commands ###