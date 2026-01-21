"""
Configuration settings for JJ Voice Assistant
"""

import os
from dotenv import load_dotenv
from utils.utils_frozen import get_env_file_path, is_frozen

class Config:
    """Global configuration settings"""
    
    # Chrome settings - auto-detect Chrome installation
    @staticmethod
    def _find_chrome_path():
        """Find Chrome installation path"""
        possible_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe"),
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        # Return default and let it fail with helpful error message
        return r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    
    CHROME_PATH = _find_chrome_path.__func__()
    USER_DATA_DIR = os.path.join(os.path.expanduser("~"), "ChromeAutomation")
    
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
    
    # Gemini AI settings
    # Load .env from executable directory in frozen mode, current dir otherwise
    env_path = get_env_file_path()
    if os.path.exists(env_path):
        load_dotenv(env_path)
    else:
        load_dotenv()  # Try default location
    
    API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_API_KEY = API_KEY
    GEMINI_MODEL = "gemini-2.5-flash"
    
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