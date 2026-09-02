#!/usr/bin/env python3
import os
import json
import logging
import requests
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables
TOKEN = "8824806107:AAF2bnlcHnD7Vl3kB37wujKc-4tHRUfydT0"
API_KEY = os.environ.get("API_KEY", "Sahil")
API_URL = "https://ethicaltabbo.in/api/lookup"

bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot, None, workers=0)

def get_number_info(number):
    try:
        url = f"{API_URL}?key={API_KEY}&mobile={number}"
        response = requests.get(url, timeout=10)
        data = response.json()
        return data if data.get('status') else None
    except Exception as e:
        logger.error(f"API Error: {e}")
        return None

def clean_data(data):
    if not data:
        return data
    import copy
    cleaned = copy.deepcopy(data)
    for key in ['credit', 'telegram', 'channel', 'api_info']:
        cleaned.pop(key, None)
    if 'data' in cleaned:
        for record in cleaned['data']:
            if isinstance(record, dict):
                for k in ['id', 'alt_number']:
                    record.pop(k, None)
    return cleaned

def start(update, context):
    update.message.reply_text("💀 DATA LEAKER OSINT BOT\n\nSend 10-digit number.")

def handle_message(update, context):
    number = update.message.text.strip()
    if not number.isdigit() or len(number) != 10:
        update.message.reply_text("❌ Send exactly 10 digits!")
        return
    
    processing_msg = update.message.reply_text("⏳ Searching...")
    data = get_number_info(number)
    
    if data:
        result = json.dumps(clean_data(data), indent=2, ensure_ascii=False)[:4000]
        processing_msg.edit_text(f"```json\n{result}\n```", parse_mode='Markdown')
    else:
        processing_msg.edit_text("❌ No data found!")

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

@app.route('/')
def index():
    return "Bot is running!", 200

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), bot)
        dispatcher.process_update(update)
        return "OK", 200
    return "Method not allowed", 405

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)