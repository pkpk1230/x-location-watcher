import os
import requests
import re
import json
from bs4 import BeautifulSoup

# ここに直接監視対象を設定
TARGET_USERNAME = "korekore19"  
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1433428950918496378/1AMU_3Cnp_1rkWZv5q2QI4BSDdPl6M_pGoPOKEwauf1X56OBtjkjO0QyDsw6aq2uUiix"

LAST_FILE = "last_location.json"
USER_AGENT = "Mozilla/5.0 (compatible; LocationWatcher/1.0)"

def get_profile_location(username):
    url = f"https://x.com/{username}"
    headers = {"User-Agent": USER_AGENT}
    try:
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code != 200:
            print(f"取得失敗: HTTP {r.status_code}")
            return None
    except Exception as e:
        print("Request error:", e)
        return None

    soup = BeautifulSoup(r.text, "html.parser")
    text = soup.get_text(" ", strip=True)
    m = re.search(r"(?:場所|Location)[:：]?\s*([^\n\r\t]{1,200})", text, re.IGNORECASE)
    if m:
        return m.group(1).strip()

    meta = soup.find("meta", {"property": "og:description"})
    if meta:
        desc = meta.get("content", "")
        m2 = re.search(r"(?:場所|Location)[:：]?\s*([^\n\r\t]{1,200})", desc, re.IGNORECASE)
        if m2:
            return m2.group(1).strip()
    return None

def load_last():
    if os.path.exists(LAST_FILE):
        with open(LAST_FILE, "r", encoding="utf-8") as f:
            return json.load(f).get("location")
    return None

def save_last(loc):
    with open(LAST_FILE, "w", encoding="utf-8") as f:
        json.dump({"location": loc}, f, ensure_ascii=False, indent=2)

def notify_discord(location):
    message = f"位置情報が更新されました！→ [{location}]"
    try:
        r = requests.post(DISCORD_WEBHOOK, json={"content": message}, timeout=10)
        print("Discord通知ステータス:", r.status_code)
    except Exception as e:
        print("Discord通知失敗:", e)

def main():
    current = get_profile_location(TARGET_USERNAME)
    if not current:
        print("位置情報を取得できませんでした。")
        return

    last = load_last()
    if last != current:
        print("変更あり。通知を送信します")
        notify_discord(current)
        save_last(current)
    else:
        print("変更なし。")

if __name__ == "__main__":
    main()
