#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import sys
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
import datetime
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database


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
      
      

      
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
      
  #get all venues in a certain city and display them
  data=[]
  cities = Venue.query.distinct(Venue.city).all() #getting records with distinct cities => getting all possible cities
  for city in cities:
    CityData = {
    "city": city.city,
    "state": city.state,
    "venues": []
    }
    
    venues = Venue.query.filter_by(city=city.city).all()
    for venue in venues:
      venueDetails = {
      "id": venue.id,
      "name": venue.name
      }
      CityData.get('venues').append(venueDetails)
    
    
    data.append(CityData)
  
  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term = request.form.get('search_term')
  venues = Venue.query.filter(Venue.name.ilike(f"%{search_term}%")).all()
  print(venues)
  data = []
  for venue in venues:
        _data = {
          'id': venue.id,
          'name': venue.name
        }
        data.append(_data)
        
  response = {
    'count': len(venues),
    'data': data
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  # NOTE: The below segment inefficent, must be a better optimal way.. optimize later if possible?

  venue = Venue.query.get(venue_id)

  past_shows_count = past_shows = db.session.query(Artist).join(Show).filter(Show.start_time < datetime.datetime.now(), Show.venue_id == venue.id).count()
  past_shows = db.session.query(Artist).join(Show).filter(Show.start_time < datetime.datetime.now(), Show.venue_id == venue.id).all()

  past_shows_data = []
  for show in past_shows:
    show_info = {
    'artist_id': show.id,
    'artist_name': show.name,
    'artist_image_link': show.image_link,
    'start_time': str(Show.query.filter_by(artist_id = show.id, venue_id = venue.id).first().start_time)
    }
    past_shows_data.append(show_info)

  upcoming_shows_count = db.session.query(Artist).join(Show).filter(Show.start_time > datetime.datetime.now(), Show.venue_id == venue.id).count()
  upcoming_shows = db.session.query(Artist).join(Show).filter(Show.start_time > datetime.datetime.now(), Show.venue_id == venue.id).all()

  upcoming_shows_data = []
  for show in upcoming_shows:
    show_info = {
    'artist_id': show.id,
    'artist_name': show.name,
    'artist_image_link': show.image_link,
    'start_time': str(Show.query.filter_by(artist_id = show.id,venue_id = venue.id).first().start_time)
    }
    upcoming_shows_data.append(show_info)
  # ----DEBUG----
  # print("Past shows:")
  # print(past_shows)
  # print(past_shows_count)
  # print("Upcoming shows:")
  # print(upcoming_shows)
  # print(upcoming_shows_count)
  # -----------------
  data = {
    'id' : venue.id,
    'name' : venue.name,
    'genres' : venue.genres,
    'address' : venue.address,
    'city' : venue.city,
    'state': venue.state,
    'phone': venue.phone,
    'past_shows': past_shows_data,
    'upcoming_shows': upcoming_shows_data,
    'past_shows_count': past_shows_count,
    'upcoming_shows_count': upcoming_shows_count
  }
  
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  try:
    data = request.form
    print(data['name'])
    venue = Venue(name=data['name'], city=data['city'], state=data['state'], address=data['address'], phone=data['phone'], genres=data.getlist('genres'),facebook_link=data['facebook_link'])
    db.session.add(venue)
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except:
    db.session.rollback()
    print(sys.exc_info())
    flash('Venue ' + request.form['name'] + ' was not listed! Something wrong happened!')

  finally:
    db.session.close()

  
  return render_template('pages/home.html')

  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
    Venue.query.delete(venue_id)
    db.session.commit()
  except:
    db.session.rollback()
    print(sys.exc_info())
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  
  data=[] 
  artists = Artist.query.all()
  for artist in artists:
    _data = {
    "id": artist.id,
    "name": artist.name
    }
    data.append(_data)
    
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term = request.form.get('search_term')
  artists = Artist.query.filter(Artist.name.ilike(f"%{search_term}%")).all()
  print(artists)
  data = []
  for artist in artists:
        _data = {
          'id': artist.id,
          'name': artist.name
        }
        data.append(_data)
        
  response = {
    'count': len(artists),
    'data': data
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # NOTE: optimization possibly(?)
  artist = Artist.query.get(artist_id)
  past_shows_count = db.session.query(Venue).join(Show).filter(Show.start_time < datetime.datetime.now(), Show.artist_id == artist.id).count()
  past_shows = db.session.query(Venue).join(Show).filter(Show.start_time < datetime.datetime.now(), Show.artist_id == artist.id).all()

  past_shows_data = []
  for show in past_shows:
    show_info = {
    'venue_id': show.id,
    'venue_name': show.name,
    'venue_image_link': show.image_link,
    'start_time': str(Show.query.filter_by(venue_id = show.id, artist_id = artist.id).first().start_time)
    }
    past_shows_data.append(show_info)
  
  upcoming_shows_count = db.session.query(Venue).join(Show).filter(Show.start_time > datetime.datetime.now(), Show.artist_id == artist.id).count()
  upcoming_shows = db.session.query(Venue).join(Show).filter(Show.start_time > datetime.datetime.now(), Show.artist_id == artist.id).all()

  upcoming_shows_data = []
  for show in upcoming_shows:
    show_info = {
    'venue_id': show.id,
    'venue_name': show.name,
    'venue_image_link': show.image_link,
    'start_time': str(Show.query.filter_by(venue_id = show.id, artist_id = artist.id).first().start_time)
    }
    upcoming_shows_data.append(show_info)

  data = {
    'id' : artist.id,
    'name' : artist.name,
    'genres' : artist.genres,
    'city' : artist.city,
    'state': artist.state,
    'phone': artist.phone,
    'facebook_link': artist.facebook_link,
    'past_shows': past_shows_data,
    'past_shows_count': past_shows_count,
    'upcoming_shows': upcoming_shows_data,
    'upcoming_shows_count': upcoming_shows_count
  }

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)

  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  try:
    data = request.form
    artist = Artist.query.get(artist_id)
    artist.name = data['name']
    artist.city = data['city']
    artist.state = data['state']
    artist.phone = data['phone']
    artist.genres = data.getlist('genres')
    artist.facebook_link = data['facebook_link']
    db.session.add(artist)
    db.session.commit()
  except:
    print(sys.exc_info())
    db.session.rollback()
  finally:
    db.session.close()
    
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)

  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):

  try:
    data = request.form
    print(data.getlist('genres'))
    venue = Venue.query.get(venue_id)
    venue.name = data['name']
    venue.city = data['city']
    venue.state = data['state']
    venue.phone = data['phone']
    venue.genres = data.getlist('genres')
    venue.address = data['address']
    venue.facebook_link = data['facebook_link']
    db.session.add(venue)
    db.session.commit()
  except:
    print(sys.exc_info())
    db.session.rollback()
  finally:
    db.session.close()

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():

  try:
    data = request.form
    print(data['name'])
    artist = Artist(name=data['name'], city=data['city'], state=data['state'], phone=data['phone'], genres=data.getlist('genres'),facebook_link=data['facebook_link'])
    db.session.add(artist)
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except:
    db.session.rollback()
    print(sys.exc_info())
    flash('Artist ' + request.form['name'] + ' was not listed! Something wrong happened!')

  finally:
    db.session.close()

  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  # assuming only future shows should be displayed
  shows = Show.query.filter(Show.start_time > datetime.datetime.now()).all()
  print(shows)
  data = []
  for show in shows:
    venue = Venue.query.filter_by(id = show.venue_id).first()
    artist = Artist.query.filter_by(id = show.artist_id).first()
    _data = {
    'venue_id': show.venue_id,
    'venue_name': venue.name,
    'artist_id': show.artist_id,
    'artist_name': artist.name,
    'artist_image_link': artist.image_link,
    'start_time': str(show.start_time)
    }
    data.append(_data)

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  try:
    data = request.form
    show = Show(artist_id=data['artist_id'],venue_id=data['venue_id'],start_time=data['start_time'])
    db.session.add(show)
    db.session.commit()
    flash('Show was successfully listed!')
  except:
    print(sys.exc_info())
    db.session.rollback()
    flash('An error occurred. Show could not be listed.')
  finally:
    db.session.close()

  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
