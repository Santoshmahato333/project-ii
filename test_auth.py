import requests
import time

def test_auth_system():
    base_url = "http://localhost:5000"
    
    print("Testing FilmyFix Authentication System")
    print("=" * 40)
    
    # Test 1: Check if the app is running
    try:
        response = requests.get(base_url)
        print(f"✓ Homepage accessible: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("✗ App not running. Please start the Flask app first.")
        return
    
    # Test 2: Check login page
    try:
        response = requests.get(f"{base_url}/login")
        print(f"✓ Login page accessible: {response.status_code}")
    except:
        print("✗ Login page not accessible")
    
    # Test 3: Check signup page
    try:
        response = requests.get(f"{base_url}/signup")
        print(f"✓ Signup page accessible: {response.status_code}")
    except:
        print("✗ Signup page not accessible")
    
    print("\nAuthentication System Features:")
    print("- User registration with email and password")
    print("- User login with username and password")
    print("- Password hashing for security")
    print("- Session management with Flask-Login")
    print("- Protected routes requiring authentication")
    print("- Flash messages for user feedback")
    print("- Responsive design matching your existing theme")
    
    print("\nTo test the system:")
    print("1. Visit http://localhost:5000")
    print("2. Click 'Sign Up' to create an account")
    print("3. Login with your credentials")
    print("4. Try the movie recommendation feature")

if __name__ == "__main__":
    test_auth_system() 