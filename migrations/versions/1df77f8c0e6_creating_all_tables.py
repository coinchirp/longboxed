"""creating all tables

Revision ID: 1df77f8c0e6
Revises: None
Create Date: 2013-10-27 23:45:32.505065

"""

# revision identifiers, used by Alembic.
revision = '1df77f8c0e6'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('creators',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('creator_type', sa.Enum('writer', 'artist', 'other', name='creator_type'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('publishers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('google_id', sa.String(length=255), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('first_name', sa.String(length=255), nullable=True),
    sa.Column('last_name', sa.String(length=255), nullable=True),
    sa.Column('full_name', sa.String(length=255), nullable=True),
    sa.Column('birthday', sa.Date(), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('last_login_at', sa.DateTime(), nullable=True),
    sa.Column('current_login_at', sa.DateTime(), nullable=True),
    sa.Column('last_login_ip', sa.String(length=80), nullable=True),
    sa.Column('current_login_ip', sa.String(length=80), nullable=True),
    sa.Column('login_count', sa.Integer(), nullable=True),
    sa.Column('confirmed_at', sa.DateTime(), nullable=True),
    sa.Column('display_pull_list', sa.Boolean(), nullable=True),
    sa.Column('default_cal', sa.String(length=255), nullable=True),
    sa.Column('mail_bundles', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('google_id')
    )
    op.create_table('roles_users',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint()
    )
    op.create_table('titles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('publisher_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['publisher_id'], ['publishers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bundles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.Column('release_date', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('publishers_users',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('publisher_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['publisher_id'], ['publishers.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint()
    )
    op.create_table('connection',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('provider_id', sa.String(length=255), nullable=True),
    sa.Column('provider_user_id', sa.String(length=255), nullable=True),
    sa.Column('access_token', sa.String(length=255), nullable=True),
    sa.Column('secret', sa.String(length=255), nullable=True),
    sa.Column('display_name', sa.String(length=255), nullable=True),
    sa.Column('profile_url', sa.String(length=512), nullable=True),
    sa.Column('image_url', sa.String(length=512), nullable=True),
    sa.Column('rank', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('issues',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title_id', sa.Integer(), nullable=True),
    sa.Column('publisher_id', sa.Integer(), nullable=True),
    sa.Column('product_id', sa.String(length=100), nullable=True),
    sa.Column('issue_number', sa.Numeric(precision=6, scale=2), nullable=True),
    sa.Column('issues', sa.Numeric(precision=6, scale=2), nullable=True),
    sa.Column('other', sa.String(length=255), nullable=True),
    sa.Column('complete_title', sa.String(length=255), nullable=True),
    sa.Column('one_shot', sa.Boolean(), nullable=True),
    sa.Column('a_link', sa.String(length=255), nullable=True),
    sa.Column('thumbnail', sa.String(length=255), nullable=True),
    sa.Column('big_image', sa.String(length=255), nullable=True),
    sa.Column('retail_price', sa.Float(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('on_sale_date', sa.Date(), nullable=True),
    sa.Column('prospective_release_date', sa.Date(), nullable=True),
    sa.Column('genre', sa.String(length=100), nullable=True),
    sa.Column('people', sa.String(length=255), nullable=True),
    sa.Column('popularity', sa.Float(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.Column('diamond_id', sa.String(length=100), nullable=True),
    sa.Column('discount_code', sa.String(length=1), nullable=True),
    sa.Column('category', sa.String(length=100), nullable=True),
    sa.Column('upc', sa.String(length=100), nullable=True),
    sa.Column('is_parent', sa.Boolean(), nullable=True),
    sa.Column('has_alternates', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['publisher_id'], ['publishers.id'], ),
    sa.ForeignKeyConstraint(['title_id'], ['titles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('titles_users',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('title_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['title_id'], ['titles.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint()
    )
    op.create_table('issues_bundles',
    sa.Column('bundle_id', sa.Integer(), nullable=True),
    sa.Column('issue_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['bundle_id'], ['bundles.id'], ),
    sa.ForeignKeyConstraint(['issue_id'], ['issues.id'], ),
    sa.PrimaryKeyConstraint()
    )
    op.create_table('issues_creators',
    sa.Column('creator_id', sa.Integer(), nullable=True),
    sa.Column('issue_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['creator_id'], ['creators.id'], ),
    sa.ForeignKeyConstraint(['issue_id'], ['issues.id'], ),
    sa.PrimaryKeyConstraint()
    )
    op.create_table('issue_cover',
    sa.Column('width', sa.Integer(), nullable=False),
    sa.Column('height', sa.Integer(), nullable=False),
    sa.Column('mimetype', sa.String(length=255), nullable=False),
    sa.Column('original', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('issue_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['issue_id'], ['issues.id'], ),
    sa.PrimaryKeyConstraint('width', 'height', 'issue_id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('issue_cover')
    op.drop_table('issues_creators')
    op.drop_table('issues_bundles')
    op.drop_table('titles_users')
    op.drop_table('issues')
    op.drop_table('connection')
    op.drop_table('publishers_users')
    op.drop_table('bundles')
    op.drop_table('titles')
    op.drop_table('roles_users')
    op.drop_table('users')
    op.drop_table('publishers')
    op.drop_table('creators')
    op.drop_table('role')
    ### end Alembic commands ###