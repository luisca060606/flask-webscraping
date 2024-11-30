"""initial migration

Revision ID: a04a7de6ae9e
Revises: 
Create Date: 2024-11-30 13:36:22.300957

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a04a7de6ae9e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.alter_column('pname', new_column_name='product_name')

    # ### end Alembic commands ###


def downgrade():
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.alter_column('product_name', new_column_name='pname')

    # ### end Alembic commands ###
