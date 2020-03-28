"""add langauge to psots

Revision ID: 7cec2a5efcfb
Revises: aa3ffb0e6da2
Create Date: 2020-02-16 10:27:26.903007

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7cec2a5efcfb'
down_revision = 'aa3ffb0e6da2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('language', sa.String(length=5), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'language')
    # ### end Alembic commands ###