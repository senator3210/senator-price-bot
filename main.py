import os
import requests
from bs4 import BeautifulSoup
from flask import Flask, request

TOKEN = os.getenv("BOT_TOKEN")
app = Flask(__name__)

def get_price_from_digikala(product_url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(product_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    price_tag = soup.find("div", class_="product-page__offer-price")
    if not price_tag:
        price_tag = soup.find("div", class_="c-product__seller-price")
        
    if price_tag:
        return price_tag.text.strip()
    return "قیمت پیدا نشد!"

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, data=payload)

@app.route("/", methods=["POST"])
def webhook():
    data = request.json
    chat_id = data["message"]["chat"]["id"]
    message = data["message"].get("text", "")

    if message.startswith("http"):
        price = get_price_from_digikala(message)
        send_message(chat_id, f"قیمت محصول:\n{price}")

    else:
        send_message(chat_id, "لینک محصول دیجی‌کالا را ارسال کن تا قیمت را بگویم.")
    
    return "OK"
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Render پورت رو با متغیر PORT می‌فرسته
    app.run(host='0.0.0.0', port=port)
