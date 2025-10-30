import os
import time
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
STATE_FILE = "last_location.txt"
TARGET_URL = "https://twitter.com/korekore19"

def send_to_discord(message):
    print("📤 Discord通知:", message)
    try:
        DiscordWebhook(url=WEBHOOK_URL, content=message).execute()
    except Exception as e:
        print("❌ Discord通知に失敗:", e)

def get_location_text():
    chromedriver_autoinstaller.install()

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--lang=ja-JP")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=options)
    driver.get(TARGET_URL)
    time.sleep(5)

    html = driver.page_source
    with open("html_dump.txt", "w", encoding="utf-8") as f:
        f.write(html)

    try:
        location_elem = driver.find_element(By.XPATH, '//*[@data-testid="UserLocation"]')
        location_html = location_elem.get_attribute("innerHTML")
        soup = BeautifulSoup(location_html, "html.parser")
        location = soup.get_text(separator="", strip=True)
    except Exception:
        location = ""

    driver.quit()
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
