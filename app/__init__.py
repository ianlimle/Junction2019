from flask import Flask, jsonify
from flask_migrate import Migrate
from config import app_config
from flask import request, Flask
from .FaceAnalysis import FacePlus, MergeFace
import glob
from models import Product

import requests
import time

print("Initilizing...")
ANALYZER = FacePlus()
MERGER = MergeFace()

ABS_BASE_PATH = "/Users/lionellloh/PycharmProjects/junction_finland/sk5_backend/uploaded_faces"

def validate_unique_id(unique_id):
    files = glob.glob(get_full_file_path(unique_id))
    query_file_name = f"{ABS_BASE_PATH}/{unique_id}.jpg"
    if query_file_name not in files:
        return False

    return True

def get_full_file_path(unique_id):
    return f"{ABS_BASE_PATH}/{unique_id}.jpg"

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


    @app.route('/image/upload', methods=["POST"])
    def upload_image():

        FOLDER_NAME = "uploaded_faces"
        if request.method == 'POST':

            file = request.files["image"]
            print(file)
            unique_id = request.form.get("unique_id")
            print("Unique_id is ", unique_id)
            filename = str(unique_id) + ".jpg"

            filename_full = FOLDER_NAME + "/" + filename

            file.save(filename_full)
            # TODO: Delete once upload is complete
            print("File Saved at {}".format(filename_full))

            return dict(message="Upload success"), 200

        else:
            return dict(message = "Method not allowed: Use POST request instead"), 400



    @app.route('/image/analyse/<int:unique_id>', methods=["GET"])
    def analyse_image(unique_id):
        print(unique_id)
        if unique_id is None:
            return dict(message="unique_id cannot be blank"), 400

        if not validate_unique_id(unique_id):
            return dict(
                message=f"Image with unique_id {unique_id} is not found, make sure you have uploaded it at HOST:PORT/image/upload"), 404

        query_file_name = get_full_file_path(unique_id)
        ANALYZER.file = query_file_name
        ret = ANALYZER.run()
        print("RET", ret)
        severity = ret[0][0]
        bounding_box = ret[0][1]
        gender = ret[1]

        return dict(condition="Acne",
                    severity = severity,
                    bounding_box = bounding_box,
                    gender = gender), 200

    @app.route('/image/products/<int:unique_id>', methods=["GET"])
    def get_products(unique_id):
        print(unique_id)
        products = Product.find_by_severity(1)[:3]
        product_obj_list = [p.serialize() for p in products]

        return dict(data = product_obj_list), 200


    @app.route('/image/merge/<int:unique_id>', methods = ["GET"])
    def get_merged_face(unique_id):
        query_file_name = get_full_file_path(unique_id)
        print(query_file_name)


        gender = "Female"
        if gender == 'Female':
            MODEL_FACE_PATH = "/Users/lionellloh/PycharmProjects/junction_finland/sk5_backend/model_faces/female_face.jpg"
        #
        elif gender == "Male":
            MODEL_FACE_PATH = "/Users/lionellloh/PycharmProjects/junction_finland/sk5_backend/model_faces/male_face.jpg"

        MERGER.template_path = MODEL_FACE_PATH
        MERGER.merge_path = "/Users/lionellloh/PycharmProjects/junction_finland/sk5_backend/output_faces"
        rectangle_box = [-7, 46, 322, 322]
        MERGER.template_rectangle = "{}, {}, {}, {}".format(rectangle_box[0], rectangle_box[1], rectangle_box[2],
                                                           rectangle_box[3])
        print(MERGER.template_rectangle)
        MERGER.run()

        # return dict(message= "Upload success"), 200




    return app