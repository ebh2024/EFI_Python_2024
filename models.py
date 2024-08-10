from app import db


class Equipo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    modelo_id = db.Column(db.Integer, db.ForeignKey('modelo.id'), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    costo = db.Column(db.Float, nullable=False)
    
    modelo = db.relationship('Modelo', back_populates='equipos')
    categoria = db.relationship('Categoria', back_populates='equipos')
    stocks = db.relationship('Stock', backref='equipo', lazy=True)

class Modelo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    fabricante_id = db.Column(db.Integer, db.ForeignKey('fabricante.id'), nullable=False)
    
    fabricante = db.relationship('Fabricante', back_populates='modelos')
    equipos = db.relationship('Equipo', back_populates='modelo')

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    
    equipos = db.relationship('Equipo', back_populates='categoria')

class Fabricante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    pais_origen = db.Column(db.String(80))
    
    modelos = db.relationship('Modelo', back_populates='fabricante')

class Caracteristica(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(80), nullable=False)
    descripcion = db.Column(db.String(200))
    
class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipo_id = db.Column(db.Integer, db.ForeignKey('equipo.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    ubicacion = db.Column(db.String(100), nullable=False)


    def __init__(self, equipo_id, cantidad, ubicacion):
        self.equipo_id = equipo_id
        self.cantidad = cantidad
        self.ubicacion = ubicacion

class Proveedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    contacto = db.Column(db.String(80), nullable=False)
    
class Accesorio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(80), nullable=False)
    modelo_id = db.Column(db.Integer, db.ForeignKey('modelo.id'), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)  
    
    modelo = db.relationship('Modelo', back_populates='accesorios')


Modelo.accesorios = db.relationship('Accesorio', back_populates='modelo')
Equipo.stock = db.relationship('Stock', uselist=False, back_populates='equipo')
