from flask_restful import Resource
from flask import request
from app.models import db,Roles, RolesSchema,RolesSwaggerSchema
from passlib.hash import pbkdf2_sha256 as sha256
from app.consultas import get_data
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource

roles_schema=RolesSchema(many=True)
registroroles_schema=RolesSchema()
updateRoles_schema=RolesSchema(partial=True)#con el atributo partial=True, no es necesario enviar todos loa datos
roles_swagger_schema=RolesSwaggerSchema(partial=True)

@doc(description='Endpoin para gestion de roles',params={
  'Authorization':{
    'description':'Authorization HTTP header con JWT token, Ej. Authorization:Bearer sadasdads',
    'in':'header',
    'type':'string',
    #'required':True
  }
},tags=['Roles'])
class RolesListResource(MethodResource, Resource):
  @doc(params={
      'filter[nombre]':{
        'description':'Rol?',
        'in':'query',
        'type':'string'
      },
      'sort':{
        'description':'Orden de registros segun campo Ej. ASC rol Ej. DESC -rol',
        'in':'query',
        'type':'string'
      },
      'include':{
        'description':'Relaciones de tabla que se van a incluir',
        'in':'query',
        'type':'string'
      },
      'page[size]':{
        'description':'Numero de registros por pagina',
        'in':'query',
        'type':'string'
      },
      'page[number]':{
        'description':'Numero de pagina',
        'in':'query',
        'type':'string'
      }
    }
  )
  @jwt_required()
  def get(self):
    '''usuarios = Usuario.query.all() #esta linea de codigo permite recuperar todos los registros de la tablas usuarios
    lista_usuarios = usuario_schema.dump(usuarios)
    return {"lista": lista_usuarios}, 200'''
    relations=[]
    params = request.args.to_dict()
    result=get_data(Roles,RolesSchema,relations,params,many=True)
    return result

  @use_kwargs(roles_swagger_schema,location=('json'))
  @jwt_required() 
  def post(self, **kwargs):
    json_data = request.get_json(force=True)
    error=registroroles_schema.validate(json_data)
    if error:
      return {"error":{"status":422, "title":"No procesable","detail":error}}, 422
    
    registro_roles=Roles(
      nombre = json_data['nombre']   
    )
    db.session.add(registro_roles)
    db.session.commit()
    resultado = registroroles_schema.dump(registro_roles)
    return {"data":resultado}, 201
    
@doc(description='Endpoin para gestion de usuarios',params={
  'Authorization':{
    'description':'Authorization HTTP header con JWT token, Ej. Authorization:Bearer sadasdads',
    'in':'header',
    'type':'string',
    #'required':True
  }
},tags=['Roles'])
class updateRoles(MethodResource, Resource):
  @jwt_required()
  def get(self,rol_id=None):
    get_roles=Roles.query.filter_by(id=rol_id).first()
    if not get_roles:
      return {"error":{"status":404, "title":"No encontrado","detail":"Rol no existe"}}, 404
    resultado=registroroles_schema.dump(get_roles)
    return {"dato":resultado}, 200

  @use_kwargs(roles_swagger_schema,location=('json'))
  @jwt_required() 
  def put(self, rol_id=None, **kwargs):
     get_rol=Roles.query.filter_by(id=rol_id).first()
     if not get_rol:
      return {"error":{"status":404, "title":"No encontrado","detail":"Rol no existe"}}, 404
     json_data = request.get_json(force=True)
     error=updateRoles_schema.validate(json_data)
     if error:
      return {"error":{"status":422, "title":"No procesable","detail":error}}, 422
     get_rol.nombre=json_data.get('nombre',get_rol.nombre)
     
     db.session.commit()
     resultado=registroroles_schema.dump(get_rol)
     return {"dato":resultado}, 200
  @jwt_required()
  def delete(self,rol_id=None):
    #Usuario.query.filter_by(id=usuario_id).delete()#eliminacion fisica de la base de datos
    get_unidad=Roles.query.filter_by(id=rol_id).first()
    if not get_unidad:
      return {"error":{"status":404, "title":"No encontrado","detail":"Rol no existe"}}, 404
    get_unidad.activo=False
    db.session.commit()
    return {"meta":{"mensaje":"eliminado correctamente"}}, 200 

