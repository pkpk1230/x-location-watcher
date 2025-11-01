import os, time, chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook
from embed_utils import create_embed

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_B")
TARGET_URL = os.environ.get("X_TARGET_URL")
STATE_FILE = "last_state.txt"

def get_location_and_url():
    chromedriver_autoinstaller.install()
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--lang=ja-JP")
    options.add_argument("--user-agent=Mozilla/5.0")

    driver = webdriver.Chrome(options=options)
    driver.get(TARGET_URL)
    time.sleep(5)

    html = driver.page_source
    with open("html_dump.txt", "w", encoding="utf-8") as f:
        f.write(html)

    try:
        location_elem = driver.find_element(By.XPATH, '//*[@data-testid="UserLocation"]')
        soup = BeautifulSoup(location_elem.get_attribute("innerHTML"), "html.parser")
        text = soup.find("span").get_text(strip=True)
        emojis = "".join(img.get("alt", "") for img in soup.find_all("img"))
        location = text + emojis
    except: location = ""

    try:
        url_elem = driver.find_element(By.XPATH, '//*[@data-testid="UserUrl"]')
        url_text = url_elem.text.strip()
    except: url_text = ""

    driver.quit()
    return location, url_text

def load_last_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
            return lines if len(lines) == 2 else [lines[0], ""]
    return ["", ""]

def save_state(location, url):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        f.write(location + "\n" + url)

def send_embed(location_text=None, url_text=None):
    webhook = DiscordWebhook(url=WEBHOOK_URL)
    fields = {
        "📍 場所欄": location_text,
        "🔗 リンク欄": url_text
    }
    embed = create_embed("x", "profile_change", TARGET_URL, fields)
    webhook.add_embed(embed)
    webhook.execute()

def main():
    current_location, current_url = get_location_and_url()
    last_location, last_url = load_last_state()
    loc_diff = current_location if current_location != last_location else None
    url_diff = current_url if current_url != last_url else None
    if loc_diff or url_diff:
        send_embed(loc_diff, url_diff)
        save_state(current_location, current_url)

if __name__ == "__main__":
    main()
