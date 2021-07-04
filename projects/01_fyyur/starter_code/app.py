#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
from datetime import datetime
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from os import name, sys
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database
migrate = Migrate(app,db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#





class Venue(db.Model):
    __tablename__ = 'venue'


    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, unique=False, default=True)
    seeking_description = db.Column(db.String,default="No description")
    website = db.Column(db.String(500))
    genres = db.Column(db.ARRAY(db.String()))
   
    
    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))   
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String()))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean,unique=False, default=True)
    seeking_description = db.Column(db.String,default="No description")
    # TODO: implement any missing fields, as a database migration using Flask-Migrate


  
class Show(db.Model):
  __tablename__ = "show"
  id = db.Column(db.Integer, primary_key=True)
  artist_id = db.Column(db.Integer,db.ForeignKey('artist.id'),nullable=False)
  venue_id = db.Column(db.Integer,db.ForeignKey('venue.id'),nullable=False)
  start_time = db.Column(db.DateTime,default=datetime.now())

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

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
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  venueslist = Venue.query.all()
  session = db.Session()  
  State_Data = {}
  for ven in venueslist:
    print(ven.name)
    num_upcom_shows = Show.query.filter(Show.venue_id==ven.id).count()
    # print(num_upcom_shows)
    if (ven.city,ven.state) in State_Data:
      State_Data[(ven.city,ven.state)].append({'id':ven.id,
              'name':ven.name,
              'num_upcoming_shows':num_upcom_shows})
    else:
      State_Data[(ven.city,ven.state)]=[]
      State_Data[(ven.city,ven.state)].append({'id':ven.id,
              'name':ven.name,
              'num_upcoming_shows':num_upcom_shows})

    data = []
    for st in State_Data.keys():
      data_element = {'city':st[0],
        'state':st[1],
        'venues':State_Data[st]     
        }
      data.append(data_element)

    print(data)

     
  # data=[{
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "venues": [{
  #     "id": 1,
  #     "name": "The Musical Hop",
  #     "num_upcoming_shows": 0,
  #   }, {
  #     "id": 3,
  #     "name": "Park Square Live Music & Coffee",
  #     "num_upcoming_shows": 1,
  #   }]
  # }, {
  #   "city": "New York",
  #   "state": "NY",
  #   "venues": [{
  #     "id": 2,
  #     "name": "The Dueling Pianos Bar",
  #     "num_upcoming_shows": 0,
  #   }]
  # }]
  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term = request.form.get('search_term', '')
  search_term = search_term.lower()
  venues = Venue.query.all()
   
  response  = {}
  all_data = []
  count = 0
  for ven in venues:    
    name = ven.name
    if search_term in name:
      venue_artists = ven.artists
      shows_num = Show.query.filter(Show.venue_id==ven.id).count()
      print(venue_artists)      
      data_element = {
        'id':ven.id,
        'name':ven.name,
        "num_upcoming_shows":len(shows_num)
      }
      all_data.append(data_element)
      count +=1
  response={
    "count":count,
    "data":all_data
  }
  print(response)
  # response={
  #   "count": 1,
  #   "data": [{
  #     "id": 2,
  #     "name": "The Dueling Pianos Bar",
  #     "num_upcoming_shows": 0,
  #   }]
  # }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  venue = Venue.query.filter(Venue.id==venue_id).first() 
 
 

  print(venue)
  current_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
  upcoming_shows = Show.query.filter((Show.start_time >current_time)&(Show.venue_id==venue.id)).all()
  prev_shows = Show.query.filter((Show.start_time < current_time)&(Show.venue_id==venue.id)).all()
  
  data_coming =[]
  data_prev = []
  for show in upcoming_shows:
    artist = Artist.query.filter(Artist.id==show.artist_id).first()
    data_coming.append({
      "artist_id":artist.id,
      "artist_name":artist.name,
      "artist_image_link":artist.image_link,
      "start_time":show.start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    })


  for show in prev_shows:
    artist = Artist.query.filter(Artist.id==show.artist_id).first()
    data_prev.append({
      "artist_id":artist.id,
      "artist_name":artist.name,
      "artist_image_link":artist.image_link,
      "start_time":show.start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    })

  "2019-05-21T21:30:00.000Z"
  data = {
    "id":venue.id,
    "name":venue.name,
    "genres":venue.genres,
    'address':venue.address,
    'city':venue.city,
    'state':venue.state,
    'phone':venue.phone,
    'website':venue.website,
    "facebook_link":venue.facebook_link,
    "seeking_talent":venue.seeking_talent,
    "seeking_description":venue.seeking_description,
    "image_link":venue.image_link,
    "past_shows":data_prev,
    "upcoming_shows": data_coming,
     "past_shows_count":len(data_prev),
     "upcoming_shows_count":len(data_coming)
  }
  # data1={
  #   "id": 1,
  #   "name": "The Musical Hop",
  #   "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
  #   "address": "1015 Folsom Street",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "123-123-1234",
  #   "website": "https://www.themusicalhop.com",
  #   "facebook_link": "https://www.facebook.com/TheMusicalHop",
  #   "seeking_talent": True,
  #   "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
  #   "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
  #   "past_shows": [{
  #     "artist_id": 4,
  #     "artist_name": "Guns N Petals",
  #     "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #     "start_time": "2019-05-21T21:30:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data2={
  #   "id": 2,
  #   "name": "The Dueling Pianos Bar",
  #   "genres": ["Classical", "R&B", "Hip-Hop"],
  #   "address": "335 Delancey Street",
  #   "city": "New York",
  #   "state": "NY",
  #   "phone": "914-003-1132",
  #   "website": "https://www.theduelingpianos.com",
  #   "facebook_link": "https://www.facebook.com/theduelingpianos",
  #   "seeking_talent": False,
  #   "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
  #   "past_shows": [],
  #   "upcoming_shows": [],
  #   "past_shows_count": 0,
  #   "upcoming_shows_count": 0,
  # }
  # data3={
  #   "id": 3,
  #   "name": "Park Square Live Music & Coffee",
  #   "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
  #   "address": "34 Whiskey Moore Ave",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "415-000-1234",
  #   "website": "https://www.parksquarelivemusicandcoffee.com",
  #   "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
  #   "seeking_talent": False,
  #   "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #   "past_shows": [{
  #     "artist_id": 5,
  #     "artist_name": "Matt Quevedo",
  #     "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #     "start_time": "2019-06-15T23:00:00.000Z"
  #   }],
  #   "upcoming_shows": [{
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-01T20:00:00.000Z"
  #   }, {
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-08T20:00:00.000Z"
  #   }, {
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-15T20:00:00.000Z"
  #   }],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 1,
  # }
  # data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  print(form)
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  try:
    venue_data = request.form
    venue = Venue()
    venue.name = venue_data.get('name')
    venue.city = venue_data.get('city')
    venue.state = venue_data.get('state')
    venue.address = venue_data.get('address')
    venue.phone = venue_data.get('phone')
    venue.genres = venue_data.getlist('genres')
    sk = venue_data.get('seeking_talent')
    if sk == 'y':
      venue.seeking_talent = True
    else:
      venue.seeking_talent = False 
    venue.seeking_description = venue_data.get('seeking_description')
    venue.website = venue_data.get('website_link ')
    venue.image_link = venue_data.get('image_link')
    venue.facebook_link = venue_data.get('facebook_link') 
    
    db.session.add(venue)
    db.session.commit()
  except:
    print(sys.exc_info())
    db.session.rollback()
  finally:
    db.session.close()    

  # on successful db insert, flash success
  flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  # data=[{
  #   "id": 4,
  #   "name": "Guns N Petals",
  # }, {
  #   "id": 5,
  #   "name": "Matt Quevedo",
  # }, {
  #   "id": 6,
  #   "name": "The Wild Sax Band",
  # }]
  artists = Artist.query.all()  
  data = []
  for artist in artists:
    data_element = {
      "id":artist.id,
      "name":artist.name
    }
    data.append(data_element)

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  # response={
  #   "count": 1,
  #   "data": [{
  #     "id": 4,
  #     "name": "Guns N Petals",
  #     "num_upcoming_shows": 0,
  #   }]
  # }
  search_term = request.form.get('search_term', '').lower()
  artists = Artist.query.all()
  data = []
  for artist in artists:
    if search_term in artist.name.lower():
      data.append({
        "id":artist.id,
        "name":artist.name,
        "num_upcoming_shows":0
      })
  response = {
    "count":len(artists),
    "data":data
  }

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id

  artist = Artist.query.filter(Artist.id==artist_id).first()
  current_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
  prev_shows = Show.query.filter((Show.start_time >current_time)&(Show.artist_id==artist.id)).all()
  prev_shows_json = []
  upcoming_shows= Show.query.filter((Show.start_time >current_time)&(Show.artist_id==artist.id)).all()
  for show in prev_shows:
    venue_id = show.venue_id
    venue = Venue.query.filter(Venue.id==venue_id).first()
    prev_shows_json.append({
      "venue_id":venue_id,
      "venue_id":venue.name,
      "venue_image_link":venue.image_link,
      "start_time":show.start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    })

  upcoming_shows_json = []
  for show in upcoming_shows:
    venue_id = show.venue_id
    venue = Venue.query.filter(Venue.id==venue_id).first()
    upcoming_shows_json.append({
      "venue_id":venue_id,
      "venue_id":venue.name,
      "venue_image_link":venue.image_link,
      "start_time":show.start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    })

  data = {
    "id":artist.id,
    "name":artist.name,
    "genres":artist.genres,
    "city":artist.city,
    "state":artist.city,
    "phone":artist.phone,
    "website":artist.website,
    "facebook_link":artist.facebook_link,
    "seeking_venue":artist.seeking_venue,
    "seeking_description":artist.seeking_description,
    "image_link":artist.image_link,
    "past_shows":prev_shows_json,
    "upcoming_shows":upcoming_shows_json,
    "past_shows_count":len(prev_shows_json),
    "upcoming_shows_count":len(prev_shows_json)

  }

  # data1={
  #   "id": 4,
  #   "name": "Guns N Petals",
  #   "genres": ["Rock n Roll"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "326-123-5000",
  #   "website": "https://www.gunsnpetalsband.com",
  #   "facebook_link": "https://www.facebook.com/GunsNPetals",
  #   "seeking_venue": True,
  #   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
  #   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #   "past_shows": [{
  #     "venue_id": 1,
  #     "venue_name": "The Musical Hop",
  #     "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
  #     "start_time": "2019-05-21T21:30:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data2={
  #   "id": 5,
  #   "name": "Matt Quevedo",
  #   "genres": ["Jazz"],
  #   "city": "New York",
  #   "state": "NY",
  #   "phone": "300-400-5000",
  #   "facebook_link": "https://www.facebook.com/mattquevedo923251523",
  #   "seeking_venue": False,
  #   "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #   "past_shows": [{
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2019-06-15T23:00:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data3={
  #   "id": 6,
  #   "name": "The Wild Sax Band",
  #   "genres": ["Jazz", "Classical"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "432-325-5432",
  #   "seeking_venue": False,
  #   "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "past_shows": [],
  #   "upcoming_shows": [{
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2035-04-01T20:00:00.000Z"
  #   }, {
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2035-04-08T20:00:00.000Z"
  #   }, {
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2035-04-15T20:00:00.000Z"
  #   }],
  #   "past_shows_count": 0,
  #   "upcoming_shows_count": 3,
  # }
  # data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
 # artist={
  #   "id": 4,
  #   "name": "Guns N Petals",
  #   "genres": ["Rock n Roll"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "326-123-5000",
  #   "website": "https://www.gunsnpetalsband.com",
  #   "facebook_link": "https://www.facebook.com/GunsNPetals",
  #   "seeking_venue": True,
  #   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
  #   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  # }
  # TODO: populate form with fields from artist with ID <artist_id>
  artist = Artist.query.filter(Artist.id==artist_id).first()
  artist_obj = {
    "id":artist.id,
    "name":artist.name,
    "genres":artist.genres,
    "city":artist.city,
    "state":artist.city,
    "phone":artist.phone,
    "website":artist.website,
    "facebook_link":artist.facebook_link,
    "seeking_venue":artist.seeking_venue,
    "seeking_description":artist.seeking_description,
    "image_link":artist.image_link,
    "genres":artist.genres
  }
 

  form.name.data = artist_obj["name"]
  form.city.data = artist_obj["city"]
  form.state.data = artist_obj["state"]
  form.phone.data = artist_obj["phone"]
  form.website_link.data = artist_obj["website"]
  form.seeking_venue.data = artist_obj["seeking_venue"]
  form.seeking_description.data = artist_obj["seeking_description"]
  form.image_link.data = artist_obj["image_link"]
  form.facebook_link.data = artist_obj["facebook_link"]
  form.genres.data = artist_obj["genres"]

  return render_template('forms/edit_artist.html', form=form, artist=artist_obj)



@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):

  '''
  try:
    artist_data = request.form
    artist = Artist()
    artist.name = artist_data.get('name')
    artist.city = artist_data.get('city')
    artist.state = artist_data.get('state')
    artist.address = artist_data.get('address')
    artist.phone = artist_data.get('phone')
    artist.genres = artist_data.getlist('genres')
    sk = artist_data.get('seeking_talent')
    if sk == 'y':
      artist.seeking_talent = True
    else:
      artist.seeking_talent = False 
    artist.seeking_description = artist_data.get('seeking_description')
    artist.website = artist_data.get('website_link ')
    artist.image_link = artist_data.get('image_link')
    artist.facebook_link = artist_data.get('facebook_link') 
       
    db.session.add(artist)
    db.session.commit()
  except:
    print(sys.exc_info())
    db.session.rollback()
  finally:
    db.session.close()    
  '''
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  artist = Artist.query.filter(Artist.id == artist_id).first()
  updated_data = request.form
  try:
    artist.name = updated_data.get('name')
    artist.state = updated_data.get('state')
    artist.city = updated_data.get('city')
    artist.genres = updated_data.getlist('genres')
    artist.address = updated_data.get('address')
    artist.website = updated_data.get('website')
    artist.image_link = updated_data.get('image_link')
    artist.facebook_link = updated_data.get('facebook_link')
    sk = updated_data.get('seeking_venue')
    if sk == 'y':
      artist.seeking_talent = True
    else:
      artist.seeking_talent = False 
    artist.seeking_description = updated_data.get('seeking_description')    
    db.session.add(artist)
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }

  venue = Venue.query.filter(Venue.id==venue_id).first()
  venue_obj = {
    "id":venue.id,
    "name":venue.name,
    "genres":venue.genres,
    "city":venue.city,
    "state":venue.city,
    "phone":venue.phone,
    "address":venue.address,
    "website":venue.website,
    "facebook_link":venue.facebook_link,
    "seeking_talent":venue.seeking_talent,
    "seeking_description":venue.seeking_description,
    "image_link":venue.image_link,
    "genres":venue.genres
  }
 

  form.name.data = venue_obj["name"]
  form.city.data = venue_obj["city"]
  form.state.data = venue_obj["state"]
  form.phone.data = venue_obj["phone"]
  form.facebook_link.data = venue_obj["facebook_link"]
  form.address.data = venue_obj["address"]
  form.website_link.data = venue_obj["website"]
  form.seeking_talent.data = venue_obj["seeking_talent"]
  form.seeking_description.data = venue_obj["seeking_description"]
  form.image_link.data = venue_obj["image_link"]
  form.facebook_link.data = venue_obj["facebook_link"]
  form.genres.data = venue_obj["genres"]
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  venue = Venue.query.filter(Venue.id == venue_id).first()
  updated_data = request.form
  try:
    venue.name = updated_data.get('name')
    venue.state = updated_data.get('state')
    venue.city = updated_data.get('city')
    venue.genres = updated_data.getlist('genres')
    venue.address = updated_data.get('address')
    venue.image_link = updated_data.get('image_link')
    venue.website = updated_data.get('website')
    venue.facebook_link = updated_data.get('facebook_link')
    
    sk = updated_data.get('seeking_talent')
    if sk == 'y':
      venue.seeking_talent = True
    else:
      venue.seeking_talent = False 
    venue.seeking_description = updated_data.get('seeking_description')    
    db.session.add(venue)
    db.session.commit()
  except:
    db.session.rollback()
    print(sys.exc_info())
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
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  try:
    artist_data = request.form
    artist = Artist()
    artist.name = artist_data.get('name')
    artist.city = artist_data.get('city')
    artist.state = artist_data.get('state')
    artist.address = artist_data.get('address')
    artist.phone = artist_data.get('phone')
    artist.genres = artist_data.getlist('genres')
    sk = artist_data.get('seeking_talent')
    if sk == 'y':
      artist.seeking_talent = True
    else:
      artist.seeking_talent = False 
    artist.seeking_description = artist_data.get('seeking_description')
    artist.website = artist_data.get('website_link ')
    artist.image_link = artist_data.get('image_link')
    artist.facebook_link = artist_data.get('facebook_link') 
       
    db.session.add(artist)
    db.session.commit()
  except:
    print(sys.exc_info())
    db.session.rollback()
  finally:
    db.session.close()    
  # on successful db insert, flash success
  flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data = []
  shows = Show.query.all()
  for show in shows:
    artist = Artist.query.filter(Artist.id==show.artist_id).first()
    venue = Venue.query.filter(Venue.id==show.venue_id).first()       
    data.append({
      "venue_id":venue.id,
      "venue_name":venue.name,
      "artist_id":artist.id,
      "artist_name":artist.name,
      "artist_image_link":artist.image_link,
      "start_time":show.start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    })

  # data=[{
  #   "venue_id": 1,
  #   "venue_name": "The Musical Hop",
  #   "artist_id": 4,
  #   "artist_name": "Guns N Petals",
  #   "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #   "start_time": "2019-05-21T21:30:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 5,
  #   "artist_name": "Matt Quevedo",
  #   "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #   "start_time": "2019-06-15T23:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 6,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-01T20:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 6,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-08T20:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 6,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-15T20:00:00.000Z"
  # }]
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
  data = request.form
  artist_id = data.get("artist_id")
  venue_id = data.get("venue_id")
  start_time= format_datetime(data.get("start_time"))
  # artist = Artist.query.filter(Artist.id==artist_id).first()
  show = Show(artist_id=artist_id,venue_id=venue_id,start_time=start_time)  
  try:
    db.session.add(show)
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  # on successful db insert, flash success
  flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
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
