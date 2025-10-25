import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:4rfvgy7ujm@localhost:5432/app'
    # Example for local PostgreSQL:
    # SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost:5432/app'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'a-jwt-secret-key'
