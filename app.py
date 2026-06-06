import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

VAPI_PRIVATE_KEY = os.getenv("8a213255-a81f-48e4-b6e8-d01f4f206674")
ASSISTANT_ID = os.getenv("4647645e-d524-4bd8-a122-79e6bc5f3dcf")
PHONE_NUMBER_ID = os.getenv("b4934082-0db3-44d4-b63f-e01a0ef8d5eb")

FIRST_MESSAGE = "Hello, my name is Arun. This is a demo AI voice call. Thank you for answering."

@app.route("/", methods=["GET"])
def home():
    return "AI Voice Agent is running!"

@app.route("/call", methods=["POST"])
def call():
    data = request.get_json() or {}
    number = data.get("number")

    if not number:
        return jsonify({"error": "Phone number is required"}), 400

    if not VAPI_PRIVATE_KEY or not ASSISTANT_ID or not PHONE_NUMBER_ID:
        return jsonify({
            "error": "Missing environment variables",
            "required": ["VAPI_PRIVATE_KEY", "ASSISTANT_ID", "PHONE_NUMBER_ID"]
        }), 500

    url = "https://api.vapi.ai/call"

    headers = {
        "Authorization": f"Bearer {VAPI_PRIVATE_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "assistantId": ASSISTANT_ID,
        "phoneNumberId": PHONE_NUMBER_ID,
        "customer": {
            "number": number
        },
        "assistantOverrides": {
            "firstMessage": FIRST_MESSAGE,
            "model": {
                "messages": [
                    {
                        "role": "system",
                        "content": f"""
You are a professional AI voice assistant.

When the call starts, clearly say:
"{FIRST_MESSAGE}"

Keep the call short and polite.
Do not ask unnecessary questions.
After speaking the introduction, wait for the user response.
"""
                    }
                ]
            }
        }
    }

    response = requests.post(url, json=payload, headers=headers)

    try:
        return jsonify(response.json()), response.status_code
    except Exception:
        return jsonify({
            "status_code": response.status_code,
            "response_text": response.text
        }), response.status_code


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)