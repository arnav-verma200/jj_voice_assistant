"""
Browser-related commands (search, open websites)
"""

import os
import json
import shutil
import webbrowser
import winreg
import requests
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
    
    @staticmethod
    def get_url_from_gemini(website_name):
        """Use Gemini API to get the correct URL for a website"""
        input_mode = Config.get_input_mode()
        
        if Config.GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
            print("⚠️ Gemini API key not configured. Using fallback URL creation.")
            if input_mode == "voice_continuous":
                speak("API key not configured, using fallback")
            return None
        
        try:
            prompt = f"""Given the website name or description: "{website_name}"

Please provide ONLY the complete, correct URL for this website.

Rules:
1. Return ONLY the URL, nothing else
2. Include https://
3. If it's a well-known site, use the exact official URL
4. If it's ambiguous, use the most popular/official version
5. For partial names, expand to full URL (e.g., "github" -> "https://github.com")
6. For government/organization sites, use appropriate domain (e.g., ".gov.in", ".org", ".edu")
7. For regional variants, use the correct country domain (e.g., "amazon india" -> ".in")
8. For acronyms or abbreviations, identify the full official website
9. Do not include explanations or alternatives

Examples:
- "github" -> https://github.com
- "twitter" -> https://twitter.com
- "amazon india" -> https://www.amazon.in
- "reddit" -> https://www.reddit.com
- "sih" -> https://www.sih.gov.in
- "sih website" -> https://www.sih.gov.in
- "amazon" -> https://www.amazon.com
- "flipkart" -> https://www.flipkart.com
- "netflix" -> https://www.netflix.com
- "instagram" -> https://www.instagram.com
- "linkedin" -> https://www.linkedin.com
- "stack overflow" -> https://stackoverflow.com
- "medium" -> https://medium.com

Now provide the URL for: "{website_name}" """

            headers = {
                "Content-Type": "application/json"
            }
            
            payload = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }],
                "generationConfig": {
                    "temperature": 0.1,
                    "maxOutputTokens": 100,
                }
            }
            
            api_url = f"{Config.GEMINI_API_URL}?key={Config.GEMINI_API_KEY}"
            
            if input_mode != "voice_continuous":
                print("🤖 Asking Gemini for the correct URL...")
            
            response = requests.post(api_url, headers=headers, json=payload, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if "candidates" in result and len(result["candidates"]) > 0:
                    url = result["candidates"][0]["content"]["parts"][0]["text"].strip()
                    
                    # Clean up the response - remove any markdown or extra text
                    url = url.replace("```", "").strip()
                    
                    # Extract just the URL if there's extra text
                    if " " in url:
                        # Try to find the URL in the text
                        words = url.split()
                        for word in words:
                            if word.startswith("http"):
                                url = word
                                break
                    
                    # Ensure it starts with http
                    if not url.startswith("http"):
                        if url.startswith("www."):
                            url = "https://" + url
                        else:
                            url = "https://www." + url
                    
                    if input_mode != "voice_continuous":
                        print(f"✅ Gemini found: {url}")
                    
                    return url
            
            print(f"⚠️ Gemini API error: {response.status_code}")
            return None
            
        except requests.exceptions.Timeout:
            print("⚠️ Gemini API timeout. Using fallback.")
            if input_mode == "voice_continuous":
                speak("API timeout, using fallback")
            return None
        except Exception as e:
            print(f"⚠️ Error calling Gemini API: {e}")
            if input_mode == "voice_continuous":
                speak("API error, using fallback")
            return None
    
    def search_google(self, query):
        """Search Google for the given query"""
        input_mode = Config.get_input_mode()
        driver = self.driver_manager.get_driver()
        
        if not driver:
            return
        
        try:
            driver.get("https://www.google.com")
            self.driver_manager.reset_whatsapp_status()
            
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
        """Open an application or website using Gemini for URL resolution"""
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
                    self.driver_manager.reset_whatsapp_status()
                    
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
                    self.driver_manager.reset_whatsapp_status()
                    
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
            # Use Gemini to get the correct URL
            url = self.get_url_from_gemini(name)
            
            # Fallback to simple URL creation if Gemini fails
            if not url:
                url = f"https://www.{name}.com" if "." not in name else f"https://{name}"
                if input_mode != "voice_continuous":
                    print(f"ℹ️ Using fallback URL: {url}")
            
            webbrowser.open(url)
            msg = f"✅ Opened {url}\n"
            if input_mode == "voice_continuous":
                speak(f"Opened {name}")
            else:
                print(msg)