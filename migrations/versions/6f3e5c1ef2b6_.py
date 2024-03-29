"""empty message

Revision ID: 6f3e5c1ef2b6
Revises: 8df37a97ee09
Create Date: 2023-06-15 12:36:09.712134

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6f3e5c1ef2b6'
down_revision = '8df37a97ee09'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order', schema=None) as batch_op:
        batch_op.add_column(sa.Column('riderID', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'rider', ['riderID'], ['riderID'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('riderID')

    # ### end Alembic commands ###
