import os
import requests

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_telegram_message(message: str):
    if not BOT_TOKEN or not CHAT_ID:
        print("請設定 TELEGRAM_BOT_TOKEN 和 TELEGRAM_CHAT_ID 環境變數")
        return
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            print("✅ Telegram 訊息發送成功")
        else:
            print("❌ 發送失敗", response.text)
    except Exception as e:
        print("❌ 無法發送訊息：", e)

if __name__ == "__main__":
    send_telegram_message("測試 Telegram 通知功能 ✅")
