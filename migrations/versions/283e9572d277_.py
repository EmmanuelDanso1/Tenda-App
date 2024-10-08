"""empty message

Revision ID: 283e9572d277
Revises: 982ed25ba02f
Create Date: 2024-09-13 10:04:48.654865

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '283e9572d277'
down_revision = '982ed25ba02f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tenda', schema=None) as batch_op:
        batch_op.add_column(sa.Column('task_id', sa.Integer(), nullable=False))
        batch_op.drop_column('id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tenda', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.INTEGER(), nullable=False))
        batch_op.drop_column('task_id')

    # ### end Alembic commands ###
