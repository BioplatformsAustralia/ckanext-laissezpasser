"""Temporary Access Passes

Revision ID: fe8daef351db
Revises: 
Create Date: 2024-04-06 04:22:20.774928

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe8daef351db'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'laissezpasser_passes',
        sa.Column('dataset', sa.UnicodeText(), sa.ForeignKey('package.name', onupdate='CASCADE', ondelete='CASCADE'), nullable=False),        
        sa.Column('user_name', sa.UnicodeText, sa.ForeignKey('user.name'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=False), nullable=False),
        sa.Column('created_by', sa.UnicodeText, sa.ForeignKey('user.name'), nullable=False),
        sa.Column('valid_until', sa.DateTime(timezone=False), nullable=False),
    )

    op.create_primary_key(
        'laissezpasser_passes_pkey', 'laissezpasser_passes',
        ['dataset', 'user_name']
    )

def downgrade():
    op.drop_table('laissezpasser_passes')
