import os
import time
import requests
from bs4 import BeautifulSoup

URL = "https://www.costco.com.tw/Digital-Mobile/Mobile-Tablets/iPhone-Mobile-Phones/Apple-iPhone-17-Pro-Max-256GB-Silver/p/158029"

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_telegram_message(message: str):
    if not BOT_TOKEN or not CHAT_ID:
        print("請設定 TELEGRAM_BOT_TOKEN 和 TELEGRAM_CHAT_ID 環境變數")
        return
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("無法發送訊息：", e)

def check_stock():
    try:
        resp = requests.get(URL, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        print("網頁請求失敗：", e)
        return False

    soup = BeautifulSoup(resp.text, "html.parser")
    # Costco 網站「缺貨」會有 sold-out / 缺貨字樣
    if "缺貨" in soup.text or "Sold Out" in soup.text:
        print("目前缺貨")
        return False
    else:
        print("⚡ 發現補貨！")
        send_telegram_message(f"Costco 補貨通知！趕快下單：{URL}")
        return True

if __name__ == "__main__":
    while True:
        check_stock()
        time.sleep(600)  # 每 10 分鐘檢查一次
