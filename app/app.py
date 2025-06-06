#!/usr/bin/env python3
"""
Main application module for the Flask web application.
"""

from flask import Flask, render_template, request, redirect, url_for, send_from_directory,jsonify
import os
from datetime import datetime
from pymongo import MongoClient

# Initialize Flask app
app = Flask(__name__, 
           template_folder='templates',
           static_folder='static')

# Load configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'

# MongoDB connection
mongo_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
client = MongoClient(mongo_uri)
db = client['TEPIS']
events_collection = db['events']

def get_featured_events():
    """Get featured events from MongoDB"""
    return list(events_collection.find().limit(6))

def get_upcoming_events():
    """Get upcoming events from MongoDB"""
    current_date = datetime.now()
    return list(events_collection.find({
        'start_date': {'$gte': current_date}
    }).sort('start_date', 1).limit(9))

@app.route('/')
def index():
    featured_events = get_featured_events()
    upcoming_events = get_upcoming_events()
    
    return render_template('index.html', 
                         featured_events=featured_events,
                         upcoming_events=upcoming_events)

@app.route('/events')
def events():
    current_date = datetime.now()
    page = request.args.get('page', 1, type=int)
    per_page = 7  # Number of events per page

    # Get total count for pagination
    total_events = events_collection.count_documents({'start_date': {'$gte': current_date}})
    
    # Get events for current page
    events_list = list(events_collection.find({
        'start_date': {'$gte': current_date}
    }).sort('start_date', 1).skip((page - 1) * per_page).limit(per_page))
    
    # Calculate total pages
    total_pages = (total_events + per_page - 1) // per_page
    
    # Get unique locations for filter
    locations = events_collection.distinct('city_name')
    
    return render_template('events.html', 
                         events=events_list,
                         current_page=page,
                         total_pages=total_pages,
                         locations=locations)

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        # Here you would typically handle login/authentication
        username = request.form.get('username')
        password = request.form.get('password')
        # Add your authentication logic here
        return redirect(url_for('index'))
    return render_template('auth.html')

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Not found'}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    
    app.run(host=host, port=port, debug=app.config['DEBUG'])
