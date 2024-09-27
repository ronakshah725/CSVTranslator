import os
from app import create_app, db
from app.models import Mapping, UniversalTemplate

app = create_app(os.getenv('FLASK_ENV') or 'default')

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Mapping': Mapping, 'UniversalTemplate': UniversalTemplate}

if __name__ == '__main__':
    app.run(host='0.0.0.0')