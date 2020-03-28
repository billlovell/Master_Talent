"""new fields in user model

Revision ID: 01eec08a0fad
Revises: 9596e11a815d
Create Date: 2020-02-07 08:52:39.428669

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01eec08a0fad'
down_revision = '9596e11a815d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('about_me', sa.String(length=140), nullable=True))
    op.add_column('user', sa.Column('last_seen', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'last_seen')
    op.drop_column('user', 'about_me')
    # ### end Alembic commands ###