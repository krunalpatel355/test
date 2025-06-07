"""
Test configuration and fixtures.
"""

import pytest
import sys
import os
from datetime import datetime, timedelta
from pymongo import MongoClient

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from app import app


@pytest.fixture(scope='session')
def mongodb():
    """Create a MongoDB test database."""
    client = MongoClient('mongodb://localhost:27017/')
    db = client['TEPIS_TEST']
    
    # Clear existing data
    db.events.delete_many({})
    
    # Insert test data
    current_date = datetime.now()
    test_events = [
        {
            'event_title': 'Test Event 1',
            'event_type': 'Conference',
            'city_name': 'Test City',
            'start_date': current_date + timedelta(days=1),
            'end_date': current_date + timedelta(days=2),
        },
        {
            'event_title': 'Test Event 2',
            'event_type': 'Workshop',
            'city_name': 'Another City',
            'start_date': current_date + timedelta(days=3),
            'end_date': current_date + timedelta(days=4),
        }
    ]
    db.events.insert_many(test_events)
    
    yield db
    
    # Cleanup after tests
    client.drop_database('TEPIS_TEST')
    client.close()


@pytest.fixture
def client(mongodb):
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    app.config['MONGODB_URI'] = 'mongodb://localhost:27017/'
    app.config['MONGODB_DB'] = 'TEPIS_TEST'
    
    # Update the app's MongoDB connection to use test database
    global db
    db = mongodb
    app.db = mongodb
    
    with app.test_client() as client:
        yield client
