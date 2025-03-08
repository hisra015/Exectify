import requests
import webbrowser
import json
import threading
from flask import Flask, request

# LinkedIn API credentials
CLIENT_ID = "78216hxwnmc057"
CLIENT_SECRET = "WPL_AP1.eppzx9H5m7kg718h.vFH2mQ=="
REDIRECT_URI = "http://localhost:8000/callback"

AUTHORIZATION_URL = "https://www.linkedin.com/oauth/v2/authorization"
TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"

# Flask app for handling OAuth callback
app = Flask(__name__)
authorization_code = None  # To store the authorization code

@app.route("/callback")
def callback():
    global authorization_code
    authorization_code = request.args.get("code")  # Extract the code from URL
    if authorization_code:
        print(f"\n✅ Extracted Authorization Code: {authorization_code}")
    return "✅ Authorization successful! You can close this window."

# Start Flask server in a separate thread
def start_server():
    app.run(port=8000)

# Step 1: Start Local Server to Capture URL
threading.Thread(target=start_server, daemon=True).start()

# Step 2: Generate LinkedIn Authorization URL & Open Browser
auth_url = (
    f"{AUTHORIZATION_URL}?response_type=code&client_id={CLIENT_ID}"
    f"&redirect_uri={REDIRECT_URI}&state=5211&scope=openid%20profile%20w_member_social"
)

print(f"🔗 Opening LinkedIn authorization URL in browser...\n{auth_url}")
webbrowser.open(auth_url)

# Step 3: Wait for the Authorization Code to Be Captured
while not authorization_code:
    pass  # Keep checking until the code is received

# Step 4: Exchange Authorization Code for Access Token
token_data = {
    "grant_type": "authorization_code",
    "code": authorization_code,
    "redirect_uri": REDIRECT_URI,
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
}

headers = {"Content-Type": "application/x-www-form-urlencoded"}

print("\n🔄 Sending token request to LinkedIn...")
token_response = requests.post(TOKEN_URL, data=token_data, headers=headers)
token_json = token_response.json()

print("🔍 Full Token Response:")
print(json.dumps(token_json, indent=4))  # Debugging output

if "access_token" not in token_json:
    print("❌ Failed to retrieve access token. Please check the error above.")
    exit()

ACCESS_TOKEN = token_json["access_token"]
print(f"✅ Access token retrieved successfully! Token: {ACCESS_TOKEN}")
