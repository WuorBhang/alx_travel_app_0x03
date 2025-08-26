#!/usr/bin/env python3
"""
Simple Celery test script that doesn't require full Django setup.
This script tests if Celery and related packages can be imported.
"""

def test_celery_imports():
    """Test if Celery and related packages can be imported."""
    print("🧪 Testing Celery Package Imports...")
    print("=" * 50)
    
    tests = []
    
    # Test Celery import
    try:
        import celery
        print(f"✅ Celery imported successfully: {celery.__version__}")
        tests.append(True)
    except ImportError as e:
        print(f"❌ Failed to import Celery: {e}")
        tests.append(False)
    
    # Test Kombu import
    try:
        import kombu
        print(f"✅ Kombu imported successfully: {kombu.__version__}")
        tests.append(True)
    except ImportError as e:
        print(f"❌ Failed to import Kombu: {e}")
        tests.append(False)
    
    # Test AMQP import
    try:
        import amqp
        print(f"✅ AMQP imported successfully: {amqp.__version__}")
        tests.append(True)
    except ImportError as e:
        print(f"❌ Failed to import AMQP: {e}")
        tests.append(False)
    
    # Test Billiard import
    try:
        import billiard
        print(f"✅ Billiard imported successfully: {billiard.__version__}")
        tests.append(True)
    except ImportError as e:
        print(f"❌ Failed to import Billiard: {e}")
        tests.append(False)
    
    # Test Django import
    try:
        import django
        print(f"✅ Django imported successfully: {django.get_version()}")
        tests.append(True)
    except ImportError as e:
        print(f"❌ Failed to import Django: {e}")
        tests.append(False)
    
    print("=" * 50)
    passed = sum(tests)
    total = len(tests)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All package imports successful!")
        print("\nNext steps:")
        print("1. Install and start RabbitMQ")
        print("2. Configure Django settings")
        print("3. Test full Celery setup with: python test_celery_setup.py")
    else:
        print("⚠️  Some imports failed. Please check your virtual environment.")
    
    return passed == total

def test_celery_basic_config():
    """Test basic Celery configuration."""
    print("\n🔧 Testing Basic Celery Configuration...")
    print("=" * 50)
    
    try:
        from celery import Celery
        
        # Create a simple Celery app
        app = Celery('test_app')
        app.config_from_object({
            'broker_url': 'amqp://guest:guest@localhost:5672//',
            'result_backend': 'rpc://',
            'task_serializer': 'json',
            'accept_content': ['json'],
            'result_serializer': 'json',
            'timezone': 'UTC',
        })
        
        print("✅ Basic Celery app created successfully")
        print(f"   Broker URL: {app.conf.broker_url}")
        print(f"   Result Backend: {app.conf.result_backend}")
        print(f"   Task Serializer: {app.conf.task_serializer}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to create basic Celery app: {e}")
        return False

if __name__ == "__main__":
    print("🚀 ALX Travel App - Celery Package Test")
    print("=" * 60)
    
    # Test imports
    imports_ok = test_celery_imports()
    
    if imports_ok:
        # Test basic configuration
        config_ok = test_celery_basic_config()
        
        if config_ok:
            print("\n🎯 Ready to proceed with full Django + Celery setup!")
        else:
            print("\n⚠️  Basic Celery configuration failed.")
    else:
        print("\n❌ Cannot proceed without proper package imports.")
