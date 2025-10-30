import requests
import os

USERNAME = "korekore19"
BEARER_TOKEN = os.environ["X_BEARER_TOKEN"]
DISCORD_WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]

def send_to_discord(message):
    print("📤 Discord通知:", message)
    requests.post(DISCORD_WEBHOOK_URL, json={"content": message})

def get_user_id(username):
    url = f"https://api.twitter.com/2/users/by/username/{username}"
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
    res = requests.get(url, headers=headers)
    print("🛰 ユーザーID取得レスポンス:", res.status_code)
    print("📦 内容:", res.text)
    data = res.json()
    if "data" in data:
        return data["data"]["id"]
    else:
        send_to_discord("❌ ユーザーIDの取得に失敗しました。")
        return None

def get_location(user_id):
    if user_id is None:
        return ""
    url = f"https://api.twitter.com/2/users/{user_id}"
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
    res = requests.get(url, headers=headers)
    print("🛰 プロフィール取得レスポンス:", res.status_code)
    print("📦 内容:", res.text)
    data = res.json()
    if "data" in data:
        return data["data"].get("location", "")
    else:
        send_to_discord("❌ プロフィール情報の取得に失敗しました。")
        return ""

def main():
    user_id = get_user_id(USERNAME)
    current_location = get_location(user_id)
    send_to_discord(f"📢 テスト通知：現在の場所欄は「{current_location}」")

if __name__ == "__main__":
    main()
