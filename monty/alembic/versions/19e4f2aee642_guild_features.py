"""guild features

Revision ID: 19e4f2aee642
Revises: 7d2f79cf061c
Create Date: 2022-06-25 02:20:19.273814

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy import sql
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "19e4f2aee642"
down_revision = "7d2f79cf061c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "features",
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("enabled", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("name"),
    )
    op.create_table(
        "guilds",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("features", postgresql.ARRAY(sa.String(length=50)), server_default="{}", nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.add_column("guild_config", sa.Column("guild", sa.BigInteger(), nullable=True))
    op.create_unique_constraint("guild_config_guild_key", "guild_config", ["guild"])
    op.create_foreign_key("fk_guild_config_guilds_id_guild", "guild_config", "guilds", ["guild"], ["id"])
    # ### end Alembic commands ###

    # we want to migrate to the guilds table, so this means creating guilds data
    op.execute("INSERT INTO guilds (id) SELECT id FROM guild_config")

    # then we want to update the guild_config guild column with the guilds we just created
    op.execute("UPDATE ONLY guild_config SET guild = (SELECT id FROM guilds WHERE guild_config.id = guilds.id)")


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("fk_guild_config_guilds_id_guild", "guild_config", type_="foreignkey")
    op.drop_constraint("guild_config_guild_key", "guild_config", type_="unique")
    op.drop_column("guild_config", "guild")
    op.drop_table("guilds")
    op.drop_table("features")
    # ### end Alembic commands ###
