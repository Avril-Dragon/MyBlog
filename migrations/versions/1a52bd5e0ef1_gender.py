"""gender

Revision ID: 1a52bd5e0ef1
Revises: 5b8c15bb39a9
Create Date: 2021-06-25 10:19:16.948839

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1a52bd5e0ef1'
down_revision = '5b8c15bb39a9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('gender', sa.String(length=10), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'gender')
    # ### end Alembic commands ###
