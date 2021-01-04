"""empty message

Revision ID: e69d0f332b63
Revises: 0596784ba576
Create Date: 2020-12-28 17:21:03.367771

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e69d0f332b63'
down_revision = '0596784ba576'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('update_id', sa.Integer(), nullable=True),
    sa.Column('message_type', sa.String(length=50), nullable=True),
    sa.Column('message_body', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user_info.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('user_info', sa.Column('first_name', sa.String(length=124), nullable=True))
    op.add_column('user_info', sa.Column('last_name', sa.String(length=124), nullable=True))
    op.add_column('user_info', sa.Column('user_id', sa.String(length=50), nullable=True))
    op.drop_column('user_info', 'message_type')
    op.drop_column('user_info', 'message_body')
    op.drop_column('user_info', 'update_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_info', sa.Column('update_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('user_info', sa.Column('message_body', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True))
    op.add_column('user_info', sa.Column('message_type', sa.VARCHAR(length=50), autoincrement=False, nullable=True))
    op.drop_column('user_info', 'user_id')
    op.drop_column('user_info', 'last_name')
    op.drop_column('user_info', 'first_name')
    op.drop_table('user_message')
    # ### end Alembic commands ###