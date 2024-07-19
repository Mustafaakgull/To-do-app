"""Add details to Task model

Revision ID: 236eefaaf812
Revises: 5637464596a0
Create Date: 2024-07-16 10:02:25.701636

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '236eefaaf812'
down_revision = '5637464596a0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('detail',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=200), nullable=False),
    sa.Column('task_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['task_id'], ['task.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('detail')
    # ### end Alembic commands ###
