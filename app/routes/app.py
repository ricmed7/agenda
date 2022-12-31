from flask import Blueprint
from flask_restful import Api
from app.resources.usuario import UsuarioListResource,updateUsuario,LoginResource
from app.resources.evento import EventoListResource,updateEvento
from app.resources.unidad import UnidadListResource,updateUnidad
from app.resources.roles import RolesListResource,updateRoles
from app.resources.permisos import PermisosListResource,updatePermisos

api_bp =Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(UsuarioListResource,'/usuarios')
api.add_resource(updateUsuario,'/usuarios/<int:usuario_id>')
api.add_resource(LoginResource,'/login')
api.add_resource(EventoListResource,'/eventos')
api.add_resource(updateEvento,'/eventos/<int:evento_id>')
api.add_resource(UnidadListResource,'/unidad')
api.add_resource(updateUnidad,'/unidad/<int:unidad_id>')
api.add_resource(RolesListResource,'/roles')
api.add_resource(updateRoles,'/roles/<int:rol_id>')
api.add_resource(PermisosListResource,'/permisos')
api.add_resource(updatePermisos,'/permisos/<int:rol_id>')