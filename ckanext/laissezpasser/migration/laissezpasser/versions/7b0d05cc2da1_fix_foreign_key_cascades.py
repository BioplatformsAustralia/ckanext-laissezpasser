"""Fix foreign key cascades

Revision ID: 7b0d05cc2da1
Revises: fe8daef351db
Create Date: 2026-03-24 07:51:56.211151

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7b0d05cc2da1'
down_revision = 'fe8daef351db'
branch_labels = None


def upgrade():
    op.drop_constraint(
        constraint_name="laissezpasser_passes_user_name_fkey",
        table_name="laissezpasser_passes",
        type_="foreignkey"
    )
    op.create_foreign_key(
        constraint_name="laissezpasser_passes_user_name_fkey",
        source_table="laissezpasser_passes",
        referent_table="user",
        local_cols=["user_name"],
        remote_cols=["name"],
        onupdate="CASCADE",
        ondelete="CASCADE"
    )
    op.drop_constraint(
        constraint_name="laissezpasser_passes_created_by_fkey",
        table_name="laissezpasser_passes",
        type_="foreignkey"
    )
    op.create_foreign_key(
        constraint_name="laissezpasser_passes_created_by_fkey",
        source_table="laissezpasser_passes",
        referent_table="user",
        local_cols=["created_by"],
        remote_cols=["name"],
        onupdate="CASCADE",
        ondelete="CASCADE"
    )


def downgrade():
    op.drop_constraint(
        constraint_name="laissezpasser_passes_user_name_fkey",
        table_name="laissezpasser_passes",
        type_="foreignkey"
    )
    op.create_foreign_key(
        constraint_name="laissezpasser_passes_user_name_fkey",
        source_table="laissezpasser_passes",
        referent_table="user",
        local_cols=["user_name"],
        remote_cols=["name"],
    )
    op.drop_constraint(
        constraint_name="laissezpasser_passes_created_by_fkey",
        table_name="laissezpasser_passes",
        type_="foreignkey"
    )
    op.create_foreign_key(
        constraint_name="laissezpasser_passes_created_by_fkey",
        source_table="laissezpasser_passes",
        referent_table="user",
        local_cols=["created_by"],
        remote_cols=["name"],
        onupdate="CASCADE",
        ondelete="CASCADE"
    )
