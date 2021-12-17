"""add foreign key to post table

Revision ID: 986737dc918c
Revises: 15381d1bfdf7
Create Date: 2021-12-16 15:41:11.065943

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import table


# revision identifiers, used by Alembic.
revision = '986737dc918c'
down_revision = '15381d1bfdf7'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
