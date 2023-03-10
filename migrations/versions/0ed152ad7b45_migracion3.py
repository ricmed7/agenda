"""migracion3

Revision ID: 0ed152ad7b45
Revises: 2f3825e3022a
Create Date: 2022-12-27 22:56:06.379788

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ed152ad7b45'
down_revision = '2f3825e3022a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('permisos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roles_permisos',
    sa.Column('roles_id', sa.Integer(), nullable=True),
    sa.Column('permisos_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['permisos_id'], ['permisos.id'], ),
    sa.ForeignKeyConstraint(['roles_id'], ['roles.id'], )
    )
    op.create_table('usuario_roles',
    sa.Column('usuario_id', sa.Integer(), nullable=True),
    sa.Column('roles_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['roles_id'], ['roles.id'], ),
    sa.ForeignKeyConstraint(['usuario_id'], ['usuario.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('usuario_roles')
    op.drop_table('roles_permisos')
    op.drop_table('roles')
    op.drop_table('permisos')
    # ### end Alembic commands ###
