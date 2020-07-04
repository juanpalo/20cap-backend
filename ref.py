from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask import jsonify
import os 


app = Flask(__name__)

CORS(app)
cors = CORS(app, resources={
    r"/*": {
        "origins": "http://localhost:3000"
    }
})

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Shop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=False)
    price = db.Column(db.Integer, unique=False)

    def __init__(self, title, price, id):
        self.title = title
        self.price = price
        self.id = id


class ShopSchema(ma.Schema):
    class Meta:
        fields = ("title", "price", "id")

shop_schema = ShopSchema()
shops_schema = ShopSchema(many=True)

# Endpoint to create a new product
@app.route("/product", methods=["POST"])
def add_product():
    title = request.json["title"]
    price = request.json["price"]

    new_product = Shop(title, price)

    db.session.add(new_product)
    db.session.commit()

    product = Shop.query.get(new_product.id)

    return shop_schema.jsonify(product)

# Endpoint to query all products
@app.route("/products", methods=["GET"])
def get_products():
    all_products = Shop.query.all()
    result = shops_schema.dump(all_products)
    return jsonify(result)

# Endpoint for querying a single guide
@app.route("/product/<id>", methods=["GET"])
def get_product(id):
    product = Shop.query.get(id)
    return shop_schema.jsonify(product)

# Endpoint for updating a product
@app.route("/product/<id>", methods=["PUT"])
def product_update(id):
    product = Shop.query.get(id)
    title = request.json["title"]
    price = request.json["price"]

    product.title = title
    product.price = price

    db.session.commit()
    return shop_schema.jsonify(product)

# Endpoint for deleting a product
@app.route("/product/<id>", methods=["DELETE"])
def product_delete(id):
    product = Shop.query.get(id)
    db.session.delete(product)
    db.session.commit()

    return "Guide was successfully deleted"

if __name__ == "__main__":
    app.run(debug=True)