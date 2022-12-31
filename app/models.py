from app import db
from app import ma
from marshmallow import Schema, fields, pre_load, validate

#relacion de muchos a muchos entre las tablas evento_usuario
evento_usuario_table=db.Table(
  "evento_usuario", 
  db.metadata,
  db.Column("evento_id",db.ForeignKey("evento.id",primary_key=True)),
  db.Column("usuario_id",db.ForeignKey("usuario.id",primary_key=True)),
  )
#relacion de muchos a muchos entre las tablas usuario-roles
usuario_roles=db.Table(
  "usuario_roles",
  db.metadata,
  db.Column("usuario_id",db.ForeignKey("usuario.id",primary_key=True)),
  db.Column("roles_id",db.ForeignKey("roles.id",primary_key=True)),
)
#relacion de muchos a muchos entre las tablas roles-permisos
roles_permisos=db.Table(
  "roles_permisos",
  db.metadata,
  db.Column("roles_id",db.ForeignKey("roles.id",primary_key=True)),
  db.Column("permisos_id",db.ForeignKey("permisos.id",primary_key=True)),
)


class Unidad(db.Model):
  __tablename__='unidad'
  id = db.Column(db.Integer, primary_key=True)
  descripcion = db.Column(db.String(250),nullable=False)
  activo = db.Column(db.Boolean,nullable=True)
  created_at=db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(),nullable=False)
  updated_at=db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(),nullable=False,onupdate=db.func.now())

class Usuario(db.Model):
  __tablename__ = 'usuario'
  id = db.Column(db.Integer, primary_key=True)
  nombres = db.Column(db.String(50),nullable=False)
  apellidos = db.Column(db.String(50),nullable=False)
  usuario = db.Column(db.String(50),nullable=False, unique=True)
  password = db.Column(db.Text(),nullable=False)
  correo = db.Column(db.String(100),nullable=False)
  responsable = db.Column(db.Boolean,nullable=True)
  activo = db.Column(db.Boolean,nullable=True)
  unidad_id = db.Column(db.Integer, db.ForeignKey('unidad.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=True)
  created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(),nullable=False)
  updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(),nullable=False,onupdate=db.func.now())
  
  #creacion de un join con la tabla unidad relacion de uno a muchos
  unidad=db.relationship('Unidad', backref=db.backref('usuario',lazy='dynamic'))
  #creacion de un join con la tabla roles relacion muchos a muchos 'secondary=usuario_roles, es la variable declarada en la linea 13' 
  roles=db.relationship('Roles', secondary=usuario_roles, backref=db.backref('usuario',lazy='dynamic'))

class Evento(db.Model):
  __tablename__ = 'evento'
  id = db.Column(db.Integer, primary_key=True)
  institucion = db.Column(db.Text,nullable=False)
  tema = db.Column(db.Text,nullable=False)
  lugar = db.Column(db.Text,nullable=True)
  fecha = db.Column(db.Date,nullable=True)
  hora = db.Column(db.Time,nullable=True)
  estado = db.Column(db.String(256),nullable=True)
  activo = db.Column(db.Boolean,nullable=True)
  usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=True)
  aprobado_id = db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=True)
  created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(),nullable=False)
  updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(),nullable=False,onupdate=db.func.now())
  #creacion de un join con la tabla usuario relacion muchos a muchos 'secondary=usuario_roles, es la variable declarada en la linea 13' 
  usuarios=db.relationship('Usuario',secondary=evento_usuario_table,backref=db.backref('eventos',lazy='dynamic'))
  usuarios_created=db.relationship('Usuario',foreign_keys=usuario_id,backref=db.backref('eventos_created',lazy='dynamic'))
  usuarios_approved=db.relationship('Usuario',foreign_keys=aprobado_id,backref=db.backref('eventos_approved',lazy='dynamic'))

class Roles(db.Model):
  __tablename__='roles'
  id = db.Column(db.Integer, primary_key=True)
  nombre=db.Column(db.String(100),nullable=False)
  created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(),nullable=False)
  updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(),nullable=False,onupdate=db.func.now())
  #creacion de un join con la tabla usuario relacion muchos a muchos 'secondary=usuario_roles, es la variable declarada en la linea 13' 
  #usuarios=db.relationship('Usuario',secondary=usuario_roles,backref=db.backref('roles',lazy='dynamic'))

class Permisos(db.Model):
  __tablename__='permisos'
  id = db.Column(db.Integer, primary_key=True)
  nombre=db.Column(db.String(100),nullable=False)
  created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(),nullable=False)
  updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(),nullable=False,onupdate=db.func.now())
  #roles=db.relationship('Roles',secondary=roles_permisos,backref=db.backref('permisos',lazy='dynamic'))
  '''
  validaciones
  '''
class UnidadSchema(ma.Schema):
  class Meta:
    order=True
  id = fields.Integer()  
  descripcion = fields.String(required=True,error_messages={"required":"descripcion es requerido"})  
  activo = fields.Boolean(required=False)  
  created_at = fields.DateTime(required=True, dump_only=True)  
  updated_at= fields.DateTime(required=True, dump_only=True)  

class UsuarioSchema(ma.Schema):
  class Meta:
    ordered=True
  id = fields.Integer()
  nombres = fields.String(required=True,error_messages={"required":"nombres es requerido"}) 
  apellidos = fields.String(required=True,error_messages={"required":"apellidos es requerido"}) 
  usuario = fields.String(required=True,error_messages={"required":"nombre de usuario es requerido"}) 
  #password = fields.String(required=True,error_messages={"required":"password es requerido"})
  password = fields.String(required=True,error_messages={"required":"password es requerido"}, load_only=True)#load_only=True hace que el password no se muestre al momento de mostrar los datos
  correo = fields.String(required=True,validate=validate.Email(error="Correo no valido"),error_messages={"required":"correo es requerido"}) 
  responsable = fields.Boolean(required=False) 
  activo = fields.Boolean(required=False) 
  unidad_id = fields.Integer(required=False, allow_none=True) 
  created_at = fields.DateTime(required=True, dump_only=True) 
  updated_at = fields.DateTime(required=True, dump_only=True) 
  
  #creacion de un join con la tabla unidad
  #unidad=fields.Nested(lambda:UnidadSchema(exclude=("created_at","updated_at")), dump_only=True)#muestra todos los campos de la tabla unidad ecepto created_at y updated_at
  unidad=fields.Nested(lambda:UnidadSchema(), dump_only=True)#muestra todos loa campos de la tabla unidad
  #creacion de un join muchos a muchos
  roles=fields.Nested(lambda:RolesSchema(),many=True, dump_only=True)

class EventoSchema(ma.Schema):
  class Meta:
    ordered=True
  id = fields.Integer() 
  institucion =fields.String(required=True,error_messages={"required":"institucion es requerido"}) 
  tema = fields.String(required=True,error_messages={"required":"tema es requerido"}) 
  lugar = fields.String(required=False) 
  fecha = fields.Date(required=False) 
  hora = fields.Time(required=False) 
  estado = fields.String(requiered=False) 
  activo = fields.Boolean(required=False) 
  usuario_id = fields.Integer(required=False) 
  aprobado_id = fields.Integer(required=False)  
  created_at = fields.DateTime(required=True, dump_only=True) 
  updated_at = fields.DateTime(required=True, dump_only=True) 
  
  #creacion de un join muchos a muchos
  usuarios=fields.Nested(lambda:UsuarioSchema(),many=True, dump_only=True)
  #creacion de un join con la tabla usuarios relacion de uno a muchos
  usuarios_created=fields.Nested(lambda:UsuarioSchema(), dump_only=True)#muestra todos loa campos de la tabla unidad
  usuarios_approved=fields.Nested(lambda:UsuarioSchema(), dump_only=True)#muestra todos loa campos de la tabla unidad


class RolesSchema(ma.Schema):
  class Meta:
    ordered=True
  id = fields.Integer() 
  nombre=fields.String(required=True) 
  created_at = fields.DateTime(required=True, dump_only=True) 
  updated_at = fields.DateTime(required=True, dump_only=True)
  #creacion de un join muchos a muchos
  #usuarios=fields.Nested(lambda:UsuarioSchema(),many=True, dump_only=True)
  

class PermisosSchema(ma.Schema):
  class Meta:
    ordered=True
  id = fields.Integer()
  nombre = fields.String(required=True) 
  created_at = fields.DateTime(required=True, dump_only=True) 
  updated_at = fields.DateTime(required=True, dump_only=True)
  #creacion de un join muchos a muchos
  #roles=fields.Nested(lambda:RolesSchema(),many=True, dump_only=True)
  #roles=db.relationship('Roles',secondary=roles_permisos,backref=db.backref('permisos',lazy='dynamic'))


class LoginSchema(ma.Schema):
  class Meta:
    ordered=True
  usuario=fields.String(requiered=True, error_messages={"required":"el campo usuario es requerido"}) 
  password=fields.String(requiered=True, error_messages={"required":"el campo password es requerido"})

class UsuarioSwaggerSchema(ma.SQLAlchemyAutoSchema): 
  class Meta:
    model=Usuario
    include_fk=True
    ordered=True
  id=fields.Integer(dump_only=True)
  created_at=fields.DateTime(dump_only=True)
  updated_at=fields.DateTime(dump_only=True)

class EventoSwaggerSchema(ma.SQLAlchemyAutoSchema): 
  class Meta:
    model=Evento
    include_fk=True
    ordered=True
  id=fields.Integer(dump_only=True)
  created_at=fields.DateTime(dump_only=True)
  updated_at=fields.DateTime(dump_only=True)

class UnidadSwaggerSchema(ma.SQLAlchemyAutoSchema): 
  class Meta:
    model=Unidad
    #include_fk=True
    ordered=True
  id=fields.Integer(dump_only=True)
  created_at=fields.DateTime(dump_only=True)
  updated_at=fields.DateTime(dump_only=True)

class RolesSwaggerSchema(ma.SQLAlchemyAutoSchema): 
  class Meta:
    model=Roles
    #include_fk=True
    ordered=True
  id=fields.Integer(dump_only=True)
  created_at=fields.DateTime(dump_only=True)
  updated_at=fields.DateTime(dump_only=True)

class PermisosSwaggerSchema(ma.SQLAlchemyAutoSchema): 
  class Meta:
    model=Permisos
    #include_fk=True
    ordered=True
  id=fields.Integer(dump_only=True)
  created_at=fields.DateTime(dump_only=True)
  updated_at=fields.DateTime(dump_only=True)



