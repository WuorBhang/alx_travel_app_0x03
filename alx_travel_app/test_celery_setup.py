#!/usr/bin/env python
"""
Simple test script to verify Celery setup.
Run this script to check if Celery is properly configured.
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_travel_app.settings')

# Setup Django
django.setup()

def test_celery_import():
    """Test if Celery can be imported and configured."""
    try:
        from alx_travel_app.celery import app
        print("✅ Celery app imported successfully")
        print(f"   App name: {app.main}")
        print(f"   Broker URL: {app.conf.broker_url}")
        return True
    except ImportError as e:
        print(f"❌ Failed to import Celery app: {e}")
        return False

def test_task_import():
    """Test if tasks can be imported."""
    try:
        from listings.tasks import send_booking_confirmation_email, send_payment_confirmation_email
        print("✅ Celery tasks imported successfully")
        print(f"   send_booking_confirmation_email: {send_booking_confirmation_email}")
        print(f"   send_payment_confirmation_email: {send_payment_confirmation_email}")
        return True
    except ImportError as e:
        print(f"❌ Failed to import tasks: {e}")
        return False

def test_django_settings():
    """Test if Django settings are properly configured."""
    try:
        from django.conf import settings
        print("✅ Django settings loaded successfully")
        print(f"   Celery broker URL: {getattr(settings, 'CELERY_BROKER_URL', 'Not set')}")
        print(f"   Email backend: {getattr(settings, 'EMAIL_BACKEND', 'Not set')}")
        return True
    except Exception as e:
        print(f"❌ Failed to load Django settings: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing Celery Setup...")
    print("=" * 50)
    
    tests = [
        test_django_settings,
        test_celery_import,
        test_task_import,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Celery is properly configured.")
        print("\nNext steps:")
        print("1. Start RabbitMQ service")
        print("2. Start Celery worker: celery -A alx_travel_app worker --loglevel=info")
        print("3. Test with: python manage.py test_celery <booking_id>")
    else:
        print("⚠️  Some tests failed. Please check the configuration.")
        sys.exit(1)

if __name__ == "__main__":
    main()
