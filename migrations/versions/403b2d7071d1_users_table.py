"""users table

Revision ID: 403b2d7071d1
Revises: 
Create Date: 2019-10-05 16:59:05.544795

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '403b2d7071d1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=70), nullable=True),
    sa.Column('email', sa.String(length=90), nullable=True),
    sa.Column('password_hash', sa.String(length=110), nullable=True),
    sa.Column('gender', sa.String(length=5), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
