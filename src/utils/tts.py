"""
Text-to-Speech utilities
"""

import pyttsx3
from config import Config


def speak(text):
    """Convert text to speech"""
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', Config.SPEECH_RATE)
        engine.setProperty('volume', Config.SPEECH_VOLUME)
        print(text)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print(f"Speech error: {e}")