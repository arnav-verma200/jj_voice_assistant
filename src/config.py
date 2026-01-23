"""
Configuration settings for JJ Voice Assistant
"""

import os
from dotenv import load_dotenv

class Config:
    """Global configuration settings"""
    
    @staticmethod
    def _get_frozen_utils():
        """Lazy import of frozen utils to avoid circular dependency"""
        from utils.utils_frozen import get_env_file_path, is_frozen
        return get_env_file_path, is_frozen
    
    # Browser settings - auto-detect browser installation
    @staticmethod
    def _find_browser():
        """
        Find available browser installation.
        Returns tuple: (browser_path, browser_type)
        browser_type can be: 'chrome', 'edge', 'brave', 'chromium'
        """
        # Define browser search paths with priority order
        browsers = [

            # Brave Browser paths
            (r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe", "brave"),
            (os.path.expanduser(r"~\AppData\Local\BraveSoftware\Brave-Browser\Application\brave.exe"), "brave"),
            
            # Chrome paths
            (r"C:\Program Files\Google\Chrome\Application\chrome.exe", "chrome"),
            (r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe", "chrome"),
            (os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe"), "chrome"),
            
            # Microsoft Edge paths (good fallback, comes pre-installed on Windows 10/11)
            (r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe", "edge"),
            (r"C:\Program Files\Microsoft\Edge\Application\msedge.exe", "edge"),

            # Chromium paths
            (os.path.expanduser(r"~\AppData\Local\Chromium\Application\chrome.exe"), "chromium"),
        ]
        
        # Search for first available browser
        for path, browser_type in browsers:
            if os.path.exists(path):
                return path, browser_type
        
        # No browser found - return None
        return None, None
    
    # Initialize browser detection
    _browser_result = _find_browser.__func__()
    BROWSER_PATH = _browser_result[0]
    BROWSER_TYPE = _browser_result[1]
    
    # Backwards compatibility - keep CHROME_PATH variable
    CHROME_PATH = BROWSER_PATH
    
    # User data directory (works for all Chromium-based browsers)
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
    @classmethod
    def load_config(cls):
        """Initialize configuration (handling .env and API keys)"""
        get_env_file_path, _ = cls._get_frozen_utils()
        env_path = get_env_file_path()
        if os.path.exists(env_path):
            load_dotenv(env_path)
        else:
            load_dotenv()  # Try default location
        
        cls.API_KEY = os.getenv("GEMINI_API_KEY")
        cls.GEMINI_API_KEY = cls.API_KEY
        
        # Display browser detection result
        if cls.BROWSER_PATH:
            print(f"✓ Detected browser: {cls.BROWSER_TYPE.upper()} at {cls.BROWSER_PATH}")
        else:
            print("\n" + "="*60)
            print("❌ ERROR: No supported browser found!")
            print("="*60)
            print("Please install one of the following browsers:")
            print("  • Google Chrome (recommended)")
            print("  • Microsoft Edge")
            print("  • Brave Browser")
            print("  • Chromium")
            print("="*60 + "\n")

    # Call it once to initialize
    GEMINI_MODEL = "gemini-2.5-flash"
    API_KEY = None
    GEMINI_API_KEY = None
    
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