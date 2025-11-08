"""
Browser-related commands (search, open websites)
"""

import os
import shutil
import webbrowser
import winreg
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import Config
from utils.tts import speak


class BrowserCommands:
    """Handle browser-related operations"""
    
    def __init__(self, driver_manager):
        self.driver_manager = driver_manager
    
    @staticmethod
    def has_protocol(name):
        """Check if a protocol exists in Windows registry"""
        try:
            key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, f"{name}")
            try:
                winreg.QueryValueEx(key, "URL Protocol")
                winreg.CloseKey(key)
                return True
            except:
                winreg.CloseKey(key)
                return False
        except:
            return False
    
    def search_google(self, query):
        """Search Google for the given query"""
        input_mode = Config.get_input_mode()
        driver = self.driver_manager.get_driver()
        
        if not driver:
            return
        
        try:
            driver.get("https://www.google.com")
            self.driver_manager.reset_whatsapp_status()  # Reset WhatsApp status
            
            wait = WebDriverWait(driver, 10)
            search_box = wait.until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            search_box.clear()
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)
            msg = f"✅ Searching Google for: {query}\n"
            if input_mode == "voice_continuous":
                speak(f"Searching for {query}")
            else:
                print(msg)
        except Exception as e:
            msg = f"❌ Error during search: {e}\n"
            if input_mode == "voice_continuous":
                speak("Error during search")
            else:
                print(msg)
            self.driver_manager.cleanup()
    
    def open_app_or_website(self, name):
        """Open an application or website"""
        input_mode = Config.get_input_mode()
        driver = self.driver_manager.get_driver()
        
        # Check if it's an executable
        app_path = shutil.which(name)
        
        if app_path:
            os.startfile(app_path)
            msg = f"✅ Opened {name}\n"
            if input_mode == "voice_continuous":
                speak(f"Opened {name}")
            else:
                print(msg)
        
        elif name in ["chrome", "msedge", "firefox"]:
            os.system(f"start {name}")
            msg = f"✅ Opened {name}\n"
            if input_mode == "voice_continuous":
                speak(f"Opened {name}")
            else:
                print(msg)
        
        elif self.has_protocol(name):
            os.system(f"start {name}://")
            msg = f"✅ Opened {name}\n"
            if input_mode == "voice_continuous":
                speak(f"Opened {name}")
            else:
                print(msg)
        
        elif "youtube" in name:
            if driver:
                try:
                    driver.get("https://www.youtube.com")
                    self.driver_manager.reset_whatsapp_status()  # Reset WhatsApp status
                    
                    msg = "✅ Opened YouTube\n"
                    if input_mode == "voice_continuous":
                        speak("Opened YouTube")
                    else:
                        print(msg)
                except Exception as e:
                    msg = f"❌ Error opening YouTube: {e}\n"
                    if input_mode == "voice_continuous":
                        speak("Error opening YouTube")
                    else:
                        print(msg)
                    self.driver_manager.cleanup()
        
        elif "whatsapp" in name:
            if driver:
                try:
                    driver.get("https://web.whatsapp.com")
                    self.driver_manager.reset_whatsapp_status()  # Will need to verify login
                    
                    msg = "✅ Opening WhatsApp Web\n"
                    if input_mode == "voice_continuous":
                        speak("Opening WhatsApp")
                    else:
                        print(msg)
                except Exception as e:
                    msg = f"❌ Error opening WhatsApp: {e}\n"
                    if input_mode == "voice_continuous":
                        speak("Error opening WhatsApp")
                    else:
                        print(msg)
                    self.driver_manager.cleanup()
        
        else:
            url = f"https://www.{name}.com" if "." not in name else f"https://{name}"
            webbrowser.open(url)
            msg = f"✅ Opened {url}\n"
            if input_mode == "voice_continuous":
                speak(f"Opened {name}")
            else:
                print(msg)