# Librerías Instaladas
from flask import Blueprint, request, jsonify
from flasgger.utils import swag_from
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError

# Módulos Propios
from models import db, User
from schemas import UserSchema, NestedModelSchema


# Inicialización del Blueprint y los esquemas
api = Blueprint('api', __name__)
user_schema = UserSchema()
nested_model_schema = NestedModelSchema()
nested_models_schema = NestedModelSchema(many=True)

# Rutas de la API

@api.route('/login', methods=['POST'])
@swag_from({
    'summary': 'Login to get JWT token',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string'},
                    'password': {'type': 'string'}
                },
                'required': ['username', 'password']
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'Token generado exitosamente',
            'schema': {
                'type': 'object',
                'properties': {
                    'access_token': {'type': 'string'}
                }
            }
        },
        '401': {
            'description': 'Nombre de usuario o contraseña incorrectos'
        }
    }
})
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token)
    return jsonify({"msg": "Bad username or password"}), 401

@api.route('/users', methods=['POST'])
@jwt_required()
@swag_from({
    'summary': 'Create a new user',
    'parameters': [
        {
            'name': 'Authorization',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'Bearer token'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string'},
                    'password': {'type': 'string'},
                    'is_admin': {'type': 'boolean'}
                },
                'required': ['username', 'password']
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'Usuario creado exitosamente',
            'schema': UserSchema
        },
        '400': {
            'description': 'Nombre de usuario ya existe o error de integridad en la base de datos'
        },
        '403': {
            'description': 'Acceso de administrador requerido'
        }
    }
})
def create_user():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if not current_user or not current_user.is_admin:
        return jsonify({"msg": "Admin access required"}), 403

    username = request.json['username']
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"msg": "Username already exists"}), 400

    new_user = User(
        username=username,
        is_admin=request.json.get('is_admin', False)
    )
    new_user.set_password(request.json['password'])
    try:
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"msg": "Database integrity error"}), 400

    result = user_schema.dump(new_user)
    return jsonify(result)

@api.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
@swag_from({
    'summary': 'Update user details',
    'parameters': [
        {
            'name': 'Authorization',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'Bearer token'
        },
        {
            'name': 'user_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del usuario a editar'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string'},
                    'password': {'type': 'string'},
                    'is_admin': {'type': 'boolean'}
                }
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'Usuario actualizado exitosamente',
            'schema': UserSchema
        },
        '403': {
            'description': 'Acceso de administrador requerido'
        },
        '404': {
            'description': 'Usuario no encontrado'
        },
        '400': {
            'description': 'Error de integridad en la base de datos'
        }
    }
})
def update_user(user_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if not current_user or not current_user.is_admin:
        return jsonify({"msg": "Admin access required"}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    user.username = request.json.get('username', user.username)
    if 'password' in request.json:
        user.set_password(request.json['password'])
    user.is_admin = request.json.get('is_admin', user.is_admin)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"msg": "Database integrity error"}), 400

    result = user_schema.dump(user)
    return jsonify(result)

@api.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
@swag_from({
    'summary': 'Delete a user',
    'parameters': [
        {
            'name': 'Authorization',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'Bearer token'
        },
        {
            'name': 'user_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del usuario a borrar'
        }
    ],
    'responses': {
        '200': {
            'description': 'Usuario borrado exitosamente'
        },
        '403': {
            'description': 'Acceso de administrador requerido'
        },
        '404': {
            'description': 'Usuario no encontrado'
        }
    }
})
def delete_user(user_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if not current_user or not current_user.is_admin:
        return jsonify({"msg": "Admin access required"}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"msg": "User deleted successfully"})

@api.route('/users', methods=['GET'])
@jwt_required()
@swag_from({
    'summary': 'Get all users',
    'parameters': [
        {
            'name': 'Authorization',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'Bearer token'
        }
    ],
    'responses': {
        '200': {
            'description': 'Lista de usuarios',
            'schema': {
                'type': 'array',
                'items': UserSchema
            }
        },
        '403': {
            'description': 'Acceso de administrador requerido'
        }
    }
})
def get_users():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if not current_user or not current_user.is_admin:
        return jsonify({"msg": "Admin access required"}), 403

    all_users = User.query.all()
    result = user_schema.dump(all_users, many=True)
    return jsonify(result)
