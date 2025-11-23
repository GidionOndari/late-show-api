import os
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from server.models import db, Episode, Guest, Appearance

#  Create Flask App
def create_app():
    app = Flask(__name__)

    # Ensure the folder for the database exists
    db_folder = os.path.join(os.path.dirname(__file__), 'server')
    os.makedirs(db_folder, exist_ok=True)
    db_path = os.path.join(db_folder, 'app.db')

    # Configure database
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    Migrate(app, db)
    api = Api(app)

    # Base Route
    @app.route("/")
    def index():
        return jsonify({"message": "Late Show API Running!"})

    # Episodes
    class EpisodesResource(Resource):
        def get(self):
            episodes = Episode.query.all()
            return [e.to_dict() for e in episodes], 200

    class EpisodeDetailResource(Resource):
        def get(self, id):
            ep = Episode.query.get(id)
            if not ep:
                return {"error": "Episode not found"}, 404
            data = ep.to_dict()
            data['appearances'] = [a.to_dict() for a in ep.appearances]
            return data, 200

        def delete(self, id):
            ep = Episode.query.get(id)
            if not ep:
                return {"error": "Episode not found"}, 404
            db.session.delete(ep)
            db.session.commit()
            return "", 204

    api.add_resource(EpisodesResource, '/episodes')
    api.add_resource(EpisodeDetailResource, '/episodes/<int:id>')

    # Guests
    class GuestsResource(Resource):
        def get(self):
            guests = Guest.query.all()
            return [g.to_dict() for g in guests], 200

    api.add_resource(GuestsResource, '/guests')

    #  Appearances
    class AppearancesResource(Resource):
        def post(self):
            data = request.get_json()
            errors = []

            # Validate required fields
            for key in ('rating', 'episode_id', 'guest_id'):
                if key not in data:
                    errors.append(f"{key} is required")
            if errors:
                return {"errors": errors}, 400

            try:
                rating = int(data['rating'])
                new = Appearance(
                    rating=rating,
                    episode_id=data['episode_id'],
                    guest_id=data['guest_id']
                )
                db.session.add(new)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return {"errors": [str(e)]}, 400

            # Nested response
            result = new.to_dict()
            result['episode'] = new.episode.to_dict()
            result['guest'] = new.guest.to_dict()
            return result, 201

    api.add_resource(AppearancesResource, '/appearances')

    return app

# Run App
if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()  # Creates tables
    app.run(port=5555, debug=True)
