import os
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "test.db"))
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class Activity(db.Model):
    ip = db.Column(db.String(20), unique=False, nullable=False, primary_key=True)
    user = db.Column(db.String(80), unique=False, nullable=False)
    product = db.Column(db.String(80), unique=False, nullable=False, primary_key=True)
    action = db.Column(db.String(80), unique=False, nullable=False, primary_key=True)
    request = db.Column(db.String(1024), unique=False, nullable=False)
    timestamp = db.Column(db.Datetime(), unique=False, nullable=False, primary_key=True)


@app.route("/log", methods=["POST"])
def log():
    activity = Activity(product=request.json["product"])
    db.session.add(activity)
    db.session.commit()
    return jsonify({"status": 200, "message": "Logged activity."})
  

@app.route("/", methods=["GET"])
def all():
    activities = Activity.query.all()
    return render_template("index.html", activities=activities)


if __name__ == "__main__":
    app.run(debug=True)