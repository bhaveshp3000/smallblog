from app import app,db
from app.models import User
from app.models import S_User

@app.shell_context_processor
def make_shell_context():
    return{'db':db,'User':User,'S_User':S_User}