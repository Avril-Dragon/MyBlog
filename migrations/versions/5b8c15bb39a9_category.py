"""'category'

Revision ID: 5b8c15bb39a9
Revises: 3e16c4d83239
Create Date: 2021-06-23 15:53:21.984452

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b8c15bb39a9'
down_revision = '3e16c4d83239'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('category', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'category')
    # ### end Alembic commands ###