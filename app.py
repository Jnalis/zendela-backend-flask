from os import getenv

from marshmallow import Schema, fields
from flask import jsonify, request
from flask_restful import Resource
from flask import Flask
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy

server = Flask(__name__)
api = Api(server)

server.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL')
server.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(server)


class Employee(db.Model):
    fname = db.Column(db.Text)
    mname = db.Column(db.Text)
    lname = db.Column(db.Text)
    number = db.Column(db.Text)
    email = db.Column(db.Text, unique=True, primary_key=True)
    address = db.Column(db.Text)

    def __init__(self, fname, mname, lname, number, email, address):
        self.fname = fname
        self.mname = mname
        self.lname = lname
        self.number = number
        self.email = email
        self.address = address

    def __repr__(self):
        return self


class RegisterSchema(Schema):
    """
    endpoint: /auth/register
    parameters:
        fname: string,
        mname: string,
        lname: string,
        number: string,
        address: string,
        email: string
    """
    fname = fields.Str(required=True)
    mname = fields.Str(required=True)
    lname = fields.Str(required=True)
    number = fields.Str(required=True)
    address = fields.Str(required=True)
    email = fields.Email(required=True)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


class Register(Resource):
    def post(self):
        req_body = request.get_json()

        # validate the request body
        errors = RegisterSchema().validate(req_body)

        if errors:
            return jsonify({"status": 400, "errors": errors})
        print(req_body)
        insert = Employee(req_body["fname"], req_body["mname"], req_body["lname"], req_body["number"],
                          req_body["email"], req_body["address"])
        db.session.add(insert)
        db.session.commit()

        return jsonify({"status": 200, "msg": "Successfully registered"})


# register the resources
api.add_resource(Register, '/auth/register')
api.add_resource(HelloWorld, '/')


@server.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


if __name__ == '__main__':
    db.create_all()
    server.run(debug=True, port=5000)
