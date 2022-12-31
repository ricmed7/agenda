from flask_restful import Resource
from flask import request
from app.models import db,Usuario, UsuarioSchema, LoginSchema, UsuarioSwaggerSchema
from passlib.hash import pbkdf2_sha256 as sha256
from app.consultas import get_data
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource

usuario_schema=UsuarioSchema(many=True)
registrousuario_schema=UsuarioSchema()
updateUsuario_schema=UsuarioSchema(partial=True)#con el atributo partial=True, no es necesario enviar todos loa datos
usuario_swagger_schema=UsuarioSwaggerSchema(partial=True)

@doc(description='Endpoin para gestion de usuarios',params={
  'Authorization':{
    'description':'Authorization HTTP header con JWT token, Ej. Authorization:Bearer sadasdads',
    'in':'header',
    'type':'string',
    #'required':True
  }
},tags=['Usuarios'])
class UsuarioListResource(MethodResource, Resource):
  @doc(params={
      'filter[nombres]':{
        'description':'Nombres de usuario',
        'in':'query',
        'type':'string'
      },
      'filter[apellidos]':{
        'description':'Apellidos del usuario',
        'in':'query',
        'type':'string'
      },
      'sort':{
        'description':'Orden de registros segun campo Ej. ASC apellidos Ej. DESC -apellidos',
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
    relations=["unidad","roles"]
    params = request.args.to_dict()
    result=get_data(Usuario,UsuarioSchema,relations,params,many=True)
    return result
  
  @use_kwargs(usuario_swagger_schema,location=('json')) 
  @jwt_required()
  def post(self, **kwargs):
    json_data = request.get_json(force=True)
    error=registrousuario_schema.validate(json_data)
    if error:
      return {"error":{"status":422, "title":"No procesable","detail":error}}, 422
    usuario=Usuario.query.filter_by(usuario=json_data['usuario']).first()
    if usuario:
      return {"error":{"status":422, "title":"No procesable","detail":"El usuario ya existe"}}, 422
    registro_usuario=Usuario(
      nombres = json_data['nombres'],
      apellidos = json_data['apellidos'],
      usuario = json_data['usuario'],
      password = sha256.hash(json_data['password']),
      correo = json_data['correo'],
      responsable = json_data['responsable'],
      activo = json_data['activo'],
      unidad_id = json_data['unidad_id']
    )
    db.session.add(registro_usuario)
    db.session.commit()
    resultado = registrousuario_schema.dump(registro_usuario)
    return {"data":resultado}, 201
    
@doc(description='Endpoin para gestion de usuarios',params={
  'Authorization':{
    'description':'Authorization HTTP header con JWT token, Ej. Authorization:Bearer sadasdads',
    'in':'header',
    'type':'string',
    #'required':True
  }
},tags=['Usuarios'])
class updateUsuario(MethodResource, Resource):
  @jwt_required()
  def get(self,usuario_id=None):
    get_usuario=Usuario.query.filter_by(id=usuario_id).first()
    if not get_usuario:
      return {"error":{"status":404, "title":"No encontrado","detail":"Usuario no existe"}}, 404
    resultado=registrousuario_schema.dump(get_usuario)
    return {"dato":resultado}, 200
  @use_kwargs(usuario_swagger_schema,location=('json'))
  @jwt_required() 
  def put(self, usuario_id=None, **kwargs):
     get_usuario=Usuario.query.filter_by(id=usuario_id).first()
     if not get_usuario:
      return {"error":{"status":404, "title":"No encontrado","detail":"Usuario no existe"}}, 404
     json_data = request.get_json(force=True)
     error=updateUsuario_schema.validate(json_data)
     if error:
      return {"error":{"status":422, "title":"No procesable","detail":error}}, 422

     get_usuario.nombres=json_data.get('nombres',get_usuario.nombres)
     get_usuario.apellidos=json_data.get('apellidos',get_usuario.apellidos)
     get_usuario.usuario=json_data.get('usuario',get_usuario.usuario)
     if json_data.get('password') is None:
      get_usuario.password=get_usuario.password
     else:
      sha256.hash(json_data.get('password'))
     get_usuario.correo=json_data.get('correo',get_usuario.correo)
     get_usuario.responsable=json_data.get('responsable',get_usuario.responsable)
     get_usuario.activo=json_data.get('activo',get_usuario.activo)
     get_usuario.unidad_id=json_data.get('unidad_id',get_usuario.unidad_id)
     db.session.commit()
     resultado=registrousuario_schema.dump(get_usuario)
     return {"dato":resultado}, 200
  @jwt_required()
  def delete(self,usuario_id=None):
    #Usuario.query.filter_by(id=usuario_id).delete()#eliminacion fisica de la base de datos
    get_usuario=Usuario.query.filter_by(id=usuario_id).first()
    if not get_usuario:
      return {"error":{"status":404, "title":"No encontrado","detail":"Usuario no existe"}}, 404
    get_usuario.activo=False
    db.session.commit()
    return {"meta":{"mensaje":"eliminado correctamente"}}, 200

@doc(description='Endpoin para autenticacion de usuarios',tags=['Autenticacion'])
class LoginResource(MethodResource, Resource):
  @use_kwargs(LoginSchema(), location=('json'))
  def post(self,**kwargs):
    json_data=request.get_json(force=True)
    #return json_data.get('usuario')
    login_schema=LoginSchema()
    error=login_schema.validate(json_data)
    if error:
      return {"errors": {"status":422, "title":"entidad no procesable", "detail":error}}, 422
    usuario=Usuario.query.filter_by(usuario=json_data.get('usuario')).first()


    if usuario and sha256.verify(json_data.get("password"), usuario.password):
      access_token=create_access_token(identity=usuario.nombres)
      refresh_token=create_refresh_token(identity=usuario.nombres)
      resultado=registrousuario_schema.dump(usuario)
      return{'data':resultado,'meta':{'access_token':access_token,'refresh_token':refresh_token}},200
    else:
      return {'errors':{'status':401,'title':'No autorizado','detail':'Credenciales incorrectas'}}, 401

