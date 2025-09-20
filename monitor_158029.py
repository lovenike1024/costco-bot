import os
import requests
from bs4 import BeautifulSoup

# 目標商品網址
URL = "https://www.costco.com.tw/Digital-Mobile/Mobile-Tablets/iPhone-Mobile-Phones/Apple-iPhone-17-Pro-Max-256GB-Silver/p/158029"

# Telegram 設定
BOT_TOKEN = 8412570840:AAF-3MoAZqtGiv6jhgwcrpGL4DRuss-rUnY("TELEGRAM_BOT_TOKEN")
CHAT_ID = 6262945484("TELEGRAM_CHAT_ID")

def send_telegram_message(message: str):
    if not BOT_TOKEN or not CHAT_ID:
        print("請設定 TELEGRAM_BOT_TOKEN 和 TELEGRAM_CHAT_ID 環境變數")
        return
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200 and response.json().get("ok"):
            print("✅ Telegram 訊息發送成功")
        else:
            print("❌ 發送失敗", response.text)
    except Exception as e:
        print("❌ 無法發送訊息：", e)

def check_stock():
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(URL, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 判斷是否有缺貨提示（這裡要依實際網頁標籤調整）
        out_of_stock = soup.find("span", string="缺貨")
        if out_of_stock:
            print("目前缺貨")
        else:
            print("⚡ 發現補貨！")
            send_telegram_message(f"⚡ Costco 補貨通知！趕快下單：{URL}")
    except Exception as e:
        print("❌ 檢查失敗：", e)

if __name__ == "__main__":
    check_stock()
