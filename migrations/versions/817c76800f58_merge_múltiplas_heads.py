"""Merge múltiplas heads

Revision ID: 817c76800f58
Revises: [id_gerado], 3b15b1ca02e9
Create Date: 2025-10-16 19:36:00.292167

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '817c76800f58'
down_revision = ('[id_gerado]', '3b15b1ca02e9')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
