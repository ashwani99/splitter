from app import create_app, db, jwt


app = create_app()
with app.app_context(): 
    db.create_all() # TODO: refactor this

from models import User


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}