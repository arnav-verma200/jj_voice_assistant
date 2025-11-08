"""
Main command executor - routes commands to appropriate handlers
"""

from config import Config
from utils.tts import speak
from commands.spotify_commands import SpotifyCommands
from commands.whatsapp_commands import WhatsAppCommands
from commands.youtube_commands import YouTubeCommands
from commands.browser_commands import BrowserCommands
from commands.volume_commands import VolumeCommands


class CommandExecutor:
    """Execute commands by routing to appropriate handlers"""
    
    def __init__(self, driver_manager, input_handler):
        self.driver_manager = driver_manager
        self.input_handler = input_handler
        
        # Initialize command handlers
        self.spotify = SpotifyCommands()
        self.whatsapp = WhatsAppCommands(driver_manager)
        self.youtube = YouTubeCommands(driver_manager)
        self.browser = BrowserCommands(driver_manager)
        self.volume = VolumeCommands()
    
    def execute(self, command):
        """Execute the given command"""
        input_mode = Config.get_input_mode()
        
        # Empty command - continue loop
        if not command:
            return True
        
        # Exit command
        if command == "exit":
            self.volume.stop_volume_control()  # Stop volume control if running
            self.driver_manager.cleanup()
            msg = "Goodbye!"
            if input_mode == "voice_continuous":
                speak(msg)
            else:
                print(msg)
            return False
        
        # Volume control commands
        elif "volume control" in command or "vol control" in command or "start volume" in command:
            self.volume.start_volume_control()
        
        elif "stop volume" in command or "close volume" in command or "exit volume" in command:
            self.volume.stop_volume_control()
        
        # WhatsApp message command
        elif command.startswith("message"):
            self._handle_message_command(command)
        
        # Spotify commands - new format: "play <song> in/on spotify"
        elif " in spotify" in command or " on spotify" in command:
            self._handle_spotify_play_command(command)
        
        # Spotify control commands
        elif command.startswith("spotify "):
            action = command.replace("spotify ", "").strip()
            if action in ["pause", "play", "next", "previous", "prev", "back"]:
                self.spotify.control_playback(action)
            else:
                msg = f"❌ Unknown Spotify command: {action}\n"
                if input_mode == "voice_continuous":
                    speak(f"Unknown Spotify command")
                else:
                    print(msg)
        
        # Quick playback controls
        elif command in ["pause", "pause music"]:
            self.spotify.control_playback("pause")
        
        elif command in ["next", "next song", "skip"]:
            self.spotify.control_playback("next")
        
        elif command in ["previous", "previous song", "back", "go back"]:
            self.spotify.control_playback("previous")
        
        elif command == "open spotify":
            self.spotify.open_app()
        
        # YouTube commands - new format: "play <video> in/on youtube"
        elif " in youtube" in command or " on youtube" in command:
            self._handle_youtube_play_command(command)
        
        # Google search command
        elif command.startswith("search "):
            query = command.replace("search ", "", 1).strip()
            if query:
                self.browser.search_google(query)
            else:
                msg = "❌ No search query provided.\n"
                if input_mode == "voice_continuous":
                    speak("No search query provided")
                else:
                    print(msg)
        
        # Open app/website command
        elif command.startswith("open "):
            name = command.replace("open ", "", 1).strip()
            self.browser.open_app_or_website(name)
        
        # Unknown command
        else:
            msg = "❌ Unknown command. Available commands: play <song> in spotify, play <video> in youtube, spotify pause/next/prev, volume control, stop volume, search <query>, open <name>, message <contact>, exit\n"
            if input_mode == "voice_continuous":
                speak("Unknown command")
            else:
                print(msg)
        
        return True
    
    def _handle_message_command(self, command):
        """Handle WhatsApp message command"""
        input_mode = Config.get_input_mode()
        rest = command.replace("message", "", 1).strip()
        
        if rest:
            contact = rest
            
            # Ask for message
            msg = f"What message do you want to send to {contact}?"
            if input_mode == "voice_continuous":
                speak(msg)
            print(msg)
            
            message = self.input_handler.get_user_input("Enter message")
            
            if not message:
                msg = "❌ No message provided. Message cancelled.\n"
                if input_mode == "voice_continuous":
                    speak("Message cancelled")
                else:
                    print(msg)
                return
            
            # Send the message - will automatically select first search result
            self.whatsapp.send_message(contact, message)
        else:
            msg = "❌ No contact provided. Format: message <contact>\n"
            if input_mode == "voice_continuous":
                speak("No contact provided")
            else:
                print(msg)
    
    def _handle_spotify_play_command(self, command):
        """Handle Spotify play command"""
        input_mode = Config.get_input_mode()
        
        # Extract song name before "in spotify" or "on spotify"
        if " in spotify" in command:
            query = command.split(" in spotify")[0].strip()
        else:
            query = command.split(" on spotify")[0].strip()
        
        # Remove "play" prefix if present
        if query.startswith("play "):
            query = query.replace("play ", "", 1).strip()
        
        if query:
            self.spotify.play_song(query)
        else:
            msg = "❌ No song name provided.\n"
            if input_mode == "voice_continuous":
                speak("No song name provided")
            else:
                print(msg)
    
    def _handle_youtube_play_command(self, command):
        """Handle YouTube play command"""
        input_mode = Config.get_input_mode()
        
        # Extract video name before "in youtube" or "on youtube"
        if " in youtube" in command:
            query = command.split(" in youtube")[0].strip()
        else:
            query = command.split(" on youtube")[0].strip()
        
        # Remove "play" prefix if present
        if query.startswith("play "):
            query = query.replace("play ", "", 1).strip()
        
        if query:
            self.youtube.play_video(query)
        else:
            msg = "❌ No video name provided.\n"
            if input_mode == "voice_continuous":
                speak("No video name provided")
            else:
                print(msg)