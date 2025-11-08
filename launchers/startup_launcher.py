"""
JJ Voice Assistant - Startup Launcher
This script runs at PC startup and prompts for input mode selection
"""

import subprocess
import sys
import os
from pathlib import Path


def print_banner():
    """Display startup banner"""
    print("=" * 60)
    print("🤖 JJ Voice Assistant - Startup Launcher")
    print("=" * 60)


def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'selenium',
        'speech_recognition',
        'keyboard',
        'pyttsx3',
        'pyautogui'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing.append(package)
    
    if missing:
        print("\n⚠️ WARNING: Missing required packages:")
        for pkg in missing:
            print(f"  - {pkg}")
        print("\nInstall them with: pip install -r requirements.txt")
        print()
        return False
    return True


def main():
    # Get the directory where this script is located
    script_dir = Path(__file__).parent.absolute()
    main_script = script_dir / "main.py"
    
    print_banner()
    print(f"\n📁 Working Directory: {script_dir}")
    print(f"🐍 Python Version: {sys.version.split()[0]}")
    print(f"💻 Python Executable: {sys.executable}")
    print()
    
    # Check if main.py exists
    if not main_script.exists():
        print(f"❌ Error: main.py not found!")
        print(f"   Expected location: {main_script}")
        print(f"\n   Current files in directory:")
        for f in script_dir.iterdir():
            if f.is_file():
                print(f"     - {f.name}")
        input("\n⏸️ Press Enter to exit...")
        return 1
    
    print("✅ main.py found!")
    
    # Check dependencies
    print("\n🔍 Checking dependencies...")
    if not check_dependencies():
        response = input("\n⚠️ Continue anyway? (y/n): ").strip().lower()
        if response != 'y':
            return 1
    else:
        print("✅ All dependencies installed!")
    
    print("\n" + "=" * 60)
    print("🚀 Starting JJ Voice Assistant...")
    print("=" * 60)
    print("\n📝 You will be prompted to select input mode:")
    print("  1 - Continuous Voice Control (Always Listening)")
    print("  2 - Button Voice Control (Press SPACE to talk)")
    print("  3 - Typing Mode")
    print("\n" + "=" * 60 + "\n")
    
    try:
        # Run main.py in the same console window
        result = subprocess.run(
            [sys.executable, str(main_script)],
            cwd=str(script_dir)
        )
        
        print("\n" + "=" * 60)
        # If the program exits normally
        if result.returncode == 0:
            print("✅ JJ Assistant closed successfully")
        else:
            print(f"⚠️ JJ Assistant exited with code {result.returncode}")
        print("=" * 60)
            
    except KeyboardInterrupt:
        print("\n\n⚠️ Interrupted by user...")
        return 130
    except Exception as e:
        print(f"\n❌ Error running JJ Assistant: {e}")
        print(f"   Exception type: {type(e).__name__}")
        input("\n⏸️ Press Enter to exit...")
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)