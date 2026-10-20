"""Text-to-speech through the Windows speech engine (SAPI).

pyttsx3 2.99 only finishes the first thing it says on Windows: later words are cut
off a fraction of a second in. Talking to SAPI directly (which is what pyttsx3 does
underneath) speaks every time, and in the background, so the game doesn't freeze
while a word is being spoken.
"""
import comtypes.client

SVSF_ASYNC = 1               # return straight away instead of waiting for the word to finish
SVSF_PURGE_BEFORE_SPEAK = 2  # a new word cuts off one that's still being spoken


class Speech:
    def __init__(self, volume=0.9):
        """volume runs from 0.0 (silent) to 1.0 (full)."""
        try:
            self.voice = comtypes.client.CreateObject("SAPI.SpVoice")
            voices = self.voice.GetVoices()
            # The second installed voice (Zira on most English Windows), or the only one there is
            self.voice.Voice = voices.Item(1 if voices.Count > 1 else 0)
            self.set_volume(volume)
        except Exception as e:
            print(f"Error initializing text-to-speech: {e}")
            self.voice = None

    def set_volume(self, volume):
        if self.voice:
            self.voice.Volume = round(min(1.0, max(0.0, volume)) * 100)

    def say(self, text):
        if self.voice and text:
            try:
                self.voice.Speak(text, SVSF_ASYNC | SVSF_PURGE_BEFORE_SPEAK)
            except Exception as e:
                print(f"Error with text-to-speech: {e}")
