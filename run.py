'''from flask import Flask

app=Flask(__name__)'''

from app import create_app
app= create_app('config')

@app.route("/")
def index():
  return "principal"

@app.route("/hola",methods=['GET'])
def hola_mundo():
  return "<p>hola richard...</p>"

@app.route("/saludo",methods=['POST'])
def saludo():
  return "saludos con post"
if __name__=='__main__':
  app.run(debug=True);
