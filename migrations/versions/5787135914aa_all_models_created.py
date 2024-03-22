"""all models created.

Revision ID: 5787135914aa
Revises: 42dd54c7b373
Create Date: 2024-03-21 18:24:05.590869

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5787135914aa'
down_revision = '42dd54c7b373'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('transaction',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('account_id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(length=10), nullable=False),
    sa.CheckConstraint("type IN ('deposit', 'withdrawal', 'transfer')", name='check_transaction_type'),
    sa.ForeignKeyConstraint(['account_id'], ['account.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('account', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.String(length=200), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('account', schema=None) as batch_op:
        batch_op.drop_column('description')

    op.drop_table('transaction')
    # ### end Alembic commands ###
