"""remove phone number

Revision ID: 0745bce02e3e
Revises: 5f871ac82b64
Create Date: 2021-12-30 10:13:40.270548

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0745bce02e3e'
down_revision = '5f871ac82b64'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'phone_number')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('phone_number', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
