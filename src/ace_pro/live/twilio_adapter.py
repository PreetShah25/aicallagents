"""
Optional Twilio adapter (stub). To enable:
- pip install twilio
- export TWILIO_ACCOUNT_SID=... TWILIO_AUTH_TOKEN=... TWILIO_FROM=...
"""
class TwilioClient:
    def __init__(self):
        try:
            import os
            from twilio.rest import Client  # type: ignore
            sid = os.getenv("TWILIO_ACCOUNT_SID"); tok = os.getenv("TWILIO_AUTH_TOKEN")
            if not (sid and tok): raise RuntimeError("Set TWILIO_ACCOUNT_SID/TWILIO_AUTH_TOKEN")
            self._from = os.getenv("TWILIO_FROM")
            self._client = Client(sid, tok)
        except Exception as e:
            raise RuntimeError("Install twilio and set env vars") from e

    def start_call(self, to_number: str, url: str):
        # url is a TwiML webhook you host (out of scope for this repo)
        return self._client.calls.create(to=to_number, from_=self._from, url=url)
