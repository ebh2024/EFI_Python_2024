import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from config import Config
from models import db, User
from schemas import ma
from views import api
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
ma.init_app(app)
jwt = JWTManager(app)
swagger = Swagger(app)

with app.app_context():
    db.create_all()

@app.before_request
def create_admin_user():
    existing_user = User.query.filter_by(username="admin").first()
    if not existing_user:
        admin_user = User(
            username="admin",
            password_hash=generate_password_hash("admin"),
            is_admin=True
        )
        try:
            db.session.add(admin_user)
            db.session.commit()
            print("Usuario admin creado exitosamente.")
        except Exception as e:
            db.session.rollback()
            print(f"Error al crear el usuario admin: {e}")
    else:
        print("El usuario admin ya existe.")

app.register_blueprint(api, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
