"""add_default_timestamps

Revision ID: e04ba0d64869
Revises: 53fc59a83b12
Create Date: 2026-01-30 00:47:38.241628

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'new_revision_id_here'
down_revision: str = '53fc59a83b12'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # First, drop the NOT NULL constraint temporarily
    op.alter_column('users', 'created_at',
                    existing_type=postgresql.TIMESTAMP(),
                    nullable=True)
    
    op.alter_column('users', 'updated_at',
                    existing_type=postgresql.TIMESTAMP(),
                    nullable=True)
    
    # Update existing NULL values to CURRENT_TIMESTAMP
    op.execute("UPDATE users SET created_at = CURRENT_TIMESTAMP WHERE created_at IS NULL")
    op.execute("UPDATE users SET updated_at = CURRENT_TIMESTAMP WHERE updated_at IS NULL")
    
    # Now add the default and set NOT NULL
    op.alter_column('users', 'created_at',
                    existing_type=postgresql.TIMESTAMP(),
                    server_default=sa.text('CURRENT_TIMESTAMP'),
                    nullable=False)
    
    op.alter_column('users', 'updated_at',
                    existing_type=postgresql.TIMESTAMP(),
                    server_default=sa.text('CURRENT_TIMESTAMP'),
                    nullable=False)


def downgrade() -> None:
    # Remove defaults
    op.alter_column('users', 'created_at',
                    existing_type=postgresql.TIMESTAMP(),
                    server_default=None,
                    nullable=True)
    
    op.alter_column('users', 'updated_at',
                    existing_type=postgresql.TIMESTAMP(),
                    server_default=None,
                    nullable=True)