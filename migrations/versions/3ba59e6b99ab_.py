"""empty message

Revision ID: 3ba59e6b99ab
Revises: ab9d35a2a7e3
Create Date: 2023-06-15 12:31:45.632778

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ba59e6b99ab'
down_revision = 'ab9d35a2a7e3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('delivery_rider',
    sa.Column('riderID', sa.Integer(), nullable=False),
    sa.Column('riderName', sa.String(length=20), nullable=False),
    sa.Column('riderSalary', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('riderID'),
    sa.UniqueConstraint('riderName')
    )
    op.drop_table('delivery_riders')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('delivery_riders',
    sa.Column('riderID', sa.INTEGER(), nullable=False),
    sa.Column('riderName', sa.VARCHAR(length=20), nullable=False),
    sa.Column('riderSalary', sa.INTEGER(), nullable=False),
    sa.PrimaryKeyConstraint('riderID'),
    sa.UniqueConstraint('riderName')
    )
    op.drop_table('delivery_rider')
    # ### end Alembic commands ###