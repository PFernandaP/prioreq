"""add area to projects

Revision ID: eaa6d1ead5a0
Revises: 034c0d71e45e
Create Date: 2025-12-09 18:33:43.581036
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eaa6d1ead5a0'
down_revision: Union[str, Sequence[str], None] = '034c0d71e45e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: add area column to projects table."""
    op.add_column(
        'projects',
        sa.Column('area', sa.String(length=255), nullable=True)
    )


def downgrade() -> None:
    """Downgrade schema: remove area column from projects table."""
    op.drop_column('projects', 'area')
