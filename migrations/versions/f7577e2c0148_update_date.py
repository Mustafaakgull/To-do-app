"""update date

Revision ID: f7577e2c0148
Revises: 236eefaaf812
Create Date: 2024-07-16 10:33:30.287565

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f7577e2c0148'
down_revision = '236eefaaf812'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('detail')
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.alter_column('date',
               existing_type=sa.VARCHAR(length=4),
               type_=sa.String(length=200),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.alter_column('date',
               existing_type=sa.String(length=200),
               type_=sa.VARCHAR(length=4),
               existing_nullable=False)

    op.create_table('detail',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('description', sa.VARCHAR(length=200), autoincrement=False, nullable=False),
    sa.Column('task_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['task_id'], ['task.id'], name='detail_task_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='detail_pkey')
    )
    # ### end Alembic commands ###
