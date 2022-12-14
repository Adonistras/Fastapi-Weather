"""services1.6

Revision ID: 8df4aff8e440
Revises: 5b400738ca5e
Create Date: 2022-10-15 19:19:01.274357

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8df4aff8e440'
down_revision = '5b400738ca5e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('cities', 'created')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cities', sa.Column('created', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
