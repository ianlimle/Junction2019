from flask import Flask, jsonify
from flask_migrate import Migrate
from config import app_config
from flask import request, Flask
from .FaceAnalysis import FacePlus
import glob
from models import Product

import requests
import time

print("Initilizing...")
ANALYZER = FacePlus()

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
            return dict(message = "Method not allowed: Use POST request instead"), 400



    @app.route('/image/analyse/<int:unique_id>', methods=["GET"])
    def analyse_image(unique_id):
        ABS_BASE_PATH = "/Users/lionellloh/PycharmProjects/junction_finland/sk5_backend/uploaded_faces"
        if unique_id is None:
            return dict(message="unique_id cannot be blank"), 400

        files = glob.glob(f"{ABS_BASE_PATH}/*.jpg")
        query_file_name = f"{ABS_BASE_PATH}/{unique_id}.jpg"
        print(files)
        print(query_file_name)
        if query_file_name not in files:
            return dict(message=f"Image with unique_id {unique_id} is not found, make sure you have uploaded it at HOST:PORT/image/upload"), 404


        ANALYZER.file = query_file_name
        ret = ANALYZER.run()
        # print(ret)
        severity = ret[0][0]
        bounding_box = ret[0][1]
        gender = ret[1]

        return dict(condition="Acne",
                    severity = severity,
                    bounding_box = bounding_box,
                    gender = gender), 200

    @app.route('/image/products/<int:unique_id>', methods=["GET"])
    def get_products(unique_id):
        products = Product.find_by_severity(1)[:3]
        product_obj_list = [p.serialize() for p in products]

        return dict(data = product_obj_list), 200


    # @app.route('/image/merge/<int:unique_id>', methods = ["GET"])


        # template_image = "/mnt/c/Users/Kevin/Documents/Kevin_Documents/Hackathon/JunctionX/Faceplus/nov_test/acne_14.jpg"
        # hello.file = template_image
        # hello_return = hello.run()
        # rectangle_box = hello_return[0][1]
        # gender = hello_return[1]
        # print(gender)
        #
        # merge = MergeFace()
        # merge.template_path = r"{}".format(template_image)
        # if gender == 'Female':
        #     # CHANGE PATH: Female model
        #     merge.merge_path = r"/mnt/c/Users/Kevin/Documents/Kevin_Documents/Hackathon/JunctionX/images/hass/makeup3.jpg"
        # else:
        #     # CHANGE PATH: Male model
        #     merge.merge_path = r"/mnt/c/Users/Kevin/Documents/Kevin_Documents/Hackathon/JunctionX/Faceplus/test2/male_face.jpg"
        # merge.template_rectangle = "{}, {}, {}, {}".format(rectangle_box[0], rectangle_box[1], rectangle_box[2],
        #                                                    rectangle_box[3])
        # print(merge.template_rectangle)
        # merge.run()

        # return dict(message= "Upload success"), 200




    return app