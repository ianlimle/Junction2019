from models import Product
import pandas as pd
from app import create_app


if __name__ == "__main__":
    from models import db
    app = create_app("development")
    db.init_app(app)
    df = pd.read_csv("../skin_care.csv")
    for i, row in df.iterrows():
        if i > 5:
            break
        print(str(row.product_id))
        with app.app_context():

            new_product = Product(
                    name = row.name,
                    description = row.description,
                    picture = row.picture,
                    price = row.price,
                    url = row.url,
                    product_id = str(row.product_id),
                    currency_id= row.currency_id

                )

            try:
                new_product.save_to_db()

            except Exception as e:
                print("Failed to save to db! " + str(e))




"""
id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(500), unique=True, nullable=False)
    category_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, primary_key=True)
    picture = db.Column(db.String(500), unique=True, nullable=False)
    url = db.Column(db.String(500), unique=True, nullable=False)
    price = db.Column(db.Integer, primary_key=True)
    currency_id = db.Column(db.Integer, primary_key=True)
    problem =  db.Column(db.String(100), unique=True, nullable=True)
    severity =  db.Column(db.String(10), unique=True, nullable=True)
    """

# new_review = LiveReview(
#             asin=asin,
#             username=jwt_username,
#             review_rating=data.review_rating,
#             review_text=data.review_text,
#             unix_timestamp=int(time.time())
#
#         )
#
#         try:
#             new_review.save_to_db()