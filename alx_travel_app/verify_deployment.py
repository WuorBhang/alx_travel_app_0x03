#!/usr/bin/env python3
"""
Deployment verification script for ALX Travel App
This script verifies that the deployed application is working correctly
"""

import requests
import json
import sys
from urllib.parse import urljoin

def test_endpoint(base_url, endpoint, method='GET', data=None, expected_status=200):
    """Test a specific endpoint"""
    url = urljoin(base_url, endpoint)
    try:
        if method == 'GET':
            response = requests.get(url, timeout=10)
        elif method == 'POST':
            response = requests.post(url, json=data, timeout=10)
        
        if response.status_code == expected_status:
            print(f"✅ {method} {endpoint} - Status: {response.status_code}")
            return True
        else:
            print(f"❌ {method} {endpoint} - Expected: {expected_status}, Got: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ {method} {endpoint} - Error: {e}")
        return False

def verify_swagger_documentation(base_url):
    """Verify Swagger documentation is accessible"""
    print("\n🔍 Testing Swagger Documentation...")
    
    # Test Swagger UI page
    swagger_accessible = test_endpoint(base_url, '/swagger/', expected_status=200)
    
    # Test OpenAPI schema
    schema_accessible = test_endpoint(base_url, '/swagger.json', expected_status=200)
    
    return swagger_accessible and schema_accessible

def verify_api_endpoints(base_url):
    """Verify API endpoints are working"""
    print("\n🔍 Testing API Endpoints...")
    
    results = []
    
    # Test listings endpoint
    results.append(test_endpoint(base_url, '/api/listings/', 'GET'))
    
    # Test bookings endpoint
    results.append(test_endpoint(base_url, '/api/bookings/', 'GET'))
    
    # Test home page
    results.append(test_endpoint(base_url, '/', 'GET'))
    
    return all(results)

def verify_celery_integration(base_url):
    """Verify Celery integration by testing booking creation"""
    print("\n🔍 Testing Celery Integration...")
    
    # Test data for booking creation
    booking_data = {
        "listing": 1,  # Assuming listing with ID 1 exists
        "user_name": "Test User",
        "user_email": "test@example.com",
        "check_in": "2024-12-01",
        "check_out": "2024-12-05"
    }
    
    # This will trigger the Celery email task
    result = test_endpoint(base_url, '/api/bookings/', 'POST', booking_data, expected_status=201)
    
    if result:
        print("✅ Booking creation successful (Celery task should be triggered)")
    else:
        print("❌ Booking creation failed")
    
    return result

def main():
    """Main verification function"""
    if len(sys.argv) != 2:
        print("Usage: python verify_deployment.py <base_url>")
        print("Example: python verify_deployment.py https://your-app.onrender.com")
        sys.exit(1)
    
    base_url = sys.argv[1]
    if not base_url.startswith(('http://', 'https://')):
        base_url = 'https://' + base_url
    
    print(f"🚀 Verifying ALX Travel App Deployment")
    print(f"🌐 Base URL: {base_url}")
    print("=" * 60)
    
    # Run verification tests
    swagger_ok = verify_swagger_documentation(base_url)
    api_ok = verify_api_endpoints(base_url)
    
    print("\n📊 Verification Summary:")
    print("=" * 30)
    print(f"Swagger Documentation: {'✅ PASS' if swagger_ok else '❌ FAIL'}")
    print(f"API Endpoints: {'✅ PASS' if api_ok else '❌ FAIL'}")
    
    if swagger_ok and api_ok:
        print("\n🎉 Deployment verification SUCCESSFUL!")
        print(f"📖 Swagger documentation available at: {base_url}/swagger/")
        print(f"🔗 API endpoints available at: {base_url}/api/")
        
        print("\n📋 Manual Testing Checklist:")
        print("1. Visit the Swagger documentation and test API calls")
        print("2. Create a booking to test Celery email notifications")
        print("3. Test payment processing if configured")
        print("4. Check admin panel functionality")
        
        return True
    else:
        print("\n❌ Deployment verification FAILED!")
        print("Please check the deployment logs and configuration.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)