import requests
import os
from dotenv import load_dotenv

load_dotenv()

# === CONFIG ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Store last state per device
last_states = {}

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print("Error sending message:", e)


def process_data(data):
    global last_states

    device_name = data.get("device_name")
    sensor_state = data.get("sensor_states")

    # Validate input
    if device_name is None or sensor_state not in [0, 1]:
        return

    # First time seeing this device
    if device_name not in last_states:
        last_states[device_name] = sensor_state
        message = f"🔔 {device_name} state initialized to {sensor_state}"
        send_telegram(message)
        return

    # Detect change for this specific device
    if sensor_state != last_states[device_name]:
        message = f"🔔 {device_name} state changed to {sensor_state}"
        send_telegram(message)
        print(message)

        # Update state
        last_states[device_name] = sensor_state