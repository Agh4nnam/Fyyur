
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

#Some columns in the models are added but not populated since the frontend does not pass values associated to them, confusion.exe

class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String()), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String()), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(200))
  
  # TODO: implement any missing fields, as a database migration using Flask-Migrate
# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
      __tablename__ = 'shows'
      show_id = db.Column(db.Integer, primary_key=True)
      artist_id = db.Column('artist_id', db.Integer, db.ForeignKey('artists.id'), nullable=False)
      venue_id = db.Column('venue_id', db.Integer, db.ForeignKey('venues.id'), nullable=False)
      start_time = db.Column(db.DateTime, nullable=False)
      