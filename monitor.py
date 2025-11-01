import os
import time
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook, DiscordEmbed

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
STATE_FILE = "last_state.txt"
TARGET_URL = "https://x.com/chopkx2"

def send_embed(location_text=None, url_text=None):
    webhook = DiscordWebhook(url=WEBHOOK_URL)

    embed = DiscordEmbed(
        title="📢 Korekoreプロフィール更新",
        description="以下の項目が変更されました",
        url=TARGET_URL,
        color=0xFFFF00
    )

    if location_text:
        embed.add_embed_field(name="📍 場所欄", value=location_text, inline=False)
    if url_text:
        embed.add_embed_field(name="🔗 リンク欄", value=url_text, inline=False)

    embed.set_footer(text="自動監視Botより")
    embed.set_timestamp()

    webhook.add_embed(embed)
    webhook.execute()

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
            if len(lines) == 2:
                return lines
            elif len(lines) == 1:
                return [lines[0], ""]
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

    loc_diff = current_location if current_location != last_location else None
    url_diff = current_url if current_url != last_url else None

    if loc_diff or url_diff:
        send_embed(location_text=loc_diff, url_text=url_diff)
        save_state(current_location, current_url)
    else:
        print("✅ 変化なし。通知は不要です。")

if __name__ == "__main__":
    main()
