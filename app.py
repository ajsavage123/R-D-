'"""
Apple-Supported WhatsAuto — Milestone 1 (Working Prototype)
Single-file Python server using pywa (MIT) + WhatsApp Cloud API.

Setup:
1. pip install flask pywa
2. Copy .env.example to .env and fill in your credentials
3. Create clients.csv with sample data
4. Run: python app.py
5. Configure webhook in Meta Developer Dashboard: https://your-server.com/webhook
"""

import csv
import os
import random
import time
from datetime import datetime
from flask import Flask, request

try:
    from pywa import WhatsApp
except ImportError:
    WhatsApp = None

app = Flask(__name__)

WHATSAPP_ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
WHATSAPP_VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN")
AUTO_REPLY = os.getenv("AUTO_REPLY", "Thank you for messaging us! We have received your message and will get back to you soon.")

CLIENTS_CSV = "clients.csv"
MESSAGES_CSV = "messages.csv"

wa = None
if WhatsApp and WHATSAPP_ACCESS_TOKEN and WHATSAPP_PHONE_NUMBER_ID:
    wa = WhatsApp(phone_id=WHATSAPP_PHONE_NUMBER_ID, token=WHATSAPP_ACCESS_TOKEN)


def load_clients():
    if not os.path.exists(CLIENTS_CSV):
        return []
    with open(CLIENTS_CSV, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def find_client_by_ip(ip_address):
    for client in load_clients():
        if client.get("ip_address", "").strip() == ip_address.strip():
            return client
    return None


def log_message(message_id, client_phone, inbound_text, outbound_text, is_killed):
    file_exists = os.path.exists(MESSAGES_CSV)
    with open(MESSAGES_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["message_id", "client_phone", "inbound_text", "outbound_text", "timestamp", "is_killed"])
        writer.writerow([message_id, client_phone, inbound_text, outbound_text, datetime.utcnow().isoformat(), str(is_killed)])


def add_random_delay():
    time.sleep(random.uniform(2, 10))


@app.route("/webhook", methods=["GET"])
def webhook_verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == WHATSAPP_VERIFY_TOKEN:
        return challenge, 200
    return "Forbidden", 403


@app.route("/webhook", methods=["POST"])
def webhook_receive():
    client_ip = request.remote_addr
    client = find_client_by_ip(client_ip)
    is_killed = False

    if not client or client.get("is_active", "").strip().lower() != "true":
        is_killed = True
        data = request.get_json(silent=True) or {}
        for entry in data.get("entry", []):
            for change in entry.get("changes", []):
                for msg in change.get("value", {}).get("messages", []):
                    from_number = msg.get("from", "")
                    msg_id = msg.get("id", "unknown")
                    if wa:
                        try:
                            wa.send_message(to=from_number, text="Service suspended. Please contact support.")
                        except Exception:
                            pass
                    log_message(msg_id, client.get("phone_number", ""), "", "Service suspended. Please contact support.", True)
        return "Service suspended", 200

    data = request.get_json(silent=True) or {}
    for entry in data.get("entry", []):
        for change in entry.get("changes", []):
            for msg in change.get("value", {}).get("messages", []):
                from_number = msg.get("from", "")
                msg_id = msg.get("id", "unknown")
                text = msg.get("text", {}).get("body", "")

                add_random_delay()

                if wa:
                    try:
                        wa.send_message(to=from_number, text=AUTO_REPLY)
                    except Exception as e:
                        app.logger.error("Failed to send reply: %s", e)

                log_message(msg_id, from_number, text, AUTO_REPLY, is_killed)

    return "OK", 200


@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}, 200


if __name__ == "__main__":
    if not WHATSAPP_ACCESS_TOKEN or not WHATSAPP_PHONE_NUMBER_ID or not WHATSAPP_VERIFY_TOKEN:
        print("WARNING: Missing WhatsApp credentials. Set WHATSAPP_ACCESS_TOKEN, WHATSAPP_PHONE_NUMBER_ID, WHATSAPP_VERIFY_TOKEN")
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
'
