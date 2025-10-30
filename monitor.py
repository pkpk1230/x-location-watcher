import requests
import os

USERNAME = "korekore19"
BEARER_TOKEN = os.environ["X_BEARER_TOKEN"]
DISCORD_WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]
STATE_FILE = "last_location.txt"

def get_user_id(username):
    url = f"https://api.twitter.com/2/users/by/username/{username}"
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
    res = requests.get(url, headers=headers).json()
    return res["data"]["id"]

def get_location(user_id):
    url = f"https://api.twitter.com/2/users/{user_id}"
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
    res = requests.get(url, headers=headers).json()
    return res["data"].get("location", "")

def send_to_discord(message):
    requests.post(DISCORD_WEBHOOK_URL, json={"content": message})

def load_last_location():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return f.read().strip()
    return ""

def save_location(location):
    with open(STATE_FILE, "w") as f:
        f.write(location)

def main():
    user_id = get_user_id(USERNAME)
    current_location = get_location(user_id)
    last_location = load_last_location()

    if current_location != last_location:
        send_to_discord(f"📢 @korekore19 の場所欄が更新されました:\n「{current_location}」")
        save_location(current_location)

if __name__ == "__main__":
    main()
