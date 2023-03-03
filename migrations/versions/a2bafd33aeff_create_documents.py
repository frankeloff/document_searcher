"""create documents

Revision ID: a2bafd33aeff
Revises: 
Create Date: 2023-03-03 12:50:26.661686

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a2bafd33aeff'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('documents',
    sa.Column('doc_id', sa.Integer(), nullable=False),
    sa.Column('rubrics', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('text', sa.Text(), nullable=True),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('doc_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('documents')
    # ### end Alembic commands ###
