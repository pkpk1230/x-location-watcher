import os
import requests
from bs4 import BeautifulSoup

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
STATE_FILE = "last_location.txt"
TWITTER_URL = "https://mobile.twitter.com/korekore19"

def send_to_discord(message):
    print("📤 Discord通知:", message)
    try:
        requests.post(WEBHOOK_URL, json={"content": message})
    except Exception as e:
        print("❌ Discord通知に失敗:", e)

def get_location_text():
    res = requests.get(TWITTER_URL, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(res.text, "html.parser")

    # ✅ プロフィール欄の場所を含む要素を抽出（構造は要確認）
    profile_blocks = soup.find_all("div", class_="profile-field")
    location = ""
    for block in profile_blocks:
        if "Location" in block.text or "場所" in block.text:
            location = block.text.strip()
            break

    print("📍 抽出された場所欄:", location)
    return location

def load_last_location():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return ""

def save_location(location):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        f.write(location)

def main():
    current_location = get_location_text()
    if not current_location:
        print("❌ 場所欄が取得できませんでした。通知はスキップします。")
        return

    last_location = load_last_location()
    print("📍 前回の場所欄:", last_location)

    if current_location != last_location:
        send_to_discord(f"📢 @korekore19 の場所欄が更新されました:\n「{current_location}」")
        save_location(current_location)
    else:
        print("✅ 場所欄に変化なし。通知は不要です。")

if __name__ == "__main__":
    main()
