import os
import time
from bs4 import BeautifulSoup
import cloudscraper
import telebot

# Зчитуємо дані з налаштувань сервера
TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
OLX_URL = os.environ.get("OLX_URL")

bot = telebot.TeleBot(TOKEN)
scraper = cloudscraper.create_scraper()
seen_ads = set()


def check_olx():
    response = scraper.get(OLX_URL)
    if response.status_code != 200:
        return

    soup = BeautifulSoup(response.text, "html.parser")

    # Шукаємо всі посилання на оголошення
    for a in soup.find_all("a", href=True):
        link = a["href"]
        if "/d/uk/obyavlenie/" in link or "/d/uk/obyavlenye/" in link:
            full_url = "https://www.olx.ua" + link if link.startswith("/") else link
            clean_url = full_url.split("#")[0]

            if clean_url not in seen_ads:
                seen_ads.add(clean_url)
                # Відправляємо перші знайдені посилання або нові
                bot.send_message(
                    CHAT_ID, f"🔥 Знайдено оголошення:\n{clean_url}"
                )


# Нескінченний цикл: перевірка кожні 3 хвилини
while True:
    try:
        check_olx()
    except Exception as e:
        print(f"Помилка: {e}")
    time.sleep(180)
