"""db changes

Revision ID: 3bba7e1c743a
Revises: 124a8d5f7051
Create Date: 2021-11-29 02:38:28.422817

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3bba7e1c743a'
down_revision = '124a8d5f7051'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Message', 'body',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    op.alter_column('Message', 'image',
               existing_type=sa.VARCHAR(length=1000000),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Message', 'image',
               existing_type=sa.VARCHAR(length=1000000),
               nullable=False)
    op.alter_column('Message', 'body',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    # ### end Alembic commands ###
