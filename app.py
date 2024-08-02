import os
from flask import Flask, render_template, url_for, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from forms import EquipoForm, ModeloForm, CategoriaForm, FabricanteForm, CaracteristicaForm, StockForm, ProveedorForm, AccesorioForm




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)  # Esto genera una clave secreta aleatoria

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)

from models import Equipo, Modelo, Fabricante, Accesorio, Caracteristica, Categoria, Stock, Proveedor

def populate_choices(form):
    if isinstance(form, AccesorioForm):
        form.categoria_id.choices = [(categoria.id, categoria.nombre_categoria) for categoria in Categoria.query.all()]
    elif isinstance(form, EquipoForm):
        form.modelo_id.choices = [(modelo.id, modelo.nombre_modelo) for modelo in Modelo.query.all()]
        form.categoria_id.choices = [(categoria.id, categoria.nombre_categoria) for categoria in Categoria.query.all()]
    elif isinstance(form, ModeloForm):
        form.fabricante_id.choices = [(fabricante.id, fabricante.nombre_fabricante) for fabricante in Fabricante.query.all()]

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

@app.route('/categoria/new', methods=['GET', 'POST'])
def new_categoria():
    form = CategoriaForm()
    if form.validate_on_submit():
        categoria = Categoria(nombre=form.nombre.data)
        db.session.add(categoria)
        db.session.commit()
        flash('Categoría creada exitosamente.', 'success')
        return redirect(url_for('categorias'))
    return render_template('categoria_form.html', form=form, legend='Nueva Categoría')

@app.route('/categoria/<int:id>/update', methods=['GET', 'POST'])
def update_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    form = CategoriaForm()
    if request.method == 'GET':
        form.nombre.data = categoria.nombre
    if form.validate_on_submit():
        categoria.nombre = form.nombre.data
        db.session.commit()
        flash('Categoría actualizada exitosamente.', 'success')
        return redirect(url_for('categorias'))
    return render_template('categoria_form.html', form=form, legend='Actualizar Categoría')

@app.route('/fabricantes')
def fabricantes():
    fabricantes = Fabricante.query.all()
    return render_template('fabricantes.html', fabricantes=fabricantes)

@app.route('/new_fabricante', methods=['GET', 'POST'])
def new_fabricante():
    form = FabricanteForm()
    if form.validate_on_submit():
        fabricante = Fabricante(nombre=form.nombre.data, pais_origen=form.pais_origen.data)
        db.session.add(fabricante)
        db.session.commit()
        flash('Fabricante añadido con éxito', 'success')
        return redirect(url_for('fabricantes'))
    return render_template('fabricante_form.html', form=form, legend='Nuevo Fabricante')

@app.route('/edit_fabricante/<int:id>', methods=['GET', 'POST'])
def edit_fabricante(id):
    fabricante = Fabricante.query.get_or_404(id)
    form = FabricanteForm()
    if form.validate_on_submit():
        fabricante.nombre = form.nombre.data
        fabricante.pais_origen = form.pais_origen.data
        db.session.commit()
        flash('Fabricante actualizado con éxito', 'success')
        return redirect(url_for('fabricantes'))
    elif request.method == 'GET':
        form.nombre.data = fabricante.nombre
        form.pais_origen.data = fabricante.pais_origen
    return render_template('fabricante_form.html', form=form, legend='Editar Fabricante')

@app.route('/delete_fabricante/<int:id>', methods=['POST'])
def delete_fabricante(id):
    fabricante = Fabricante.query.get_or_404(id)
    db.session.delete(fabricante)
    db.session.commit()
    flash('Fabricante eliminado con éxito', 'success')
    return redirect(url_for('fabricantes'))



@app.route('/caracteristicas')
def caracteristicas():
    caracteristicas = Caracteristica.query.all()
    return render_template('caracteristicas.html', caracteristicas=caracteristicas)

@app.route('/caracteristica/new', methods=['GET', 'POST'])
def new_caracteristica():
    form = CaracteristicaForm()
    if form.validate_on_submit():
        caracteristica = Caracteristica(tipo=form.tipo.data, descripcion=form.descripcion.data)
        db.session.add(caracteristica)
        db.session.commit()
        flash('Característica creada exitosamente.', 'success')
        return redirect(url_for('caracteristicas'))
    return render_template('caracteristica_form.html', form=form, legend='Nueva Característica')

@app.route('/caracteristica/<int:id>/update', methods=['GET', 'POST'])
def update_caracteristica(id):
    caracteristica = Caracteristica.query.get_or_404(id)
    form = CaracteristicaForm()
    if request.method == 'GET':
        form.tipo.data = caracteristica.tipo
        form.descripcion.data = caracteristica.descripcion
    if form.validate_on_submit():
        caracteristica.tipo = form.tipo.data
        caracteristica.descripcion = form.descripcion.data
        db.session.commit()
        flash('Característica actualizada exitosamente.', 'success')
        return redirect(url_for('caracteristicas'))
    return render_template('caracteristica_form.html', form=form, legend='Actualizar Característica')



@app.route('/stocks')
def stocks():
    stocks = Stock.query.all()
    return render_template('stocks.html', stocks=stocks)

@app.route('/stock/new', methods=['GET', 'POST'])
def new_stock():
    form = StockForm()
    if form.validate_on_submit():
        stock = Stock(cantidad=form.cantidad.data, ubicacion=form.ubicacion.data)
        db.session.add(stock)
        db.session.commit()
        flash('Stock creado exitosamente.', 'success')
        return redirect(url_for('stocks'))
    return render_template('stock_form.html', form=form, legend='Nuevo Stock')

@app.route('/stock/<int:id>/update', methods=['GET', 'POST'])
def update_stock(id):
    stock = Stock.query.get_or_404(id)
    form = StockForm()
    if request.method == 'GET':
        form.cantidad.data = stock.cantidad
        form.ubicacion.data = stock.ubicacion
    if form.validate_on_submit():
        stock.cantidad = form.cantidad.data
        stock.ubicacion = form.ubicacion.data
        db.session.commit()
        flash('Stock actualizado exitosamente.', 'success')
        return redirect(url_for('stocks'))
    return render_template('stock_form.html', form=form, legend='Actualizar Stock')


@app.route('/proveedores')
def proveedores():
    proveedores = Proveedor.query.all()
    return render_template('proveedores.html', proveedores=proveedores)

@app.route('/proveedor/new', methods=['GET', 'POST'])
def new_proveedor():
    form = ProveedorForm()
    if form.validate_on_submit():
        proveedor = Proveedor(nombre=form.nombre.data, contacto=form.contacto.data)
        db.session.add(proveedor)
        db.session.commit()
        flash('Proveedor creado exitosamente.', 'success')
        return redirect(url_for('proveedores'))
    return render_template('proveedor_form.html', form=form, legend='Nuevo Proveedor')

@app.route('/proveedor/<int:id>/update', methods=['GET', 'POST'])
def update_proveedor(id):
    proveedor = Proveedor.query.get_or_404(id)
    form = ProveedorForm()
    if request.method == 'GET':
        form.nombre.data = proveedor.nombre
        form.contacto.data = proveedor.contacto
    if form.validate_on_submit():
        proveedor.nombre = form.nombre.data
        proveedor.contacto = form.contacto.data
        db.session.commit()
        flash('Proveedor actualizado exitosamente.', 'success')
        return redirect(url_for('proveedores'))
    return render_template('proveedor_form.html', form=form, legend='Actualizar Proveedor')

@app.route('/accesorios')
def accesorios():
    accesorios = Accesorio.query.all()
    return render_template('accesorios.html', accesorios=accesorios)

@app.route('/accesorio/new', methods=['GET', 'POST'])
def new_accesorio():
    form = AccesorioForm()
    populate_choices(form)  
    if form.validate_on_submit():
        accesorio = Accesorio(
            tipo=form.tipo.data,
            compatible_con_modelos=form.compatible_con_modelos.data,
            categoria_id=form.categoria_id.data  
        )
        db.session.add(accesorio)
        db.session.commit()
        flash('Accesorio creado con éxito', 'success')
        return redirect(url_for('accesorios'))
    return render_template('accesorio_form.html', form=form, legend='Nuevo Accesorio')

@app.route('/accesorio/<int:id>/update', methods=['GET', 'POST'])
def update_accesorio(id):
    accesorio = Accesorio.query.get_or_404(id)
    form = AccesorioForm()
    populate_choices(form)
    if request.method == 'GET':
        form.tipo.data = accesorio.tipo
        form.modelo_id.data = accesorio.modelo_id
    if form.validate_on_submit():
        accesorio.tipo = form.tipo.data
        accesorio.modelo_id = form.modelo_id.data
        db.session.commit()
        flash('Accesorio actualizado exitosamente.', 'success')
        return redirect(url_for('accesorios'))
    return render_template('accesorio_form.html', form=form, legend='Actualizar Accesorio')



if __name__ == '__main__':
    app.run(debug=True)

#'mysql+pymysql://root:@localhost/database'