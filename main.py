"""
JJ Voice Assistant - Main Entry Point
Handles user interaction and command routing
"""
from config import Config
from utils.driver_manager import DriverManager
from utils.input_handler import InputHandler
from commands.command_executor import CommandExecutor


def print_welcome_banner():
    """Display welcome banner and instructions"""
    print("=" * 60)
    print("🤖 jj - Voice Controlled Browser Automation")
    print("=" * 60)
    print("\nSelect Input Mode:")
    print("1 - Continuous Voice Control (Always Listening)")
    print("2 - Button Voice Control (Press SPACE to talk)")
    print("3 - Typing")
    print("-" * 60)


def get_input_mode():
    """Get user's preferred input mode"""
    while True:
        mode_choice = input("\nEnter your choice (1, 2, or 3): ").strip()
        if mode_choice == "1":
            print("\n✅ Continuous Voice Mode Activated!")
            print("🎤 I'm always listening for 'jj' commands")
            print("⚠️ Press ESC anytime to stop\n")
            return "voice_continuous"
        elif mode_choice == "2":
            print("\n✅ Button Voice Mode Activated!")
            print("🎤 Hold SPACE to speak your commands")
            print("⚠️ Start every command with 'jj'\n")
            return "voice_button"
        elif mode_choice == "3":
            print("\n✅ Typing Mode Activated!\n")
            return "typing"
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")


def print_commands():
    """Display available commands"""
    print("\nCommands:")
    print("  • play <song> in spotify       - Play song on Spotify")
    print("  • play <video> in youtube      - Play video on YouTube")
    print("  • spotify pause/next/prev      - Control Spotify playback")
    print("  • pause / next / previous      - Quick playback control")
    print("  • open spotify                 - Open Spotify app")
    print("  • volume control               - Start gesture volume control")
    print("  • stop volume                  - Stop volume control")
    print("  • message <contact>            - Send WhatsApp message")
    print("  • search <query>               - Google search")
    print("  • open <app/website>           - Open application or website")
    print("  • exit                         - Exit program")
    print("-" * 60)
    print("\nℹ️ First time? Sign in to Google & WhatsApp when Chrome opens!")
    print("Your login will be saved for future sessions.")
    print("\n💡 TIP: Make sure Spotify is installed for music playback!")
    print("💡 TIP: WhatsApp will ALWAYS message the first person in search results!")
    print("💡 TIP: Volume control uses your webcam - pinch thumb and index finger!\n")


def main():
    """Main application loop"""
    try:
        print_welcome_banner()
        input_mode = get_input_mode()
        print_commands()
        
        # Initialize components
        Config.set_input_mode(input_mode)
        driver_manager = DriverManager()
        input_handler = InputHandler(input_mode)
        command_executor = CommandExecutor(driver_manager, input_handler)
        
        first_voice_command = True
        
        # Main command loop
        while True:
            command = input_handler.get_command(first_run=first_voice_command)
            first_voice_command = False
            
            if command is None:
                driver_manager.cleanup()
                break
            
            should_continue = command_executor.execute(command)
            if not should_continue:
                break
    
    except KeyboardInterrupt:
        print("\n\n⚠️ Interrupted by user...")
        driver_manager.cleanup()
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        driver_manager.cleanup()


if __name__ == "__main__":
    main()