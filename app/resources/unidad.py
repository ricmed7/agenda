from flask_restful import Resource
from flask import request
from app.models import db,Unidad, UnidadSchema,UnidadSwaggerSchema
from passlib.hash import pbkdf2_sha256 as sha256
from app.consultas import get_data
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource

unidad_schema=UnidadSchema(many=True)
registrounidad_schema=UnidadSchema()
updateUnidad_schema=UnidadSchema(partial=True)#con el atributo partial=True, no es necesario enviar todos loa datos
unidad_swagger_schema=UnidadSwaggerSchema(partial=True)

@doc(description='Endpoin para gestion de eventos',params={
  'Authorization':{
    'description':'Authorization HTTP header con JWT token, Ej. Authorization:Bearer sadasdads',
    'in':'header',
    'type':'string',
    'required':True
  }
},tags=['Unidad'])
class UnidadListResource(MethodResource, Resource):
  @doc(params={
      'filter[descripcion]':{
        'description':'Descripcion?',
        'in':'query',
        'type':'string'
      },
      'filter[activo]':{
        'description':'Activo',
        'in':'query',
        'type':'string'
      },
      
      'sort':{
        'description':'Orden de registros segun campo Ej. ASC descripcion Ej. DESC -descripcion',
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
    result=get_data(Unidad,UnidadSchema,relations,params,many=True)
    return result

  @use_kwargs(unidad_swagger_schema,location=('json'))
  @jwt_required() 
  def post(self, **kwargs):
    json_data = request.get_json(force=True)
    error=registrounidad_schema.validate(json_data)
    if error:
      return {"error":{"status":422, "title":"No procesable","detail":error}}, 422
    
    registro_unidad=Unidad(
      descripcion = json_data['descripcion'],  
      activo = json_data['activo'] 
    )
    db.session.add(registro_unidad)
    db.session.commit()
    resultado = registrounidad_schema.dump(registro_unidad)
    return {"data":resultado}, 201

@doc(description='Endpoin para gestion de usuarios',params={
  'Authorization':{
    'description':'Authorization HTTP header con JWT token, Ej. Authorization:Bearer sadasdads',
    'in':'header',
    'type':'string',
    #'required':True
  }
},tags=['Unidad'])
class updateUnidad(MethodResource, Resource):
  @jwt_required()
  def get(self,unidad_id=None):
    get_unidad=Unidad.query.filter_by(id=unidad_id).first()
    if not get_unidad:
      return {"error":{"status":404, "title":"No encontrado","detail":"Unidad no existe"}}, 404
    resultado=registrounidad_schema.dump(get_unidad)
    return {"dato":resultado}, 200

  @use_kwargs(unidad_swagger_schema,location=('json')) 
  @jwt_required()
  def put(self, unidad_id=None, **kwargs):
     get_unidad=Unidad.query.filter_by(id=unidad_id).first()
     if not get_unidad:
      return {"error":{"status":404, "title":"No encontrado","detail":"Unidad no existe"}}, 404
     json_data = request.get_json(force=True)
     error=updateUnidad_schema.validate(json_data)
     if error:
      return {"error":{"status":422, "title":"No procesable","detail":error}}, 422
     get_unidad.institucion=json_data.get('descripcion',get_unidad.descripcion)
     get_unidad.lugar=json_data.get('activo',get_unidad.activo)
     
     db.session.commit()
     resultado=registrounidad_schema.dump(get_unidad)
     return {"dato":resultado}, 200
  @jwt_required()
  def delete(self,unidad_id=None):
    #Usuario.query.filter_by(id=usuario_id).delete()#eliminacion fisica de la base de datos
    get_unidad=Unidad.query.filter_by(id=unidad_id).first()
    if not get_unidad:
      return {"error":{"status":404, "title":"No encontrado","detail":"Unidad no existe"}}, 404
    get_unidad.activo=False
    db.session.commit()
    return {"meta":{"mensaje":"eliminado correctamente"}}, 200 

