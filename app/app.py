#!/usr/bin/env python3
"""
Main application module for the Flask web application.
"""

from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from datetime import datetime

# Initialize Flask app
app = Flask(__name__, 
           template_folder='templates',
           static_folder='static')

# Load configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/events')
def events():
    return render_template('events.html')

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
