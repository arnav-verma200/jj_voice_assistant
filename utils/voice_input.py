"""
Voice input recognition utilities
"""

import time
import speech_recognition as sr
import keyboard
from config import Config
from utils.tts import speak


class VoiceInput:
    """Handle voice input recognition"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
    
    def get_continuous_input(self, first_run=False):
        """Listen continuously for voice commands starting with 'jj'"""
        if first_run:
            speak("Hello I am Jamnalaal Jamdaas in short JJ")
            time.sleep(0.1)
            print("Calibrating microphone for ambient noise... Please wait...")
            speak("Calibrating microphone, please wait")
            
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=Config.MICROPHONE_CALIBRATION_DURATION)
            
            print("Calibration complete! Listening continuously. Press ESC to stop listening.")
            speak("Ready. I'm listening")
        
        while True:
            if keyboard.is_pressed("esc"):
                print("Stopping continuous listening...")
                speak("Goodbye")
                return None
            
            try:
                with self.microphone as source:
                    if first_run:
                        self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    print("🎤 Listening... say 'jj' to give a command")
                    audio = self.recognizer.listen(
                        source, 
                        timeout=Config.VOICE_LISTEN_TIMEOUT, 
                        phrase_time_limit=Config.VOICE_PHRASE_TIME_LIMIT
                    )
                    
                    print("🔄 Processing...")
                    text = self.recognizer.recognize_google(audio)
                    print(f"📢 Heard: {text}")
                    
                    if text.lower().strip().startswith("jj"):
                        return text
                    else:
                        print("❌ Command ignored (didn't start with 'jj')\n")
                        
            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                print("❓ Could not understand, still listening...\n")
                continue
            except sr.RequestError as e:
                print(f"❌ Recognition service error: {e}")
                speak("Recognition service error")
                time.sleep(1)
                continue
            except Exception as e:
                print(f"❌ Error: {e}")
                speak("An error occurred")
                time.sleep(1)
                continue
    
    def get_button_input(self):
        """Listen for voice input when SPACE is pressed"""
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            print("Hold Alt+A to speak... release to stop and transcribe.")
            if retry_count > 0:
                print(f"Retry {retry_count}/{max_retries}")
            print("Press ESC to cancel.\n")
            
            while True:
                time.sleep(0.01)
                
                if keyboard.is_pressed("esc"):
                    print("Cancelled.")
                    return None

                if keyboard.is_pressed("alt+a"):
                    print("Listening...")
                    with self.microphone as source:
                        self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                        start_time = time.time()
                        try:
                            audio = self.recognizer.listen(source, timeout=30, phrase_time_limit=20)
                            duration = time.time() - start_time
                            print(f"Recognizing ({duration:.1f}s)...")
                            
                            text = self.recognizer.recognize_google(audio)
                            print("You said:", text)
                            return text
                            
                        except sr.WaitTimeoutError:
                            print("No speech detected.")
                            retry_count += 1
                            break
                        except sr.UnknownValueError:
                            print("Could not understand. Please try again...")
                            retry_count += 1
                            break
                        except sr.RequestError as e:
                            print(f"Recognition service error: {e}")
                            return None
                        finally:
                            while keyboard.is_pressed("alt+a"):
                                time.sleep(0.01)
        
        print(f"Failed after {max_retries} attempts.")
        return None