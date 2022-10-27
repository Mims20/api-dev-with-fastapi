"""add foreign-key to posts table

Revision ID: 22c0bfb08fbf
Revises: b45608381444
Create Date: 2022-10-26 19:03:43.935430

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22c0bfb08fbf'
down_revision = 'b45608381444'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer, nullable=False))
    op.create_foreign_key(constraint_name="post_users_fk",
                          source_table="posts",
                          referent_table="users",
                          local_cols=["owner_id"],
                          remote_cols=["id"],
                          ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint(constraint_name="posts_users_fk",
                       table_name="posts")
    op.drop_column(table_name="posts", column_name="owner_id")
    pass
