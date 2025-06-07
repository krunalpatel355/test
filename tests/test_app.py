"""
Tests for the main application routes and functionality.
"""

import json


def test_home_page(client):
    """Test the home page loads correctly."""
    response = client.get('/')
    assert response.status_code == 200
    data = response.data.decode('utf-8')
    # Check for event titles
    assert 'Test Event 1' in data
    assert 'Test Event 2' in data
    # Check for event details
    assert 'Test Venue 1' in data
    assert '$100' in data
    assert 'A test conference event' in data


def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert 'timestamp' in data
    assert 'version' in data


def test_404_error(client):
    """Test 404 error handling."""
    response = client.get('/nonexistent-page')
    assert response.status_code == 404
    
    data = json.loads(response.data)
    assert 'error' in data
    assert data['error'] == 'Not found'
