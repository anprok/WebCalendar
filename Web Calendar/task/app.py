import datetime

from flask import Flask, abort, jsonify
from flask_restful import Api, Resource, inputs, reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
import sys

app = Flask(__name__)

api = Api(app)
parser = reqparse.RequestParser()
get_parser = reqparse.RequestParser()
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///webcalendar.db'


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(80), nullable=False)
    date = db.Column(db.Date, nullable=False)


db.create_all()
parser.add_argument(
    'date',
    type=inputs.date,
    help="The event date with the correct format is required! The correct format is YYYY-MM-DD!",
    required=True
)
parser.add_argument(
    'event',
    type=str,
    help="The event name is required!",
    required=True
)
get_parser.add_argument(
    'start_time',
    type=str,
    help="The start time with the correct format is required! The correct format is YYYY-MM-DD!",
    required=False
)
get_parser.add_argument(
    'end_time',
    type=str,
    help="The end time with the correct format is required! The correct format is YYYY-MM-DD!",
    required=False
)
resource_fields = {
    'id': fields.String,
    'event': fields.String,
    'date': fields.String,
}


class EventsResource(Resource):
    def post(self):
        args = parser.parse_args()
        event = Event(event=args['event'], date=args['date'].date())
        # saves data into the table
        db.session.add(event)
        # commits changes
        db.session.commit()
        response = {
            "message": "The event has been added!",
            "event": args['event'],
            "date": str(args['date'].date())
        }
        return response

    @marshal_with(resource_fields)
    def get(self):
        args = get_parser.parse_args()
        if args['start_time'] is None and args['end_time'] is None:
            return Event.query.all()

        return Event.query.filter(Event.date.between(args['start_time'], args['end_time'])).all()


class EventByIDResource(Resource):

    def get_event(self, event_id):
        event = Event.query.filter(Event.id == event_id).first()
        if event is None:
            abort(404, "The event doesn't exist!")
        return event

    @marshal_with(resource_fields)
    def get(self, event_id):
        return self.get_event(event_id)

    def delete(self, event_id):
        event = self.get_event(event_id)
        db.session.delete(event)
        db.session.commit()
        return jsonify({'message': "The event has been deleted!"})


class EventTodayResource(Resource):
    @marshal_with(resource_fields)
    def get(self):
        return Event.query.filter(Event.date == datetime.date.today()).all()


api.add_resource(EventsResource, '/event')
api.add_resource(EventByIDResource, '/event/<int:event_id>')
api.add_resource(EventTodayResource, '/event/today')

# do not change the way you run the program
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
