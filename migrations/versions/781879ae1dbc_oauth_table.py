"""OAuth table

Revision ID: 781879ae1dbc
Revises: c201844df0e6
Create Date: 2018-06-18 12:43:22.455221

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '781879ae1dbc'
down_revision = 'c201844df0e6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('flask_dance_oauth',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('provider', sa.String(length=50), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('token', sqlalchemy_utils.types.json.JSONType(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], [u'user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('flask_dance_oauth')
    # ### end Alembic commands ###
