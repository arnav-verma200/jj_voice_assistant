"""
Spotify-related commands
"""

import os
import time
import urllib.parse
import pyautogui
from config import Config
from utils.tts import speak


class SpotifyCommands:
    """Handle Spotify-related operations"""
    
    @staticmethod
    def play_song(query):
        """Play a song on Spotify app"""
        input_mode = Config.get_input_mode()
        msg = f"🎵 Searching Spotify for: {query}"
        if input_mode == "voice_continuous":
            speak(f"Playing {query} on Spotify")
        else:
            print(msg)
        
        try:
            search_query = urllib.parse.quote(query)
            spotify_uri = f"spotify:search:{search_query}"
            os.startfile(spotify_uri)
            
            time.sleep(2)
            pyautogui.press('enter')
            
            msg = f"✅ Playing: {query} on Spotify\n"
            if input_mode != "voice_continuous":
                print(msg)
                
        except Exception as e:
            msg = f"❌ Error: {e}. Make sure Spotify is installed.\n"
            if input_mode == "voice_continuous":
                speak("Error opening Spotify. Make sure it's installed.")
            else:
                print(msg)
    
    @staticmethod
    def control_playback(action):
        """Control Spotify playback using media keys"""
        input_mode = Config.get_input_mode()
        
        try:
            if action == "pause":
                pyautogui.press('playpause')
                msg = "⏸️ Spotify paused"
            elif action == "play":
                pyautogui.press('playpause')
                msg = "▶️ Spotify playing"
            elif action == "next":
                pyautogui.press('nexttrack')
                msg = "⏭️ Next song"
            elif action == "previous" or action == "prev" or action == "back":
                pyautogui.press('prevtrack')
                msg = "⏮️ Previous song"
            else:
                msg = "❌ Unknown action"
            
            if input_mode == "voice_continuous":
                speak(msg)
            else:
                print(msg + "\n")
                
        except Exception as e:
            msg = f"❌ Error controlling Spotify: {e}"
            if input_mode == "voice_continuous":
                speak("Error controlling Spotify")
            else:
                print(msg + "\n")
    
    @staticmethod
    def open_app():
        """Open Spotify app"""
        input_mode = Config.get_input_mode()
        
        try:
            os.startfile("spotify:")
            msg = "✅ Opened Spotify"
            if input_mode == "voice_continuous":
                speak("Opened Spotify")
            else:
                print(msg + "\n")
        except Exception as e:
            msg = f"❌ Error opening Spotify: {e}"
            if input_mode == "voice_continuous":
                speak("Error opening Spotify")
            else:
                print(msg + "\n")