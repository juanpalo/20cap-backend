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
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "db.sqlite")
db = SQLAlchemy(app)
ma = Marshmallow(app)

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(300), unique=False)
    

    def __init__(self, message):
        self.message = message


class NewsSchema(ma.Schema):
    class Meta:
        fields = ("message", "id")

news_schema = NewsSchema()
manynews_schema = NewsSchema(many=True)

# Endpoint to create a new message
@app.route("/message", methods=["POST"])
def add_message():
    message = request.json["message"]

    new_message = News(message)

    db.session.add(new_message)
    db.session.commit()

    message = News.query.get(new_message.id)

    return news_schema.jsonify(message)

# Endpoint to query all messages
@app.route("/messages", methods=["GET"])
def get_messages():
    all_messages = News.query.all()
    result = manynews_schema.dump(all_messages)
    return jsonify(result)

    # all_products = Shop.query.all()
    # result = shops_schema.dump(all_products)
    # return jsonify(result)

# Endpoint for querying a single message
@app.route("/message/<id>", methods=["GET"])
def get_message(id):
    message = News.query.get(id)
    return news_schema.jsonify(message)

# Endpoint for updating a message
@app.route("/message/<id>", methods=["PUT"])
def message_update(id):
    message = News.query.get(id)
    
    message = request.json["message"]

    message.message = message

    db.session.commit()
    return news_schema.jsonify(message)

# Endpoint for deleting a message
@app.route("/message/<id>", methods=["DELETE"])
def message_delete(id):
    message = News.query.get(id)
    db.session.delete(message)
    db.session.commit()

    return "Message was successfully deleted"

if __name__ == "__main__":
    app.run(debug=True)