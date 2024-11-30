"""add models in app products

Revision ID: 64ad1f57d171
Revises: a04a7de6ae9e
Create Date: 2024-11-30 15:58:42.821881

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64ad1f57d171'
down_revision = 'a04a7de6ae9e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('category_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_test_product_id_category'), 'categories', ['category_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('category_id')
        batch_op.drop_column('description')

    # ### end Alembic commands ###