import requests
import os

USERNAME = "korekore19"
BEARER_TOKEN = os.environ["X_BEARER_TOKEN"]
DISCORD_WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]
STATE_FILE = "last_location.txt"
USER_ID_CACHE = "user_id.txt"

def send_to_discord(message):
    print("📤 Discord通知:", message)
    try:
        requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
    except Exception as e:
        print("❌ Discord通知に失敗:", e)

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
        return None

def get_user_id_cached():
    if os.path.exists(USER_ID_CACHE):
        with open(USER_ID_CACHE, "r") as f:
            return f.read().strip()
    user_id = get_user_id(USERNAME)
    if user_id:
        with open(USER_ID_CACHE, "w") as f:
            f.write(user_id)
    return user_id

def get_location(user_id):
    if user_id is None:
        return ""
    url = f"https://api.twitter.com/2/users/{user_id}"
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
    res = requests.get(url, headers=headers)
    print("🛰 プロフィール取得レスポンス:", res.status_code)
    print("📦 内容:", res.text)
    if res.status_code == 429:
        print("⚠️ レート制限中（429）")
        return ""
    data = res.json()
    if "data" in data:
        return data["data"].get("location", "")
    else:
        return ""

def load_last_location():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return f.read().strip()
    return ""

def save_location(location):
    with open(STATE_FILE, "w") as f:
        f.write(location)

def main():
    user_id = get_user_id_cached()
    current_location = get_location(user_id)

    if not current_location:
        print("❌ 場所欄が取得できませんでした。通知はスキップします。")
        return

    last_location = load_last_location()
    print("📍 現在の場所欄:", current_location)
    print("📍 前回の場所欄:", last_location)

    if current_location != last_location:
        send_to_discord(f"📢 @korekore19 の場所欄が更新されました:\n「{current_location}」")
        save_location(current_location)
    else:
        print("✅ 場所欄に変化なし。通知は不要です。")

if __name__ == "__main__":
    main()
