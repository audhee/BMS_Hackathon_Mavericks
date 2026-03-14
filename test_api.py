import requests
import json

def get_auth_token():
    login_url = "http://127.0.0.1:8000/api-token-auth/"
    credentials = {"username": "admin", "password": "admin@123"}
    try:
        response = requests.post(login_url, json=credentials)
        if response.status_code == 200:
            return response.json().get("token")
        else:
            print("❌ Login failed. Did you seed the data?")
            return None
    except Exception as e:
        print(f"Error connecting to login endpoint: {e}")
        return None

def run_demo():
    token = get_auth_token()
    if not token:
        return

    url = "http://127.0.0.1:8000/api/verify-traveler/"
    headers = {"Authorization": f"Token {token}"}
    
    scenarios = [
        {"name": "Scenario 1: Safe Traveler (John Doe)", "image": "passport_john_doe.jpg"},
        {"name": "Scenario 2: Blacklisted Person (Jane Doe)", "image": "passport_blacklisted_jane.jpg"},
        {"name": "Scenario 3: Expired Visa (Bob Smith)", "image": "passport_expired_bob.jpg"},
        {"name": "Scenario 4: Suspicious Look (Biometric Mismatch)", "image": "passport_imposter_blacklisted.jpg"},
        {"name": "Scenario 5: Genuine First-Timer (Sarah Miller)", "image": "passport_first_time_sarah.jpg"},
    ]

    for scenario in scenarios:
        print(f"\n{'='*50}")
        print(f"RUNNING: {scenario['name']}")
        print(f"{'='*50}")
        
        payload = {
            "passport_image": scenario['image'],
            "live_face_image": "live_feed.jpg",
            "border_location": "Delhi Airport (IGI)",
            "officer_id": "OFFICER_007"
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            data = response.json()
            print(f"STATUS: {data.get('status')}")
            print(f"RISK SCORE: {data.get('risk_score')}")
            
            # Special check for first-timers
            if "Sarah Miller" in str(data):
                print("🔎 Checking DB for Sarah's new record...")
                hist_url = f"http://127.0.0.1:8000/api/traveler/{data['traveler']['passport_number']}/"
                hist_res = requests.get(hist_url, headers=headers)
                if hist_res.status_code == 200:
                    print(f"✅ CONFIRMED: Sarah is now in the DB! History count: {len(hist_res.json()['history'])}")
                else:
                    print(f"❌ ERROR: Sarah was not saved to DB (Status: {hist_res.status_code})")
                    
        except Exception as e:
            print(f"Error: {e}. Is the server running?")

if __name__ == "__main__":
    print("🚀 Starting Digital Border Management System Demo...")
    run_demo()
