import requests
import time
from datetime import datetime

# Server configuration
SERVER_HOST = "localhost"  # Change to IP address if testing across devices
SERVER_PORT = 5000
SERVER_URL = f"http://{SERVER_HOST}:{SERVER_PORT}"

notification_count=0

def send_notif(message):
    try:
        response = requests.post(
            f"{SERVER_URL}/notify",
            json={"message":message},
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Notification sent successfully!")
            print(f"   Server response: {data}")
            return True
        else:
            print(f"❌ Error: Server returned status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"❌ Error: Could not connect to server at {SERVER_URL}")
        print(f"   Make sure the server is running!")
        return False
    except requests.exceptions.Timeout:
        print(f"❌ Error: Request timed out")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
send_notif("hi")