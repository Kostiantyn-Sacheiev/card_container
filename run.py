from app import app, db
from flask_migrate import upgrade
import os

if __name__ == '__main__':
    with app.app_context():
        if not os.path.exists('app.db'):
            db.create_all()
        upgrade()
    app.run(debug=True)
