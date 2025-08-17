"""
Streaming ASR placeholder. Use OpenAI Whisper, Deepgram, or Vosk as needed.
"""
class ASRWhisper:
    def transcribe_stream(self, audio_iter):
        for chunk in audio_iter:
            yield "[ASR text for chunk]"  # replace with real ASR output
