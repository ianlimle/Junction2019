from flask import Flask, jsonify
from flask_migrate import Migrate
from config import app_config
from flask import request, Flask
from .FaceAnalysis import FacePlus, MergeFace
import glob
from models import Product
from flask_pymongo import PyMongo

import requests
import time

print("Initilizing...")
ANALYZER = FacePlus()
MERGER = MergeFace()
mongo = PyMongo()

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
    mongo.init_app(app)
    print(app.config["SQLALCHEMY_DATABASE_URI"])
    face_collection = mongo.db.faces
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
            try:
                unique_id = int(request.form.get("unique_id"))

            except Exception as e:
                print("Unique_id must be an integer")
            print("Unique_id is ", unique_id)

            filename = str(unique_id) + ".jpg"

            filename_full = FOLDER_NAME + "/" + filename
            face_collection.insert(dict(face_id=unique_id, file_path=filename_full, stage = 1))

            file.save(filename_full)
            # TODO: Delete once upload is complete
            print("File Saved at {}".format(filename_full))

            return dict(message="Upload success"), 200

        else:
            return dict(message = "Method not allowed: Use POST request instead"), 400



    @app.route('/image/analyse/<int:unique_id>', methods=["GET"])
    def analyse_image(unique_id):
        print("Analyese ", unique_id)
        if unique_id is None:
            return dict(message="unique_id cannot be blank"), 400

        if not validate_unique_id(unique_id):
            return dict(
                message=f"Image with unique_id {unique_id} is not found, make sure you have uploaded it at HOST:PORT/image/upload"), 404

        query_file_name = get_full_file_path(unique_id)
        ANALYZER.file = query_file_name
        print("Sending Analyze API call to F++")
        ret = ANALYZER.run()
        print("RET", ret)
        severity = ret[0][0]
        bounding_box = ret[0][1]
        gender = ret[1]

        # face_collection.
        output =  dict(condition="Acne",
                    severity = severity,
                    bounding_box = bounding_box,
                    gender = gender,
                    stage = 2)

        updated = face_collection.find_one_and_update({"face_id": unique_id},
                                         {"$set": output}, upsert=True)

        print(updated)

        return output, 200

    @app.route('/image/products/<int:unique_id>', methods=["GET"])
    def get_products(unique_id):
        print(unique_id)
        products = Product.find_by_severity(1)[:3]
        product_obj_list = [p.serialize() for p in products]

        updated = face_collection.find_one_and_update({"face_id": unique_id},
                                                      {"$set": {
                                                          "recommended_products" : product_obj_list,
                                                          "stage": 3
                                                      }}, upsert=True)
        output = dict(data = product_obj_list)
        print(output)

        return output, 200


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

        # MERGER.template_path = get_full_file_path(unique_id)
        MERGER.template_path = "/Users/lionellloh/Desktop/acne.jpg"
        print(get_full_file_path(unique_id))
        MERGER.merge_path = MODEL_FACE_PATH
        rectangle_box = [70,80,100,100]
        MERGER.template_rectangle = "{},{},{},{}".format(rectangle_box[0], rectangle_box[1], rectangle_box[2],
                                                            rectangle_box[3])

        merged_image = MERGER.run()
        updated = face_collection.find_one_and_update({"face_id": unique_id},
                                                      {"$set": {
                                                          "merged_image": merged_image,
                                                          "stage": 4
                                                      }}, upsert=True)
        return {"merged_image": merged_image}, 200


    return app