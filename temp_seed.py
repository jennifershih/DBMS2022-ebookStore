from app import create_app, db
from seed import seed_data

app = create_app()
with app.app_context():
    db.create_all()
    seed_data()
