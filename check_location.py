import os
import requests
import re
import json
from bs4 import BeautifulSoup

TARGET_USERNAME = os.environ.get("korekore19")  # 監視対象のXユーザー名（@なし）
DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK")
LAST_FILE = "last_location.json"
USER_AGENT = "Mozilla/5.0 (compatible; LocationWatcher/1.0)"

def get_profile_location(username):
    url = f"https://x.com/{username}"
    headers = {"User-Agent": USER_AGENT}
    r = requests.get(url, headers=headers, timeout=15)
    if r.status_code != 200:
        print("取得失敗:", r.status_code)
        return None

    soup = BeautifulSoup(r.text, "html.parser")
    text = soup.get_text(" ", strip=True)
    m = re.search(r"(?:場所|Location)[:：]?\s*([^\n\r\t]{1,200})", text, re.IGNORECASE)
    if m:
        return m.group(1).strip()

    meta = soup.find("meta", {"property": "og:description"})
    if meta:
        desc = meta.get("content", "")
        m2 = re.search(r"(?:Location|場所)[:：]?\s*([^\n\r\t]{1,200})", desc, re.IGNORECASE)
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
    payload = {"content": message}
    requests.post(DISCORD_WEBHOOK, json=payload, timeout=10)

def main():
    username = TARGET_USERNAME
    if not username:
        print("TARGET_USERNAME が設定されていません")
        return

    current = get_profile_location(username)
    if not current:
        print("位置情報を取得できませんでした")
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
