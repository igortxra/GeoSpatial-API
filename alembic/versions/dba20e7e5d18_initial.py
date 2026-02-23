"""initial

Revision ID: dba20e7e5d18
Revises:
Create Date: 2026-02-23 11:46:02.431785

"""

from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = "dba20e7e5d18"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
