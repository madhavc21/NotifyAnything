"""
WIP: LAN server to receive notifications from other devices on the same network
"""

from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

notification_count=0

@app.route('/')
def home():
    return """
<h1>NotifyAnything Server is running</h1>
notif_count = {}
""".format(notification_count)

@app.route('/notify', methods=['POST'])
def notify():
    global notification_count
    notification_count+=1

    data = request.get_json() if request.is_json else {}
    message = data.get('message', 'no message provided')
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"\n{'='*50}")
    print(f"🔔 NOTIFICATION RECEIVED at {timestamp}")
    print(f"Message: {message}")
    print(f"Total count: {notification_count}")
    print(f"{'='*50}\n")
    return {"status": "success", "count":notification_count}

app.run(host='0.0.0.0', port=5000, debug=True)