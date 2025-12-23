import os
os.environ['FLASK_ENV'] = 'production'

from app import create_app, db
from sqlalchemy import inspect


app = create_app()

with app.app_context():
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    print("Tablas",tables)

if __name__ == '__main__':
    # Configuración SSL con certificados de Let's Encrypt
    ssl_context = (
        "/home/ubuntu/certs/fullchain.pem",
        "/home/ubuntu/certs/privkey.pem"
    )
    app.run(host='0.0.0.0', port=5000, debug=False, ssl_context=ssl_context)

