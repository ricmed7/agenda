import re

def split(string, brackets_on_first_result=False):
  matches=re.split("[\[\]]+",string)
  matches.remove('')
  return matches

def mr_parse(params):
  results={}
  for key in params.keys():
    if'[' in key:
      key_list=split(key)
      d=results
      for partial_key in key_list[:-1]:
        if partial_key not in d:
          d[partial_key]=dict()
        d=d[partial_key]
      d[key_list[-1]]=params[key]
    else:
      results[key]=params[key]
  return results

def get_data(class_model, class_schema, exclude_fields, query_params, many=False):
  data=class_model.query
  page={}
  qparams=mr_parse(query_params)

  if qparams:
    if "filter" in qparams:
      for atributo, valor in qparams['filter'].items():
        try:
          if str(getattr(class_model, atributo).property.columns[0].type)=='BOOLEAN' or str(getattr(class_model, atributo).property.columns[0].type)=='DATE':
            data=data.filter(getattr(class_model,atributo)==valor)
          else:
            data=data.filter(getattr(class_model,atributo).ilike(f'%{valor}%'))
        except AttributeError:
          return {'error':{'status':400, 'title':'Peticion incorrecta','details':f'El objeto {getattr(class_model, "__name__")}no tiene el atributo{atributo}'}},400
    if "sort" in qparams:
      campos=query_params['sort'].split(',')
      for field in campos:
        field=field.strip()
        try:
          if field[0]=='-':
            field=field.replace('-','')
            data=data.order_by(getattr(class_model,field).desc())
          else:
            #field=field.replace('+','')
            data=data.order_by(getattr(class_model,field))
        except AttributeError:      
          return {'error':{'status':400, 'title':'Peticion incorrecta','details':f'El objeto {getattr(class_model, "__name__")}no tiene el atributo{atributo}'}},400
    if "page" in qparams:
      try:
        number=int(qparams['page']['number'])
        size=int(qparams['page']['size'])
      except ValueError:
        return {'error':{'status':400, 'title':'Peticion incorrecta','details':f'El objeto page[number] y page[size] deben de ser numeros'}},400
      except KeyError:
        return {'error':{'status':400, 'title':'Peticion incorrecta','details':f'parametos page[number] y page[size], deben ser enviados simultaneamente'}},400
      data =data.paginate(page=number, per_page=size)
      page['current-page']=data.page #indica en que pagina se encuentra
      page['per-page']=data.per_page #indica la cantidad de datos que tiene cada pagina
      page['from']=data.first #indica el intervalo de registros
      page['to']=data.last 
      page['total']=data.total
      page['last-page']=data.pages
    if "include" in qparams:
      relations=qparams['include'].split(',')
      for rel in relations:
        rel=rel.strip()
        if rel in exclude_fields:
          exclude_fields.remove(rel)
        else:
          return {'error':{'status':400, 'title':'Peticion incorrecta','details':f'El objeto {getattr(class_model,"__name__")}no tiene relacion con{rel}'}},400
  else:
    data=data.all()

  data_schema=class_schema(many=many, exclude=exclude_fields)
  return {'data':data_schema.dump(data),'meta':{'page':page}}, 200