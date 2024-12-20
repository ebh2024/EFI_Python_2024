# Librerías Instaladas
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

# Módulos Propios
from models import User, NestedModel


# Inicialización de Marshmallow
ma = Marshmallow()

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True
        exclude = ("password_hash", "nested_models")

class NestedModelSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = NestedModel
        include_fk = True
        load_instance = True

    user = ma.Nested(UserSchema)
