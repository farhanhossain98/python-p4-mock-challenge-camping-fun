#!/usr/bin/env python3

from models import db, Activity, Camper, Signup
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)
validation_errors = {"errors": ["validation errors"]}
# 
# @app.route('/')
# def home():
    # return ''


class Campers(Resource):
    
    def get(self):
        
        campers = Camper.query.all()
        
        campers_dict = [camper.to_dict(rules = ("-signups",)) for camper in campers]
        
        return make_response(campers_dict, 200)
    
    
    def post(self):

        req = request.get_json()

        try:
            camper = Camper(
                name = req.get("name"),
                age = req.get("age")
            )
            db.session.add(camper)
            db.session.commit()
            return make_response(camper.to_dict(rules = ('-signups',)), 201)
        except:
            return make_response(validation_errors, 400) 




class CampersById(Resource):
    
    def get(self, id):
        camper = Camper.query.filter(Camper.id == id).one_or_none()
        # camper = Camper.query.get(id)
        
        print('We are here')
        if camper is None:
            return make_response({"error":"Camper not found"}, 404)
        else:
            return make_response(camper.to_dict(), 200)
    
    def patch(self, id):
        camper = Camper.query.get(id)
        req = request.get_json()
        
        if camper:
            try:
                for attr in req:
                    setattr(camper, attr, req.get(attr))
                db.session.commit()

                return make_response(camper.to_dict(rules = ('-signups',)), 202)
            except:
                return make_response(validation_errors, 400)
                # error 422 
        else:
            return make_response({"error":"Camper not found"}, 404)




class Activities(Resource):

    def get(self):
        activities = Activity.query.all()

        activities_dict = [activitie.to_dict(rules = ("-signups",)) for activitie in activities]

        return make_response(activities_dict, 200)
        


class ActivitiesById(Resource):
    def delete(self, id):
        activity = Activity.query.get(id)
        if activity:
            db.session.delete(activity)
            db.session.commit()
            return make_response({}, 204)
            
        else:
            return make_response({"error":"Activity not found"}, 404)


class Signups(Resource):

    def post(self):
        req = request.get_json()
        try:
            signup = Signup(
                camper_id = req.get("camper_id"),
                activity_id = req.get("activity_id"),
                time = req.get("time")
                )
            db.session.add(signup)
            db.session.commit()
            return make_response(signup.to_dict(), 201)
        except:
            return make_response(validation_errors, 400) 
                # error 422


api.add_resource(Signups, "/signups")
api.add_resource(CampersById, "/campers/<int:id>")
api.add_resource(Campers, "/campers")
api.add_resource(ActivitiesById, "/activities/<int:id>")
api.add_resource(Activities, "/activities")

if __name__ == '__main__':
    app.run(port=5555, debug=True)
