"""
Handle different input modes (voice continuous, voice button, typing)
"""

from utils.voice_input import VoiceInput
from utils.tts import speak


class InputHandler:
    """Manage user input across different modes"""
    
    def __init__(self, input_mode):
        self.input_mode = input_mode
        self.voice_input = VoiceInput() if input_mode in ["voice_continuous", "voice_button"] else None
    
    def get_command(self, first_run=False):
        """Get command from user based on input mode"""
        if self.input_mode == "voice_continuous":
            voice_input = self.voice_input.get_continuous_input(first_run=first_run)
            
            if voice_input is None:
                return None
            
            command = voice_input.lower().replace("jj", "", 1).strip()
            print(f"⚡ Executing: {command}\n")
            return command
        
        elif self.input_mode == "voice_button":
            print("\n[Voice Mode - Say 'jj' first]")
            voice_input = self.voice_input.get_button_input()
            
            if voice_input:
                voice_input_lower = voice_input.lower().strip()
                
                if voice_input_lower.startswith("jj"):
                    command = voice_input_lower.replace("jj", "", 1).strip()
                    print(f"\n⚡ Executing: {command}\n")
                    return command
                else:
                    print("❌ Command ignored. Please start with 'jj'")
                    return ""  # Return empty to continue loop
            else:
                print("❌ No voice command received.")
                return ""  # Return empty to continue loop
        
        else:  # typing mode
            return input("\nCommand: ").lower().strip()
    
    def get_user_input(self, prompt_text):
        """Get generic input from user (used for follow-up questions)"""
        if self.input_mode == "voice_continuous":
            speak(prompt_text)
            print(f"\n{prompt_text}")
            print("🎤 Say 'jj' followed by your response...")
            
            voice_input = self.voice_input.get_continuous_input(first_run=False)
            if voice_input is None:
                return None
            
            response = voice_input.lower().replace("jj", "", 1).strip()
            print(f"📢 You said: {response}")
            return response
        
        elif self.input_mode == "voice_button":
            speak(prompt_text)
            print(f"\n{prompt_text}")
            print("Hold SPACE and say 'jj' followed by your response...")
            
            voice_input = self.voice_input.get_button_input()
            if voice_input:
                voice_input_lower = voice_input.lower().strip()
                if voice_input_lower.startswith("jj"):
                    response = voice_input_lower.replace("jj", "", 1).strip()
                    print(f"📢 You said: {response}")
                    return response
                else:
                    print("❌ Response ignored. Please start with 'jj'")
                    return None
            return None
        
        else:  # typing mode
            return input(f"{prompt_text}: ").strip()