#!/usr/bin/env python3
"""
Simple deployment script for the application.
"""

import os
import subprocess
import argparse


def run_command(command):
    """Run a shell command."""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True)
    return result.returncode == 0


def deploy_docker():
    """Deploy using Docker."""
    print("🐳 Starting Docker deployment...")
    
    run_command("docker-compose down")
    run_command("docker-compose build")
    run_command("docker-compose up -d")
    
    print("✅ Docker deployment completed!")


def deploy_local():
    """Deploy locally."""
    print("🏠 Starting local deployment...")
    
    # Install dependencies
    run_command("pip install -r requirements.txt")
    
    # Run tests
    run_command("python -m pytest tests/")
    
    # Start the application
    print("Starting the application...")
    os.environ['FLASK_ENV'] = 'production'
    run_command("python app/app.py")


def main():
    """Main deployment function."""
    parser = argparse.ArgumentParser(description='Deploy the application')
    parser.add_argument(
        '--method',
        choices=['docker', 'local'],
        default='docker',
        help='Deployment method (default: docker)'
    )
    
    args = parser.parse_args()
    
    print(f"🚀 Deploying using {args.method} method")
    
    if args.method == 'docker':
        deploy_docker()
    elif args.method == 'local':
        deploy_local()
    
    print("🎉 Deployment completed!")


if __name__ == '__main__':
    main()
