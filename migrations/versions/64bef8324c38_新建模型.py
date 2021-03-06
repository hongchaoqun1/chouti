"""新建模型

Revision ID: 64bef8324c38
Revises: 884200177bec
Create Date: 2018-06-19 17:22:37.204131

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64bef8324c38'
down_revision = '884200177bec'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('news',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('userinfo_id', sa.Integer(), nullable=True),
    sa.Column('ntype', sa.Integer(), nullable=True),
    sa.Column('ctime', sa.DateTime(), nullable=True),
    sa.Column('title', sa.String(length=32), nullable=True),
    sa.Column('url', sa.String(length=128), nullable=True),
    sa.Column('content', sa.String(length=256), nullable=True),
    sa.ForeignKeyConstraint(['ntype'], ['news_type.id'], ),
    sa.ForeignKeyConstraint(['userinfo_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_info_id', sa.Integer(), nullable=True),
    sa.Column('news_id', sa.Integer(), nullable=True),
    sa.Column('reply_id', sa.Integer(), nullable=True),
    sa.Column('up', sa.Integer(), nullable=True),
    sa.Column('down', sa.Integer(), nullable=True),
    sa.Column('ctime', sa.DateTime(), nullable=True),
    sa.Column('device', sa.String(length=32), nullable=True),
    sa.Column('content', sa.String(length=256), nullable=True),
    sa.ForeignKeyConstraint(['news_id'], ['news.id'], ),
    sa.ForeignKeyConstraint(['reply_id'], ['comment.id'], ),
    sa.ForeignKeyConstraint(['user_info_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('favor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_info_id', sa.Integer(), nullable=True),
    sa.Column('news_id', sa.Integer(), nullable=True),
    sa.Column('ctime', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['news_id'], ['news.id'], ),
    sa.ForeignKeyConstraint(['user_info_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('favor')
    op.drop_table('comment')
    op.drop_table('news')
    # ### end Alembic commands ###
