from flask import Flask, render_template
from backend.models import *
from flask_sqlalchemy import SQLAlchemy

app=None #INITIAL VALUE

def init_app():
    syncit_app=Flask(__name__)  #OBJECT OF FLASK
    syncit_app.debug=True
    
    syncit_app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///syncit.sqlite3"
    syncit_app.config["SECRET_KEY"] = "2277"

    syncit_app.app_context().push() #DIRECT ACCESS APP BY OTHER MODULES LIKE DATABASE, AUTHENTICATION ETC
    db.init_app(syncit_app)
    print ("SyncIT Application has Started..")
    return app


app=init_app()
from backend.controllers import * #TO IMPORT ALL THE ROUTES



if __name__=="__main__":
    app.run()