"""add content column to posts table

Revision ID: 27f5262f3e69
Revises: e6fef4bcc804
Create Date: 2021-12-16 14:32:51.985867

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '27f5262f3e69'
down_revision = 'e6fef4bcc804'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
