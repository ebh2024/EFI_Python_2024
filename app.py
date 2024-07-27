import os
from flask import Flask, render_template, url_for, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from forms import EquipoForm, ModeloForm


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)  # Esto genera una clave secreta aleatoria

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)

from models import Equipo, Modelo, Categoria, Fabricante, Caracteristica, Stock, Proveedor, Accesorio

def populate_choices(form):
    form.modelo_id.choices = [(modelo.id, modelo.nombre) for modelo in Modelo.query.all()]
    form.categoria_id.choices = [(categoria.id, categoria.nombre) for categoria in Categoria.query.all()]

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/equipos')
def equipos():
    equipos = Equipo.query.all()
    return render_template('equipos.html', equipos=equipos)

@app.route('/equipo/new', methods=['GET', 'POST'])
def new_equipo():
    form = EquipoForm()
    populate_choices(form)
    if form.validate_on_submit():
        equipo = Equipo(nombre=form.nombre.data, modelo_id=form.modelo_id.data, categoria_id=form.categoria_id.data, costo=form.costo.data)
        db.session.add(equipo)
        db.session.commit()
        flash('Equipo creado exitosamente.', 'success')
        return redirect(url_for('equipos'))
    return render_template('equipo_form.html', form=form, legend='Nuevo Equipo')

@app.route('/equipo/<int:id>/update', methods=['GET', 'POST'])
def update_equipo(id):
    equipo = Equipo.query.get_or_404(id)
    form = EquipoForm()
    populate_choices(form)
    if request.method == 'GET':
        form.nombre.data = equipo.nombre
        form.modelo_id.data = equipo.modelo_id
        form.categoria_id.data = equipo.categoria_id
        form.costo.data = equipo.costo
    if form.validate_on_submit():
        equipo.nombre = form.nombre.data
        equipo.modelo_id = form.modelo_id.data
        equipo.categoria_id = form.categoria_id.data
        equipo.costo = form.costo.data
        db.session.commit()
        flash('Equipo actualizado exitosamente.', 'success')
        return redirect(url_for('equipos'))
    return render_template('equipo_form.html', form=form, legend='Actualizar Equipo')

@app.route('/equipo/<int:id>/delete', methods=['POST'])
def delete_equipo(id):
    equipo = Equipo.query.get_or_404(id)
    db.session.delete(equipo)
    db.session.commit()
    flash('Equipo eliminado exitosamente.', 'success')
    return redirect(url_for('equipos'))

@app.route('/modelos')
def modelos():
    modelos = Modelo.query.all()
    return render_template('modelos.html', modelos=modelos)

@app.route('/modelo/new', methods=['GET', 'POST'])
def new_modelo():
    form = ModeloForm()
    form.fabricante_id.choices = [(f.id, f.nombre) for f in Fabricante.query.all()]
    if form.validate_on_submit():
        modelo = Modelo(nombre=form.nombre.data, fabricante_id=form.fabricante_id.data)
        db.session.add(modelo)
        db.session.commit()
        flash('Modelo creado exitosamente.', 'success')
        return redirect(url_for('modelos'))
    return render_template('modelo_form.html', form=form, legend='Nuevo Modelo')

@app.route('/modelo/<int:id>/update', methods=['GET', 'POST'])
def update_modelo(id):
    modelo = Modelo.query.get_or_404(id)
    form = ModeloForm()
    form.fabricante_id.choices = [(f.id, f.nombre) for f in Fabricante.query.all()]
    if request.method == 'GET':
        form.nombre.data = modelo.nombre
        form.fabricante_id.data = modelo.fabricante_id
    if form.validate_on_submit():
        modelo.nombre = form.nombre.data
        modelo.fabricante_id = form.fabricante_id.data
        db.session.commit()
        flash('Modelo actualizado exitosamente.', 'success')
        return redirect(url_for('modelos'))
    return render_template('modelo_form.html', form=form, legend='Actualizar Modelo')

@app.route('/modelo/<int:id>/delete', methods=['POST'])
def delete_modelo(id):
    modelo = Modelo.query.get_or_404(id)
    db.session.delete(modelo)
    db.session.commit()
    flash('Modelo eliminado exitosamente.', 'success')
    return redirect(url_for('modelos'))

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

#'mysql+pymysql://root:@localhost/database'