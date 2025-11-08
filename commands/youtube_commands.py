"""
YouTube-related commands
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import Config
from utils.tts import speak


class YouTubeCommands:
    """Handle YouTube-related operations"""
    
    def __init__(self, driver_manager):
        self.driver_manager = driver_manager
    
    def play_video(self, query):
        """Play a YouTube video with the given query"""
        input_mode = Config.get_input_mode()
        driver = self.driver_manager.get_driver()
        
        if not driver:
            return
        
        try:
            driver.get("https://www.youtube.com")
            self.driver_manager.reset_whatsapp_status()  # Reset WhatsApp status when navigating away
            
            msg = f"✅ Opening YouTube to play: {query}"
            if input_mode == "voice_continuous":
                speak(f"Playing {query} on YouTube")
            else:
                print(msg)
            
            wait = WebDriverWait(driver, 10)
            search_box = wait.until(
                EC.presence_of_element_located((By.NAME, "search_query"))
            )
            search_box.clear()
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)
            
            time.sleep(3)
            try:
                first_video = wait.until(
                    EC.element_to_be_clickable((By.XPATH, '(//a[@id="video-title"])[1]'))
                )
                video_title = first_video.get_attribute("title")
                first_video.click()
                msg = f"▶️ Now playing: {video_title}\n"
                if input_mode == "voice_continuous":
                    speak(f"Now playing {video_title}")
                else:
                    print(msg)
            except Exception:
                msg = "✅ Search results displayed\n"
                if input_mode == "voice_continuous":
                    speak("Search results displayed")
                else:
                    print(msg)
        except Exception as e:
            msg = f"❌ Error playing video: {e}\n"
            if input_mode == "voice_continuous":
                speak("Error playing video")
            else:
                print(msg)
            self.driver_manager.cleanup()