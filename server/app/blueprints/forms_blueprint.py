import json
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.forms_db import User, Forms
from app.status_codes import  HTTP_200_OK, HTTP_201_CREATED, \
    HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED_ACCESS, HTTP_404_NOT_FOUND, \
    HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_204_NO_CONTENT
from functools import wraps
from datetime import datetime

# Create the blueprint instance
form_blueprint = Blueprint('forms', __name__)


def user_only(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        user = User.query.filter_by(id=current_user['id']).first()
        if user and user.role == 'supervisor':
            return func(*args, **kwargs)
        else:
            return jsonify({"message": "You don't have permission to access this page."}), HTTP_401_UNAUTHORIZED_ACCESS

    return wrapper

@form_blueprint.route('/save_form', methods=['POST'])
@jwt_required()
@user_only
def set_and_save_form():
    form_data = request.json.get('form_data')
    json_string = json.dumps(form_data)
    form_title = request.json.get('form_title')
    # import pdb
    # pdb.set_trace()

    # access_token = request.cookies.get('access_token')
    user_id = get_jwt_identity()

    if user_id:
        user = User.query.filter_by(id=user_id).first();
        if user:
            try:
                form = Forms(form_title=form_title,  form_data=json_string)
                db.session.add(form)
                db.session.commit()
                return {"success_message": "Form saved successfully!"}, HTTP_200_OK
            
            except Exception as e:
                return {"error_message": e}
    else:
        return jsonify({'message': 'Unauthorized'}), HTTP_401_UNAUTHORIZED_ACCESS


@form_blueprint.get('/<int:id>')
@jwt_required()
@user_only
def get_form_to_edit(id):
    user_id = get_jwt_identity()
    try:
        form = Forms(id=id, user_id=user_id)
        form_data = form.form_data
        form_data = json.loads(form_data)
        return {'form_title': form.form_title, 'form_data':form_data, 'form_date': form.form_date}, HTTP_200_OK
    
    except Exception as e:
        return {"error_message": e}
    
# after getting forms to edit, pass in the id
@form_blueprint.put('/<int:id>')
@form_blueprint.patch('/<int:id>')
@jwt_required()
@user_only
def save_edited_form(id):
    user_id = get_jwt_identity()
    form = Forms(id=id, user_id=user_id)

    form_data = request.get_json().get('form_data','')
    json_string = json.dumps(form_data)
    form_title = request.get_json().get('form_title','')
    
    try:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
        form = Forms(form_title=form_title,  form_data=json_string)

        form.form_title = form_title
        form.form_data = form_data

        db.session.commit()
        return {"success_message": "Form saved successfully!"}, HTTP_200_OK
    
    except Exception as e:
        return {"error_message": e}

