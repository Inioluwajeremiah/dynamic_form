import pytest
from app import create_app, db
from app.forms_db import User
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity

class TestConfig:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:qwertyui@localhost:5432/forms_test' # or your database URI for testing
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
    SECRET_KEY = 'test-secret-key'

@pytest.fixture
def app():
    app = create_app(test_config=TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()


def test_register_client(client):
    response = client.post('/register', json={
        'firstname': 'Test User',
        'email': 'test@example.com',
        'password': 'Test123!',
        'role': 'user'
    })

    data = response.get_json()
    assert response.status_code == 200
    assert 'success_message' in data

def test_verify_user(client):
    # Create a test user in the database
    test_user = User(username='Test User', email='test@example.com', role='user')
    db.session.add(test_user)
    db.session.commit()

    # Verify the test user
    response = client.post('/verify-user', json={
        'email': 'test@example.com',
        'code': test_user.otp
    })

    data = response.get_json()
    assert response.status_code == 200
    assert 'success_message' in data

def test_login(client):
    # Create a test user in the database
    hashed_password = generate_password_hash('Test123!')
    test_user = User(username='Test User', email='test@example.com', role='user', password=hashed_password, otp='123456')
    db.session.add(test_user)
    db.session.commit()

    # Log in the test user
    response = client.post('/login', json={
        'email': 'test@example.com',
        'password': 'Test123!'
    })

    data = response.get_json()
    assert response.status_code == 200
    assert 'access_token' in data
    assert 'refresh_token' in data
    assert 'email' in data

def test_refresh_user_token(client, jwt_token):
    headers = {'Authorization': f'Bearer {jwt_token}'}
    response = client.get('/token/refresh', headers=headers)

    data = response.get_json()
    assert response.status_code == 200
    assert 'access' in data
