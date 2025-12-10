#!/usr/bin/env python3
"""
Script to create a superuser and generate an API token for the Zeppelin project.
Run this script after setting up the Django project to get the API token for frontend integration.
"""

import os
import sys
import django

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zeppelin.settings')
django.setup()

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

def create_superuser_and_token():
    """Create a superuser and generate an API token."""
    
    # Check if superuser already exists
    if User.objects.filter(is_superuser=True).exists():
        print("Superuser already exists.")
        superuser = User.objects.filter(is_superuser=True).first()
    else:
        # Create superuser
        username = input("Enter superuser username (default: admin): ").strip() or "admin"
        email = input("Enter superuser email: ").strip()
        password = input("Enter superuser password: ").strip()
        
        if not email or not password:
            print("Email and password are required!")
            return
        
        superuser = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print(f"Superuser '{username}' created successfully!")
    
    # Get or create token
    token, created = Token.objects.get_or_create(user=superuser)
    
    if created:
        print(f"New API token created: {token.key}")
    else:
        print(f"Existing API token: {token.key}")
    
    print("\n" + "="*60)
    print("SETUP INSTRUCTIONS:")
    print("="*60)
    print("1. Copy the API token above")
    print("2. In the frontend directory (zeppelin-frontend), create a .env file")
    print("3. Add the following line to your .env file:")
    print(f"   VITE_ZEPPELIN_API_TOKEN={token.key}")
    print("4. Also add these other required environment variables:")
    print("   VITE_API_BASE_URL=http://localhost:8000")
    print("   VITE_CLIENT_ID=your_client_id")
    print("   VITE_CLIENT_SECRET=your_client_secret")
    print("5. Start both backend and frontend servers")
    print("6. You can now submit questionnaires from the frontend!")
    print("="*60)

if __name__ == "__main__":
    create_superuser_and_token()