"""
WhatsApp-related commands
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import Config
from utils.tts import speak


class WhatsAppCommands:
    """Handle WhatsApp-related operations"""
    
    def __init__(self, driver_manager):
        self.driver_manager = driver_manager
    
    def send_message(self, contact, message):
        """Send WhatsApp message via WhatsApp Web - Always clicks first search result"""
        input_mode = Config.get_input_mode()
        driver = self.driver_manager.get_driver()
        
        if not driver:
            return
        
        try:
            # Open WhatsApp Web if not already there
            if not self.driver_manager.is_whatsapp_logged_in():
                driver.get("https://web.whatsapp.com")
                msg = "📱 Opening WhatsApp Web..."
                if input_mode == "voice_continuous":
                    speak("Opening WhatsApp Web")
                else:
                    print(msg)
                
                wait = WebDriverWait(driver, Config.WHATSAPP_LOGIN_TIMEOUT)
                try:
                    wait.until(
                        EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
                    )
                    self.driver_manager.set_whatsapp_logged_in(True)
                    msg = "✅ WhatsApp Web logged in successfully!"
                    if input_mode == "voice_continuous":
                        speak("WhatsApp logged in")
                    else:
                        print(msg)
                except Exception:
                    msg = "⏳ Please scan the QR code on WhatsApp Web to continue..."
                    if input_mode == "voice_continuous":
                        speak("Please scan QR code")
                    else:
                        print(msg)
                    
                    wait = WebDriverWait(driver, Config.WHATSAPP_QR_SCAN_TIMEOUT)
                    wait.until(
                        EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
                    )
                    self.driver_manager.set_whatsapp_logged_in(True)
                    msg = "✅ QR code scanned! WhatsApp ready!"
                    if input_mode == "voice_continuous":
                        speak("WhatsApp ready")
                    else:
                        print(msg)
            
            # Now send the message
            wait = WebDriverWait(driver, Config.SELENIUM_WAIT_TIMEOUT)
            
            # Find and click search box
            search_box = wait.until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
            )
            search_box.click()
            time.sleep(0.5)
            
            # Clear any existing search
            search_box.send_keys(Keys.CONTROL + "a")
            search_box.send_keys(Keys.BACKSPACE)
            time.sleep(0.3)
            
            # Type contact name
            search_box.send_keys(contact)
            msg = f"🔍 Searching for contact: {contact}"
            if input_mode == "voice_continuous":
                speak(f"Searching for {contact}")
            else:
                print(msg)
            time.sleep(2.5)  # Wait for search results to load
            
            # ALWAYS click the first result - Try multiple strategies
            contact_clicked = False
            
            # Strategy 1: Click first visible chat span with title
            try:
                first_result = wait.until(
                    EC.element_to_be_clickable((By.XPATH, '(//span[@title])[1]'))
                )
                first_result.click()
                contact_clicked = True
                msg = f"✅ Selected first result for '{contact}'"
                if input_mode == "voice_continuous":
                    speak("Contact selected")
                else:
                    print(msg)
            except Exception:
                pass
            
            # Strategy 2: Click using the specific structure
            if not contact_clicked:
                try:
                    first_result = wait.until(
                        EC.element_to_be_clickable((By.XPATH, '//div[@id="pane-side"]//div[@role="listitem"][1]'))
                    )
                    first_result.click()
                    contact_clicked = True
                    msg = f"✅ Selected first result for '{contact}'"
                    if input_mode == "voice_continuous":
                        speak("Contact selected")
                    else:
                        print(msg)
                except Exception:
                    pass
            
            # Strategy 3: Press DOWN arrow and ENTER (most reliable!)
            if not contact_clicked:
                try:
                    search_box.send_keys(Keys.DOWN)
                    time.sleep(0.3)
                    search_box.send_keys(Keys.RETURN)
                    contact_clicked = True
                    msg = f"✅ Selected first result for '{contact}'"
                    if input_mode == "voice_continuous":
                        speak("Contact selected")
                    else:
                        print(msg)
                except Exception:
                    pass
            
            # If nothing worked
            if not contact_clicked:
                msg = f"❌ No search results found for '{contact}'\n"
                if input_mode == "voice_continuous":
                    speak(f"No results for {contact}")
                else:
                    print(msg)
                # Clear the search
                search_box.send_keys(Keys.ESCAPE)
                return
            
            time.sleep(1)
            
            # Find message input box and send message
            try:
                message_box = wait.until(
                    EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
                )
            except Exception:
                # Alternative: Try finding by role
                message_box = wait.until(
                    EC.presence_of_element_located((By.XPATH, '//div[@role="textbox"][@contenteditable="true"]'))
                )
            
            message_box.click()
            time.sleep(0.3)
            
            # Type and send message
            message_box.send_keys(message)
            time.sleep(0.5)
            message_box.send_keys(Keys.RETURN)
            
            msg = f"✅ Message sent: '{message}'\n"
            if input_mode == "voice_continuous":
                speak("Message sent")
            else:
                print(msg)
                
        except Exception as e:
            msg = f"❌ Error sending WhatsApp message: {e}\n"
            if input_mode == "voice_continuous":
                speak("Error sending WhatsApp message")
            else:
                print(msg)
            self.driver_manager.set_whatsapp_logged_in(False)