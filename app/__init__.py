from flask import Flask
from flask_migrate import Migrate
from config import app_config
from flask import request, Flask
import requests
import time

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_name)
    from models import db
    db.init_app(app)

    print(app.config["SQLALCHEMY_DATABASE_URI"])

    migrate = Migrate(app, db)

    @app.route("/")
    def hello():
        return "Hello World from SUTD"

    @app.route('/upload', methods=["POST"])
    def upload_image():
        return "lol"
        FOLDER_NAME = "boards"
        if request.method == 'POST':
            file = request.files['file']

            filename = str(time.time()) + ".jpg"

            filename_full = FOLDER_NAME + "/" + filename

            file.save(filename_full)
            # TODO: Delete once upload is complete
            print("File Saved at {}".format(filename_full))

            # os.remove(filename_full)

        else:
            return "Method not allowed: Use POST request instead"


    return app