"""setup

Revision ID: 72a7b946cbd5
Revises: dba20e7e5d18
Create Date: 2026-02-23 11:46:57.395303

"""

from typing import Sequence, Union

import geoalchemy2
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "72a7b946cbd5"
down_revision: Union[str, Sequence[str], None] = "dba20e7e5d18"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "links",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("road_name", sa.String(), nullable=True),
        sa.Column(
            "geom",
            geoalchemy2.types.Geometry(
                geometry_type="LINESTRING",
                srid=4326,
                dimension=2,
                from_text="ST_GeomFromEWKT",
                name="geometry",
                nullable=False,
            ),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "speed_records",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=True),
        sa.Column("speed", sa.Float(), nullable=False),
        sa.Column("day_of_week", sa.Integer(), nullable=False),
        sa.Column("period", sa.Integer(), nullable=False),
        sa.Column("link_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["link_id"],
            ["links.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("timestamp", "link_id", name="uq_speedrecord_ts_link"),
    )
    op.create_index(
        "idx_speed_records_covering",
        "speed_records",
        ["day_of_week", "period", "link_id"],
        unique=False,
        postgresql_include=["speed"],
    )
    op.create_index(
        op.f("ix_speed_records_link_id"), "speed_records", ["link_id"], unique=False
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_speed_records_link_id"), table_name="speed_records")
    op.drop_index(
        "idx_speed_records_covering",
        table_name="speed_records",
        postgresql_include=["speed"],
    )
    op.drop_table("speed_records")
    op.drop_table("links")
