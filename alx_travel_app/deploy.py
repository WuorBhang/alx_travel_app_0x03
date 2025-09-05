#!/usr/bin/env python3
"""
Deployment helper script for ALX Travel App
This script helps prepare the application for deployment
"""

import os
import sys
import subprocess
import secrets

def generate_secret_key():
    """Generate a secure Django secret key"""
    return secrets.token_urlsafe(50)

def check_requirements():
    """Check if all required files exist"""
    required_files = [
        'requirements.txt',
        'Procfile',
        'render.yaml',
        'build.sh',
        'manage.py',
        'alx_travel_app/settings.py',
        'alx_travel_app/wsgi.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ All required deployment files are present")
    return True

def create_production_env():
    """Create a production environment template"""
    secret_key = generate_secret_key()
    
    prod_env_content = f"""# Production Environment Variables
# Copy these to your deployment platform (Render, Heroku, etc.)

SECRET_KEY={secret_key}
DEBUG=False
ALLOWED_HOSTS=your-domain.com,*.render.com,*.herokuapp.com

# Database (will be provided by hosting platform)
# DATABASE_URL=postgresql://user:password@host:port/database

# Celery Configuration (Redis recommended for production)
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Email Configuration (Update with your credentials)
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Payment Gateway (Update with your credentials)
CHAPA_SECRET_KEY=your_chapa_secret_key_here
"""
    
    with open('.env.production', 'w') as f:
        f.write(prod_env_content)
    
    print("✅ Created .env.production template")
    print("📝 Update the values in .env.production with your actual credentials")

def run_pre_deployment_checks():
    """Run checks before deployment"""
    print("🔍 Running pre-deployment checks...")
    
    # Check if we can import Django
    try:
        import django
        print(f"✅ Django {django.get_version()} is available")
    except ImportError:
        print("❌ Django is not installed")
        return False
    
    # Check if we can import required packages
    required_packages = ['rest_framework', 'drf_yasg', 'celery']
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} is available")
        except ImportError:
            print(f"❌ {package} is not installed")
            return False
    
    return True

def collect_static_files():
    """Collect static files for deployment"""
    print("📦 Collecting static files...")
    try:
        result = subprocess.run([
            sys.executable, 'manage.py', 'collectstatic', '--noinput'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Static files collected successfully")
            return True
        else:
            print(f"❌ Error collecting static files: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error running collectstatic: {e}")
        return False

def main():
    """Main deployment preparation function"""
    print("🚀 ALX Travel App - Deployment Preparation")
    print("=" * 50)
    
    # Change to the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Create production environment template
    create_production_env()
    
    # Run pre-deployment checks
    if not run_pre_deployment_checks():
        print("\n❌ Pre-deployment checks failed. Please install missing packages.")
        sys.exit(1)
    
    # Collect static files
    if not collect_static_files():
        print("\n❌ Failed to collect static files.")
        sys.exit(1)
    
    print("\n🎉 Deployment preparation completed successfully!")
    print("\n📋 Next steps:")
    print("1. Update .env.production with your actual credentials")
    print("2. Commit your changes to Git")
    print("3. Deploy to your chosen platform (Render, Heroku, etc.)")
    print("4. Set environment variables on your hosting platform")
    print("5. Test your deployed application")
    print("\n📖 See DEPLOYMENT_GUIDE.md for detailed instructions")

if __name__ == "__main__":
    main()