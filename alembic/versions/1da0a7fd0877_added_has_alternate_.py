"""added has_alternate attribute to issue

Revision ID: 1da0a7fd0877
Revises: 255e433c3d28
Create Date: 2013-09-02 22:15:17.816355

"""

# revision identifiers, used by Alembic.
revision = '1da0a7fd0877'
down_revision = '255e433c3d28'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('issues', sa.Column('has_alternates', sa.Boolean(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('issues', 'has_alternates')
    ### end Alembic commands ###
