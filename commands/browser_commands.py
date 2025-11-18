"""
Browser-related commands (search, open websites)
"""

import os
import shutil
import webbrowser
import winreg
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import Config
from utils.tts import speak

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


class BrowserCommands:
    """Handle browser-related operations"""
    
    def __init__(self, driver_manager):
        self.driver_manager = driver_manager
        self.gemini_model = None
        self._initialize_ai()
    
    def _initialize_ai(self):
        """Initialize Gemini AI for smart URL detection"""
        if GEMINI_AVAILABLE and Config.GEMINI_API_KEY != "your_api_key_here":
            try:
                genai.configure(api_key=Config.GEMINI_API_KEY)
                self.gemini_model = genai.GenerativeModel(Config.GEMINI_MODEL)
                print("✅ AI-powered website opening enabled")
            except Exception as e:
                print(f"⚠️ AI initialization failed: {e}")
    
    def _get_smart_url(self, name):
        """Use AI to figure out the correct URL"""
        if not self.gemini_model:
            return None
                
        prompt = f"""Given the user wants to open: "{name}"

Your job:
- Determine the most likely correct URL.
- Handle ALL major categories:
    • Popular sites (YouTube, IG, FB, etc.)
    • Government sites (NTA, Aadhaar, Passport, SIH, DigiLocker, etc.)
    • Exam sites (JEE Mains, JEE Advanced, NEET, CUET, UPSC, SSC, etc.)
    • College/university websites
    • Tech services
    • Shopping sites
    • Banking sites
    • OTT platforms
    • Apps/services that have an obvious official website
- Remove words like "open", "website", "visit", "go to", etc.
- Respond ONLY using valid JSON (no markdown, no backticks).

Format:
{{
  "url": "https://example.com",
  "confidence": 0.0-1.0
}}

---------------------------------
COMMON WEBSITE EXAMPLES
---------------------------------
Input: "youtube"
Output: {{"url": "https://www.youtube.com", "confidence": 0.99}}

Input: "facebook"
Output: {{"url": "https://www.facebook.com", "confidence": 0.99}}

Input: "instagram"
Output: {{"url": "https://www.instagram.com", "confidence": 0.99}}

Input: "twitter"
Output: {{"url": "https://x.com", "confidence": 0.95}}

Input: "reddit"
Output: {{"url": "https://www.reddit.com", "confidence": 0.99}}

Input: "github"
Output: {{"url": "https://github.com", "confidence": 0.99}}

---------------------------------
SPECIAL CASES (GOVERNMENT & OFFICIAL)
---------------------------------
Input: "open sih website"
Output: {{"url": "https://sih.gov.in", "confidence": 0.97}}

Input: "aadhaar"
Output: {{"url": "https://uidai.gov.in", "confidence": 0.98}}

Input: "passport"
Output: {{"url": "https://www.passportindia.gov.in", "confidence": 0.98}}

Input: "pan card"
Output: {{"url": "https://www.onlineservices.nsdl.com", "confidence": 0.95}}

Input: "digilocker"
Output: {{"url": "https://www.digilocker.gov.in", "confidence": 0.98}}

Input: "pm modi website"
Output: {{"url": "https://www.pmindia.gov.in", "confidence": 0.95}}

Input: "cowin"
Output: {{"url": "https://www.cowin.gov.in", "confidence": 0.98}}

---------------------------------
EXAM + EDUCATION SPECIAL CASES
---------------------------------
Input: "jee mains website"
Output: {{"url": "https://jeemain.nta.ac.in", "confidence": 0.97}}

Input: "jee advanced"
Output: {{"url": "https://jeeadv.ac.in", "confidence": 0.97}}

Input: "neet"
Output: {{"url": "https://exams.nta.ac.in/NEET", "confidence": 0.97}}

Input: "cuet"
Output: {{"url": "https://cuet.samarth.ac.in", "confidence": 0.97}}

Input: "upsc"
Output: {{"url": "https://www.upsc.gov.in", "confidence": 0.98}}

Input: "ssc"
Output: {{"url": "https://ssc.nic.in", "confidence": 0.98}}

Input: "gate exam"
Output: {{"url": "https://gate2025.iisc.ac.in", "confidence": 0.95}}

---------------------------------
COLLEGE / UNIVERSITY SPECIAL CASES
---------------------------------
Input: "jiit 62 website"
Output: {{"url": "https://www.jiit.ac.in", "confidence": 0.95}}

Input: "iit bombay"
Output: {{"url": "https://www.iitb.ac.in", "confidence": 0.97}}

Input: "iit delhi"
Output: {{"url": "https://home.iitd.ac.in", "confidence": 0.97}}

Input: "nit warangal"
Output: {{"url": "https://www.nitw.ac.in", "confidence": 0.95}}

Input: "vit vellore"
Output: {{"url": "https://www.vit.ac.in", "confidence": 0.95}}

Input: "amu"
Output: {{"url": "https://www.amu.ac.in", "confidence": 0.95}}

---------------------------------
SHOPPING SPECIAL CASES
---------------------------------
Input: "amazon"
Output: {{"url": "https://www.amazon.in", "confidence": 0.99}}

Input: "flipkart"
Output: {{"url": "https://www.flipkart.com", "confidence": 0.99}}

Input: "myntra"
Output: {{"url": "https://www.myntra.com", "confidence": 0.99}}

Input: "ajio"
Output: {{"url": "https://www.ajio.com", "confidence": 0.99}}

---------------------------------
BANKING SPECIAL CASES
---------------------------------
Input: "sbi"
Output: {{"url": "https://www.onlinesbi.sbi", "confidence": 0.98}}

Input: "hdfc bank"
Output: {{"url": "https://www.hdfcbank.com", "confidence": 0.98}}

Input: "icici"
Output: {{"url": "https://www.icicibank.com", "confidence": 0.98}}

Input: "axis bank"
Output: {{"url": "https://www.axisbank.com", "confidence": 0.98}}

---------------------------------
OTT SPECIAL CASES
---------------------------------
Input: "netflix"
Output: {{"url": "https://www.netflix.com", "confidence": 0.99}}

Input: "amazon prime"
Output: {{"url": "https://www.primevideo.com", "confidence": 0.99}}

Input: "hotstar"
Output: {{"url": "https://www.hotstar.com", "confidence": 0.99}}

Input: "zee5"
Output: {{"url": "https://www.zee5.com", "confidence": 0.99}}

---------------------------------
TECH SERVICES
---------------------------------
Input: "chatgpt"
Output: {{"url": "https://chat.openai.com", "confidence": 0.99}}

Input: "claude"
Output: {{"url": "https://claude.ai", "confidence": 0.99}}

Input: "gemini"
Output: {{"url": "https://gemini.google.com", "confidence": 0.99}}

Input: "gmail"
Output: {{"url": "https://mail.google.com", "confidence": 0.95}}

Input: "drive"
Output: {{"url": "https://drive.google.com", "confidence": 0.95}}

---------------------------------

Now determine the URL for: "{name}"
"""


        try:
            response = self.gemini_model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Clean response
            if response_text.startswith("```json"):
                response_text = response_text.replace("```json", "").replace("```", "").strip()
            elif response_text.startswith("```"):
                response_text = response_text.replace("```", "").strip()
            
            data = json.loads(response_text)
            
            if data.get("confidence", 0) > 0:
                return data.get("url")
            
        except Exception as e:
            print(f"⚠️ AI URL detection failed: {e}")
        
        return None
    
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
            return
        
        if name in ["chrome", "msedge", "firefox"]:
            os.system(f"start {name}")
            msg = f"✅ Opened {name}\n"
            if input_mode == "voice_continuous":
                speak(f"Opened {name}")
            else:
                print(msg)
            return
        
        if self.has_protocol(name):
            os.system(f"start {name}://")
            msg = f"✅ Opened {name}\n"
            if input_mode == "voice_continuous":
                speak(f"Opened {name}")
            else:
                print(msg)
            return
        
        if "youtube" in name:
            if driver:
                try:
                    driver.get("https://www.youtube.com")
                    self.driver_manager.reset_whatsapp_status()  # Reset WhatsApp status
                    
                    msg = "✅ Opened YouTube\n"
                    if input_mode == "voice_continuous":
                        speak("Opened YouTube")
                    else:
                        print(msg)
                    return
                except Exception as e:
                    msg = f"❌ Error opening YouTube: {e}\n"
                    if input_mode == "voice_continuous":
                        speak("Error opening YouTube")
                    else:
                        print(msg)
                    self.driver_manager.cleanup()
            return
        
        if "whatsapp" in name:
            if driver:
                try:
                    driver.get("https://web.whatsapp.com")
                    self.driver_manager.reset_whatsapp_status()  # Will need to verify login
                    
                    msg = "✅ Opening WhatsApp Web\n"
                    if input_mode == "voice_continuous":
                        speak("Opening WhatsApp")
                    else:
                        print(msg)
                    return
                except Exception as e:
                    msg = f"❌ Error opening WhatsApp: {e}\n"
                    if input_mode == "voice_continuous":
                        speak("Error opening WhatsApp")
                    else:
                        print(msg)
                    self.driver_manager.cleanup()
            return
        
        # Try AI-powered URL detection first
        smart_url = self._get_smart_url(name)
        
        if smart_url:
            print(f"🤖 AI detected URL: {smart_url}")
            # Always use webbrowser.open for AI-detected URLs to avoid driver issues
            webbrowser.open(smart_url)
            msg = f"✅ Opened {smart_url}\n"
            if input_mode == "voice_continuous":
                speak(f"Opened {name}")
            else:
                print(msg)
            return
        
        # Fallback to traditional method
        url = f"https://www.{name}.com" if "." not in name else f"https://{name}"
        webbrowser.open(url)
        msg = f"✅ Opened {url}\n"
        if input_mode == "voice_continuous":
            speak(f"Opened {name}")
        else:
            print(msg)