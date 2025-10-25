import unittest
from app import create_app, db

if __name__ == '__main__':
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        suite = unittest.TestLoader().discover('tests')
        unittest.TextTestRunner(verbosity=2).run(suite)
        db.drop_all()
