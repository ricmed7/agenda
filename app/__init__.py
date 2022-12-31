from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec import FlaskApiSpec

db=SQLAlchemy()
ma=Marshmallow()
migrate = Migrate()
docs =FlaskApiSpec()

def create_app(config_filename='config'):
  app=Flask(__name__)
  app.config.from_object(config_filename)

  app.config.update({
    'APISPEC_SPEC':APISpec(
      title='API REST - AGENDA',
      version='V1.0 mi primer api',
      plugins=[MarshmallowPlugin()],
      openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL':'/swagger/',
    'APISPEC_SWAGGER_UI_URL':'/swagger-ui/'
  })

  from app.models import Usuario, Unidad, Evento, Roles, Permisos
  db.init_app(app)
  ma.init_app(app)
  migrate.init_app(app, db)
  jwt=JWTManager(app)
  from app.routes.app import api_bp
  app.register_blueprint(api_bp, url_prefix='/api/v1')

  from app.resources.usuario import UsuarioListResource,updateUsuario,LoginResource
  from app.resources.evento import EventoListResource,updateEvento
  from app.resources.unidad import UnidadListResource,updateUnidad
  from app.resources.roles import RolesListResource,updateRoles
  from app.resources.permisos import PermisosListResource,updatePermisos
  docs.init_app(app)
  #registro de endpoints de usuario
  docs.register(LoginResource,blueprint='api', endpoint='loginresource')
  docs.register(UsuarioListResource,blueprint='api', endpoint='usuariolistresource')
  docs.register(updateUsuario,blueprint='api', endpoint='updateusuario')
  #registro de endpoints de eventos
  docs.register(EventoListResource, blueprint='api', endpoint='eventolistresource')
  docs.register(updateEvento, blueprint='api', endpoint='updateevento')
  #registro de endpoints de unidad
  docs.register(UnidadListResource, blueprint='api', endpoint='unidadlistresource')
  docs.register(updateUnidad, blueprint='api', endpoint='updateunidad')
  #registro de endpoints de roles
  docs.register(RolesListResource, blueprint='api', endpoint='roleslistresource')
  docs.register(updateRoles, blueprint='api', endpoint='updateroles')
  #registro de endpoints de permisos
  docs.register(PermisosListResource, blueprint='api', endpoint='permisoslistresource')
  docs.register(updatePermisos, blueprint='api', endpoint='updatepermisos')
  return app
