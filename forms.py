from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, TextAreaField, FloatField
from wtforms.validators import DataRequired, Length

class EquipoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=1, max=80)])
    modelo_id = SelectField('Modelo', coerce=int)
    categoria_id = SelectField('Categoría', coerce=int)
    costo = FloatField('Costo', validators=[DataRequired()])
    submit = SubmitField('Guardar')


class ModeloForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    fabricante_id = SelectField('Fabricante', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Guardar')
    
    
class CategoriaForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    submit = SubmitField('Guardar')

class FabricanteForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    pais_origen = StringField('País de Origen', validators=[DataRequired()])
    submit = SubmitField('Guardar')

class CaracteristicaForm(FlaskForm):
    tipo = StringField('Tipo', validators=[DataRequired()])
    descripcion = TextAreaField('Descripción', validators=[DataRequired()])
    submit = SubmitField('Guardar')

class StockForm(FlaskForm):
    cantidad = IntegerField('Cantidad', validators=[DataRequired()])
    ubicacion = StringField('Ubicación', validators=[DataRequired()])
    submit = SubmitField('Guardar')

class ProveedorForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    contacto = StringField('Contacto', validators=[DataRequired()])
    submit = SubmitField('Guardar')

class AccesorioForm(FlaskForm):
    tipo = StringField('Tipo de Accesorio', validators=[DataRequired()])
    compatible_con_modelos = StringField('Compatible con Modelos', validators=[DataRequired()])
    categoria_id = SelectField('Categoría', coerce=int)  
    submit = SubmitField('Guardar')
