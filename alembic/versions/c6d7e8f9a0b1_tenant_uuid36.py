"""tenant id/owner_id/user_id varchar 32 -> 36

Revision ID: c6d7e8f9a0b1
Revises: b5655f13e8dc
Create Date: 2026-02-05

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'c6d7e8f9a0b1'
down_revision: Union[str, None] = 'b5655f13e8dc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        'tenants',
        'id',
        existing_type=sa.String(length=32),
        type_=sa.String(length=36),
        existing_nullable=False
    )
    op.alter_column(
        'tenants',
        'owner_id',
        existing_type=sa.String(length=32),
        type_=sa.String(length=36),
        existing_nullable=False
    )
    op.alter_column(
        'tenant_members',
        'tenant_id',
        existing_type=sa.String(length=32),
        type_=sa.String(length=36),
        existing_nullable=False
    )
    op.alter_column(
        'tenant_members',
        'user_id',
        existing_type=sa.String(length=32),
        type_=sa.String(length=36),
        existing_nullable=False
    )


def downgrade() -> None:
    op.alter_column(
        'tenant_members',
        'user_id',
        existing_type=sa.String(length=36),
        type_=sa.String(length=32),
        existing_nullable=False
    )
    op.alter_column(
        'tenant_members',
        'tenant_id',
        existing_type=sa.String(length=36),
        type_=sa.String(length=32),
        existing_nullable=False
    )
    op.alter_column(
        'tenants',
        'owner_id',
        existing_type=sa.String(length=36),
        type_=sa.String(length=32),
        existing_nullable=False
    )
    op.alter_column(
        'tenants',
        'id',
        existing_type=sa.String(length=36),
        type_=sa.String(length=32),
        existing_nullable=False
    )
