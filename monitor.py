import os
import time
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
STATE_FILE = "last_state.txt"
TARGET_URL = "https://twitter.com/korekore19"

def send_to_discord(message):
    print("📤 Discord通知:", message)
    try:
        DiscordWebhook(url=WEBHOOK_URL, content=message).execute()
    except Exception as e:
        print("❌ Discord通知に失敗:", e)

def get_location_and_url():
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
        text = soup.find("span").get_text(strip=True)
        emojis = "".join(img.get("alt", "") for img in soup.find_all("img"))
        location = text + emojis
    except Exception:
        location = ""

    try:
        url_elem = driver.find_element(By.XPATH, '//*[@data-testid="UserUrl"]')
        url_text = url_elem.text.strip()
    except Exception:
        url_text = ""

    driver.quit()
    print("📍 抽出された場所欄:", location)
    print("🔗 抽出されたリンク欄:", url_text)
    return location, url_text

def load_last_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
            return lines if len(lines) == 2 else ["", ""]
    return ["", ""]

def save_state(location, url):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        f.write(location + "\n" + url)

def main():
    current_location, current_url = get_location_and_url()
    if not current_location and not current_url:
        print("❌ プロフィール情報が取得できませんでした。通知はスキップします。")
        return

    last_location, last_url = load_last_state()
    print("📍 前回の場所欄:", last_location)
    print("🔗 前回のリンク欄:", last_url)

    changes = []
    if current_location != last_location:
        changes.append(f"📍 場所欄が更新されました:\n「{current_location}」")
    if current_url != last_url:
        changes.append(f"🔗 リンク欄が更新されました:\n「{current_url}」")

    if changes:
        send_to_discord("\n\n".join(changes))
        save_state(current_location, current_url)
    else:
        print("✅ 変化なし。通知は不要です。")

if __name__ == "__main__":
    main()
