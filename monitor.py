import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# 🔐 Discord Webhookを直接設定（GitHub Secrets推奨）
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
STATE_FILE = "last_location.txt"
TWITTER_URL = "https://twitter.com/korekore19"

def send_to_discord(message):
    print("📤 Discord通知:", message)
    try:
        requests.post(WEBHOOK_URL, json={"content": message})
    except Exception as e:
        print("❌ Discord通知に失敗:", e)

def get_location_text():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(TWITTER_URL)
        time.sleep(5)  # ページ読み込み待ち（必要に応じて調整）

        # ✅ 場所欄を含む要素を抽出（XPathはTwitterの構造に依存）
        elems = driver.find_elements(By.XPATH, '//span[contains(text(),"生年月日")]/ancestor::div[1]/following-sibling::div//span')
        location = ""
        for elem in elems:
            txt = elem.text.strip()
            if txt and "から利用しています" not in txt and "生年月日" not in txt:
                location = txt
                break

        print("📍 抽出された場所欄:", location)
        return location
    finally:
        driver.quit()

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
