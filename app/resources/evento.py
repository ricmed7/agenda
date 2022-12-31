from flask_restful import Resource
from flask import request
from app.models import db,Evento, EventoSchema,EventoSwaggerSchema
from passlib.hash import pbkdf2_sha256 as sha256
from app.consultas import get_data
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource

evento_schema=EventoSchema(many=True)
registroevento_schema=EventoSchema()
updateEvento_schema=EventoSchema(partial=True)#con el atributo partial=True, no es necesario enviar todos loa datos
evento_swagger_schema=EventoSwaggerSchema(partial=True)

@doc(description='Endpoin para gestion de eventos',params={
  'Authorization':{
    'description':'Authorization HTTP header con JWT token, Ej. Authorization:Bearer sadasdads',
    'in':'header',
    'type':'string',
    #'required':True
  }
},tags=['Eventos'])
class EventoListResource(MethodResource, Resource):
  @doc(params={
      'filter[institucion]':{
        'description':'Institucion?',
        'in':'query',
        'type':'string'
      },
      'filter[tema]':{
        'description':'Tematica del evento',
        'in':'query',
        'type':'string'
      },
      'filter[lugar]':{
        'description':'Ubicacion del evento',
        'in':'query',
        'type':'string'
      },
      'filter[fecha]':{
        'description':'Fecha de evento Ej. 23/02/2022 o 2022-02-23',
        'in':'query',
        'type':'date'
      },

      'filter[estado]':{
        'description':'Estado del evento',
        'in':'query',
        'type':'string'
      },
      'sort':{
        'description':'Orden de registros segun campo Ej. ASC institucion Ej. DESC -institucion',
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
    relations=["usuarios","usuarios_created","usuarios_approved"]
    params = request.args.to_dict()
    result=get_data(Evento,EventoSchema,relations,params,many=True)
    return result

  @use_kwargs(evento_swagger_schema,location=('json'))
  @jwt_required() 
  def post(self, **kwargs):
    json_data = request.get_json(force=True)
    error=registroevento_schema.validate(json_data)
    if error:
      return {"error":{"status":422, "title":"No procesable","detail":error}}, 422
    
    registro_evento=Evento(
      institucion =json_data['institucion'], #db.Column(db.Text,nullable=False)
      tema = json_data['tema'],#db.Column(db.Text,nullable=False)
      lugar = json_data['lugar'],#db.Column(db.Text,nullable=True)
      fecha = json_data['fecha'],#db.Column(db.Date,nullable=True)
      hora = json_data['hora'],#db.Column(db.Time,nullable=True)
      estado = json_data['estado'],#db.Column(db.String(256),nullable=True)
      activo = json_data['activo'],#db.Column(db.Boolean,nullable=True)
      usuario_id = json_data['usuario_id'],#db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=True)
      aprobado_id = json_data['aprobado_id']#db.Column(db.Integer, db.ForeignKey('usuario.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=True)
    )
    db.session.add(registro_evento)
    db.session.commit()
    resultado = registroevento_schema.dump(registro_evento)
    return {"data":resultado}, 201
@doc(description='Endpoin para gestion de usuarios',params={
  'Authorization':{
    'description':'Authorization HTTP header con JWT token, Ej. Authorization:Bearer sadasdads',
    'in':'header',
    'type':'string',
    #'required':True
  }
},tags=['Eventos'])
class updateEvento(MethodResource, Resource):
  @jwt_required()
  def get(self,evento_id=None):
    get_evento=Evento.query.filter_by(id=evento_id).first()
    if not get_evento:
      return {"error":{"status":404, "title":"No encontrado","detail":"Evento no existe"}}, 404
    resultado=registroevento_schema.dump(get_evento)
    return {"dato":resultado}, 200

  @use_kwargs(evento_swagger_schema,location=('json'))
  @jwt_required() 
  def put(self, evento_id=None, **kwargs):
     get_evento=Evento.query.filter_by(id=evento_id).first()
     if not get_evento:
      return {"error":{"status":404, "title":"No encontrado","detail":"Evento no existe"}}, 404
     json_data = request.get_json(force=True)
     error=updateEvento_schema.validate(json_data)
     if error:
      return {"error":{"status":422, "title":"No procesable","detail":error}}, 422
     get_evento.institucion=json_data.get('institucion',get_evento.institucion)
     get_evento.tema=json_data.get('tema',get_evento.tema)
     get_evento.lugar=json_data.get('lugar',get_evento.lugar)
     get_evento.fecha=json_data.get('fecha',get_evento.fecha)
     get_evento.hora=json_data.get('hora',get_evento.hora)
     get_evento.estado=json_data.get('estado',get_evento.estado)
     get_evento.activo=json_data.get('activo',get_evento.activo)
     get_evento.usuario_id=json_data.get('usuario_id',get_evento.usuario_id)
     get_evento.aprobado_id=json_data.get('aprobado_id',get_evento.aprobado_id)
     db.session.commit()
     resultado=registroevento_schema.dump(get_evento)
     return {"dato":resultado}, 200
  @jwt_required()
  def delete(self,evento_id=None):
    #Usuario.query.filter_by(id=usuario_id).delete()#eliminacion fisica de la base de datos
    get_evento=Evento.query.filter_by(id=evento_id).first()
    if not get_evento:
      return {"error":{"status":404, "title":"No encontrado","detail":"Evento no existe"}}, 404
    get_evento.activo=False
    db.session.commit()
    return {"meta":{"mensaje":"eliminado correctamente"}}, 200 

