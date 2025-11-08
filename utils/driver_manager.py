"""
Selenium WebDriver management
"""

import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from config import Config
from utils.tts import speak


class DriverManager:
    """Manage Selenium WebDriver lifecycle"""
    
    def __init__(self):
        self.driver = None
        self.whatsapp_logged_in = False
    
    def get_driver(self):
        """Get or create WebDriver instance"""
        if not self.driver:
            self.driver = self._create_driver()
        return self.driver
    
    def _create_driver(self):
        """Create a new Chrome WebDriver instance"""
        options = Options()
        options.binary_location = Config.CHROME_PATH
        
        if not os.path.exists(Config.USER_DATA_DIR):
            os.makedirs(Config.USER_DATA_DIR)
        
        options.add_argument(f"--user-data-dir={Config.USER_DATA_DIR}")
        options.add_argument("--profile-directory=Default")
        options.add_argument("--remote-allow-origins=*")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--start-maximized")
        options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
        options.add_experimental_option("useAutomationExtension", False)
        
        try:
            new_driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()), 
                options=options
            )
            print("Chrome opened successfully!")
            return new_driver
        except Exception as e:
            print(f"Error creating driver: {e}. Trying alternative method...")
            
            try:
                options2 = Options()
                options2.binary_location = Config.CHROME_PATH
                options2.add_argument("--remote-allow-origins=*")
                options2.add_argument("--no-sandbox")
                options2.add_argument("--disable-dev-shm-usage")
                options2.add_argument("--start-maximized")
                options2.add_experimental_option('excludeSwitches', ['enable-logging'])
                
                new_driver = webdriver.Chrome(
                    service=Service(ChromeDriverManager().install()), 
                    options=options2
                )
                print("Chrome opened (temporary session)")
                return new_driver
            except Exception as e2:
                print(f"Failed to open Chrome: {e2}")
                if Config.get_input_mode() == "voice_continuous":
                    speak("Failed to open Chrome")
                return None
    
    def reset_whatsapp_status(self):
        """Reset WhatsApp login status"""
        self.whatsapp_logged_in = False
    
    def is_whatsapp_logged_in(self):
        """Check if WhatsApp is logged in"""
        return self.whatsapp_logged_in
    
    def set_whatsapp_logged_in(self, status):
        """Set WhatsApp login status"""
        self.whatsapp_logged_in = status
    
    def cleanup(self):
        """Close WebDriver and cleanup"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None
            self.whatsapp_logged_in = False