"""
Configuration settings for JJ Voice Assistant
"""

import os


class Config:
    """Global configuration settings"""
    
    # Chrome settings
    CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    USER_DATA_DIR = os.path.join(os.path.expanduser("~"), "ChromeAutomation")
    
    # Gemini API settings
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyD9lxqOHZDlBiISPqmlG0Hdd-5QQk0DNCs")
    GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    
    # Voice settings
    SPEECH_RATE = 175
    SPEECH_VOLUME = 0.9
    
    # Timeout settings
    MICROPHONE_CALIBRATION_DURATION = 2
    VOICE_LISTEN_TIMEOUT = 10
    VOICE_PHRASE_TIME_LIMIT = 20
    WHATSAPP_LOGIN_TIMEOUT = 60
    WHATSAPP_QR_SCAN_TIMEOUT = 120
    SELENIUM_WAIT_TIMEOUT = 15
    
    # Global state
    _input_mode = None
    
    @classmethod
    def set_input_mode(cls, mode):
        """Set the input mode for the application"""
        cls._input_mode = mode
    
    @classmethod
    def get_input_mode(cls):
        """Get the current input mode"""
        return cls._input_mode