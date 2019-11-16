from flask import Flask
from flask_migrate import Migrate
from config import app_config
from flask import request, Flask
from .FaceAnalysis import FacePlus

import requests
import time

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    from models import db
    db.init_app(app)

    print(app.config["SQLALCHEMY_DATABASE_URI"])

    migrate = Migrate(app, db)

    @app.route("/", methods=["POST", "GET"])
    def hello():
        return "Hello World from SUTD"


    @app.route('/upload', methods=["POST"])
    def upload_image():

        FOLDER_NAME = "uploaded_faces"
        if request.method == 'POST':

            print(request.data)
            file = request.files["image"]
            print(type(file))
            print(file)
            unique_id = request.form.get("unique_id")
            print(unique_id)
            # filename = "".join(str(time.time()).split(".")) + ".jpg"
            filename = str(unique_id) + ".jpg"

            filename_full = FOLDER_NAME + "/" + filename

            file.save(filename_full)
            # TODO: Delete once upload is complete
            print("File Saved at {}".format(filename_full))

            # os.remove(filename_full)

        else:
            return "Method not allowed: Use POST request instead"

        fp = FacePlus
        return dict(message= "Upload success"), 200




    return app