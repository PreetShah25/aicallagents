"""
Flask app with minimal Twilio endpoints (demo only).
- POST /voice  -> returns TwiML to speak a consent notice and record consent.
- POST /dial   -> returns TwiML to dial a number (demo).
- POST /outbound -> triggers an outbound call via Twilio REST (requires env).
"""
import os
from flask import Flask, request, Response, jsonify
try:
    from twilio.twiml.voice_response import VoiceResponse  # type: ignore
except Exception:
    VoiceResponse = None

from ace_pro.tools.consent import ConsentPolicy, consent_prompt
from ace_pro.live.twilio_adapter import TwilioClient

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health():
    return {"ok": True}

@app.route("/voice", methods=["POST"])
def voice():
    if VoiceResponse is None:
        return Response("Twilio library not installed", status=500)
    region = request.values.get("region", "US-CA")
    vr = VoiceResponse()
    prompt = consent_prompt(ConsentPolicy(region=region))
    vr.say(prompt)
    vr.pause(length=1)
    vr.say("Thank you. Proceeding to the expert agenda. This is a demo TwiML response.")
    return Response(str(vr), mimetype="text/xml")

@app.route("/dial", methods=["POST"])
def dial():
    if VoiceResponse is None:
        return Response("Twilio library not installed", status=500)
    to_number = request.values.get("to")
    vr = VoiceResponse()
    if to_number:
        dial = vr.dial(callerId=os.getenv("TWILIO_FROM"))
        dial.number(to_number)
    else:
        vr.say("No destination provided.")
    return Response(str(vr), mimetype="text/xml")

@app.route("/outbound", methods=["POST"])
def outbound():
    to = request.json.get("to")
    url = request.json.get("url")  # public URL to /voice or /dial TwiML
    client = TwilioClient()
    call = client.start_call(to_number=to, url=url)
    return jsonify({"sid": getattr(call, "sid", "unknown")})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
