import os
from datetime import timedelta

class Config:
    # Secret Key
    SECRET_KEY = os.environ.get('SECRET_KEY')  # or secrets.token_hex(32)
    # PostgreSQL Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)
    MAIL_SERVER = 'smtp.ephphathagc@gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'ephphathagc@gmail.com'
    MAIL_PASSWORD = os.environ.get('APP_PASSWORD')
    MAIL_DEFAULT_SENDER = 'ephphathagc@gmail.com'

class TestConfig(Config):
    # Testing configuration
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL')
    # Set a fixed secret key for testing (do not use a random secret key)
    SECRET_KEY = 'test-secret-key'
    # Optional: Set a shorter token expiration time for testing
    # For example, set the token expiration to 1 hour (3600 seconds)
    # JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=3600)
   