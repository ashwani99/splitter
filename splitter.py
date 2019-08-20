from app import create_app, db, jwt

app = create_app()
with app.app_context(): 
    db.create_all() # TODO: refactor this

from app.models import User, Bill, BillSplit


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Bill': Bill, 'BillSplit': BillSplit}