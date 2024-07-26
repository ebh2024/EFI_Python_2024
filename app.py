from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import Equipo, Modelo, Categoria, Fabricante, Caracteristica, Stock, Proveedor, Accesorio


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/equipos')
def equipos():
    equipos = Equipo.query.all()
    return render_template('equipos.html', equipos=equipos)

@app.route('/modelos')
def modelos():
    modelos = Modelo.query.all()
    return render_template('modelos.html', modelos=modelos)

@app.route('/categorias')
def categorias():
    categorias = Categoria.query.all()
    return render_template('categorias.html', categorias=categorias)

@app.route('/fabricantes')
def fabricantes():
    fabricantes = Fabricante.query.all()
    return render_template('fabricantes.html', fabricantes=fabricantes)

@app.route('/caracteristicas')
def caracteristicas():
    caracteristicas = Caracteristica.query.all()
    return render_template('caracteristicas.html', caracteristicas=caracteristicas)

@app.route('/stocks')
def stocks():
    stocks = Stock.query.all()
    return render_template('stocks.html', stocks=stocks)

@app.route('/proveedores')
def proveedores():
    proveedores = Proveedor.query.all()
    return render_template('proveedores.html', proveedores=proveedores)

@app.route('/accesorios')
def accesorios():
    accesorios = Accesorio.query.all()
    return render_template('accesorios.html', accesorios=accesorios)



if __name__ == '__main__':
    app.run(debug=True)

