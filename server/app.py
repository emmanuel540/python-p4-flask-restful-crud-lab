#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


class Plants(Resource):

    def get(self):
        plants = [plant.to_dict() for plant in Plant.query.all()]
        return make_response(jsonify(plants), 200)

    def post(self):
        data = request.get_json()

        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price'],
        )

        db.session.add(new_plant)
        db.session.commit()

        return make_response(new_plant.to_dict(), 201)


api.add_resource(Plants, '/plants')


class PlantByID(Resource):

    def get(self, id):
        plant = Plant.query.filter_by(id=id).first().to_dict()
        return make_response(jsonify(plant), 200)
    
    
    def delete(self,id):
        deleted_reco = Plant.query.filter_by(id=id).first()
        db.session.delete(deleted_reco)
        db.session.commit()
        response = make_response("",204)
        return response
    @app.route("/plants/<int:id>",methods = ["PATCH"])
    def patch(id):
        patch_by_id = Plant.query.filter_by(id=id).first()

        # Check if the plant with the specified ID exists
        if not patch_by_id:
            return jsonify({"error": "Plant not found"}), 404

        # Parse JSON data from the request's body
        data = request.get_json()

        # Check if data is valid JSON
        if not data:
            return jsonify({"error": "Invalid JSON data"}), 400

        # Update plant attributes based on the JSON data
        for key, value in data.items():
            setattr(patch_by_id, key, value)

        # Commit the changes to the database
        db.session.commit()

        # Convert the updated plant to a dictionary
        response_dict = patch_by_id.to_dict()

        # Return the updated plant as a JSON response
        return jsonify(response_dict), 200


api.add_resource(PlantByID, '/plants/<int:id>')


if __name__ == '__main__':
    app.run(port=5555, debug=True)