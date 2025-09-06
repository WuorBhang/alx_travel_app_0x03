#!/usr/bin/env python3
"""
Final verification script for ALX Travel App Milestone 5 implementation.
This script verifies that all required components are properly implemented.
"""

import os
import sys
from pathlib import Path

def check_file_exists(file_path, description):
    """Check if a file exists and return status."""
    exists = os.path.exists(file_path)
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {file_path}")
    return exists

def check_file_content(file_path, required_strings, description):
    """Check if file contains required strings."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        missing = []
        for required in required_strings:
            if required not in content:
                missing.append(required)
        
        if not missing:
            print(f"✅ {description}: All required content found")
            return True
        else:
            print(f"⚠️  {description}: Missing: {', '.join(missing)}")
            return False
    except Exception as e:
        print(f"❌ {description}: Error reading file - {e}")
        return False

def check_directory_structure():
    """Check the project directory structure."""
    print("📁 Checking Project Directory Structure...")
    print("=" * 60)
    
    checks = []
    
    # Check main project files
    checks.append(check_file_exists("manage.py", "Django manage.py"))
    checks.append(check_file_exists("requirements.txt", "Requirements file"))
    checks.append(check_file_exists("README.md", "README documentation"))
    checks.append(check_file_exists("PROJECT_SUMMARY.md", "Project summary"))
    checks.append(check_file_exists(".env", "Environment variables file"))
    
    # Check Django app structure
    checks.append(check_file_exists("alx_travel_app/__init__.py", "Django app __init__.py"))
    checks.append(check_file_exists("alx_travel_app/celery.py", "Celery configuration"))
    checks.append(check_file_exists("alx_travel_app/settings.py", "Django settings"))
    checks.append(check_file_exists("alx_travel_app/urls.py", "Django URLs"))
    
    # Check listings app
    checks.append(check_file_exists("listings/__init__.py", "Listings app __init__.py"))
    checks.append(check_file_exists("listings/models.py", "Listings models"))
    checks.append(check_file_exists("listings/views.py", "Listings views"))
    checks.append(check_file_exists("listings/tasks.py", "Celery tasks"))
    checks.append(check_file_exists("listings/serializers.py", "Listings serializers"))
    
    # Check management commands
    checks.append(check_file_exists("listings/management/commands/test_celery.py", "Test Celery command"))
    
    # Check test scripts
    checks.append(check_file_exists("test_celery_setup.py", "Full Celery test script"))
    checks.append(check_file_exists("simple_celery_test.py", "Simple Celery test script"))
    checks.append(check_file_exists("start_dev.sh", "Development startup script"))
    
    print("=" * 60)
    return all(checks)

def check_celery_configuration():
    """Check Celery configuration files."""
    print("\n🔧 Checking Celery Configuration...")
    print("=" * 60)
    
    checks = []
    
    # Check celery.py content
    celery_checks = [
        "from celery import Celery",
        "app = Celery('alx_travel_app')",
        "app.config_from_object",
        "app.autodiscover_tasks"
    ]
    checks.append(check_file_content("alx_travel_app/celery.py", celery_checks, "Celery configuration"))
    
    # Check __init__.py content
    init_checks = [
        "from .celery import app as celery_app",
        "__all__ = ('celery_app',)"
    ]
    checks.append(check_file_content("alx_travel_app/__init__.py", init_checks, "Celery app import"))
    
    # Check settings.py content
    settings_checks = [
        "CELERY_BROKER_URL",
        "EMAIL_BACKEND",
        "EMAIL_HOST",
        "EMAIL_PORT"
    ]
    checks.append(check_file_content("alx_travel_app/settings.py", settings_checks, "Django settings"))
    
    print("=" * 60)
    return all(checks)

def check_task_implementation():
    """Check Celery task implementation."""
    print("\n🐇 Checking Celery Task Implementation...")
    print("=" * 60)
    
    checks = []
    
    # Check tasks.py content
    task_checks = [
        "from celery import shared_task",
        "@shared_task",
        "send_booking_confirmation_email",
        "send_payment_confirmation_email",
        "django.core.mail import send_mail"
    ]
    checks.append(check_file_content("listings/tasks.py", task_checks, "Celery tasks"))
    
    # Check views.py content
    view_checks = [
        "from .tasks import",
        "send_booking_confirmation_email.delay",
        "send_payment_confirmation_email.delay"
    ]
    checks.append(check_file_content("listings/views.py", view_checks, "Task triggers in views"))
    
    print("=" * 60)
    return all(checks)

def check_dependencies():
    """Check required dependencies in requirements.txt."""
    print("\n📦 Checking Dependencies...")
    print("=" * 60)
    
    required_packages = [
        "celery",
        "kombu",
        "billiard",
        "amqp",
        "Django",
        "djangorestframework"
    ]
    
    try:
        with open("requirements.txt", 'r') as f:
            content = f.read()
        
        missing = []
        for package in required_packages:
            if package.lower() not in content.lower():
                missing.append(package)
        
        if not missing:
            print("✅ All required packages found in requirements.txt")
            return True
        else:
            print(f"⚠️  Missing packages: {', '.join(missing)}")
            return False
    except Exception as e:
        print(f"❌ Error reading requirements.txt: {e}")
        return False

def check_documentation():
    """Check documentation completeness."""
    print("\n📚 Checking Documentation...")
    print("=" * 60)
    
    checks = []
    
    # Check README content
    readme_checks = [
        "Celery",
        "RabbitMQ",
        "Background Jobs",
        "Email Notifications",
        "Installation",
        "Testing"
    ]
    checks.append(check_file_content("README.md", readme_checks, "README documentation"))
    
    # Check project summary
    summary_checks = [
        "Milestone 5",
        "Background Jobs",
        "Email Notifications",
        "Celery",
        "RabbitMQ"
    ]
    checks.append(check_file_content("PROJECT_SUMMARY.md", summary_checks, "Project summary"))
    
    print("=" * 60)
    return all(checks)

def main():
    """Run all verification checks."""
    print("🚀 ALX Travel App - Milestone 5 Implementation Verification")
    print("=" * 80)
    
    # Run all checks
    checks = [
        ("Directory Structure", check_directory_structure),
        ("Celery Configuration", check_celery_configuration),
        ("Task Implementation", check_task_implementation),
        ("Dependencies", check_dependencies),
        ("Documentation", check_documentation)
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n🔍 Running {name} Check...")
        result = check_func()
        results.append((name, result))
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 80)
    
    passed = 0
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {name}")
        if result:
            passed += 1
    
    print("=" * 80)
    print(f"Overall Result: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 CONGRATULATIONS! All checks passed!")
        print("Your Milestone 5 implementation is complete and ready for submission.")
        print("\nNext steps:")
        print("1. Install and start RabbitMQ")
        print("2. Test the implementation with: python simple_celery_test.py")
        print("3. Submit your project for review")
        return True
    else:
        print(f"\n⚠️  {total - passed} check(s) failed. Please review and fix the issues.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
