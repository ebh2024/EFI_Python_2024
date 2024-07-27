from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SelectField, SubmitField
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
