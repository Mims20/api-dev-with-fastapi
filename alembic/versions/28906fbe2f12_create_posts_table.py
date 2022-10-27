"""create posts table

Revision ID: 28906fbe2f12
Revises: 
Create Date: 2022-10-25 21:40:44.411856

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '28906fbe2f12'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("posts", sa.Column("id", sa.Integer, nullable=False, primary_key=True),
                    sa.Column("title", sa.String, nullable=False))
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass
