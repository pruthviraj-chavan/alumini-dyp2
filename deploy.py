#!/usr/bin/env python
"""
Deployment script for DYP Salokhenagar Alumni Portal
This script helps prepare the application for deployment to a production environment.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

# Get the base directory of the project
BASE_DIR = Path(__file__).resolve().parent

def check_requirements():
    """Check if all required packages are installed"""
    print("Checking requirements...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True)
        print("✅ All requirements installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install requirements")
        sys.exit(1)

def collect_static():
    """Collect static files"""
    print("Collecting static files...")
    try:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alumni_portal.settings")
        subprocess.run([sys.executable, "manage.py", "collectstatic", "--noinput"], 
                      check=True)
        print("✅ Static files collected successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to collect static files")
        sys.exit(1)

def run_migrations():
    """Run database migrations"""
    print("Running database migrations...")
    try:
        subprocess.run([sys.executable, "manage.py", "migrate"], 
                      check=True)
        print("✅ Database migrations applied successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to apply database migrations")
        sys.exit(1)

def create_production_settings():
    """Create a production settings file"""
    print("Creating production settings file...")
    prod_settings_path = BASE_DIR / "alumni_portal" / "settings_prod.py"
    
    if not prod_settings_path.exists():
        with open(prod_settings_path, 'w') as f:
            f.write("""\"\"\"
Production settings for alumni_portal project.
\"\"\"

from .settings import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Database
# Use PostgreSQL in production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Static files (CSS, JavaScript, Images)
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# Media files
MEDIA_ROOT = BASE_DIR / 'mediafiles'

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')
""")
        print("✅ Production settings file created successfully")
    else:
        print("⚠️ Production settings file already exists")

def check_for_sensitive_data():
    """Check for sensitive data in the codebase"""
    print("Checking for sensitive data...")
    sensitive_patterns = [
        "SECRET_KEY =", 
        "PASSWORD =", 
        "TOKEN =",
        "API_KEY ="
    ]
    
    # Files to exclude from check
    exclude_files = [
        "settings_prod.py",
        "deploy.py"
    ]
    
    found_sensitive = False
    
    for root, dirs, files in os.walk(BASE_DIR):
        # Skip virtual environment directories and migrations
        if "venv" in root or "migrations" in root or "__pycache__" in root:
            continue
            
        for file in files:
            if file.endswith(".py") and file not in exclude_files:
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    try:
                        content = f.read()
                        for pattern in sensitive_patterns:
                            if pattern in content:
                                print(f"⚠️ Potential sensitive data found in {filepath}: {pattern}")
                                found_sensitive = True
                    except:
                        print(f"⚠️ Could not read {filepath}")
    
    if not found_sensitive:
        print("✅ No obvious sensitive data found in the codebase")
    else:
        print("⚠️ Please review the files mentioned above and remove any sensitive data")

def main():
    """Main function to run the deployment script"""
    print("=" * 50)
    print("DYP Salokhenagar Alumni Portal - Deployment Script")
    print("=" * 50)
    
    check_requirements()
    run_migrations()
    collect_static()
    create_production_settings()
    check_for_sensitive_data()
    
    print("\n" + "=" * 50)
    print("Deployment preparation completed!")
    print("=" * 50)
    print("\nNext steps:")
    print("1. Review the production settings file")
    print("2. Set up environment variables for sensitive data")
    print("3. Configure your web server (Nginx, Apache, etc.)")
    print("4. Set up a process manager (Gunicorn, uWSGI, etc.)")
    print("5. Configure SSL certificates")
    print("6. Set up database backups")
    print("7. Configure monitoring")
    print("\nThank you for using the DYP Salokhenagar Alumni Portal!")

if __name__ == "__main__":
    main()
