# 🤖 JJ Voice Assistant

A powerful voice-controlled browser automation assistant that lets you control Spotify, send WhatsApp messages, play YouTube videos, and browse the web using simple voice commands or text input.

## ✨ Features

- 🎵 **Spotify Control** - Play songs, control playback (pause, next, previous)
- 💬 **WhatsApp Messaging** - Send messages via WhatsApp Web
- 🎥 **YouTube Player** - Search and play videos
- 🔍 **Google Search** - Perform web searches
- 🌐 **Website/App Launcher** - Open websites and applications
- 🎤 **Multiple Input Modes** - Voice (continuous or button-triggered) or text
- 🔒 **Persistent Sessions** - Login once to Google & WhatsApp, credentials saved for future use

## 🎯 Demo

```
Commands:
  • play despacito in spotify       - Play song on Spotify
  • play nodejs tutorial in youtube - Play video on YouTube
  • message John                     - Send WhatsApp message
  • search python tutorials          - Google search
  • open github                      - Open website
  • spotify pause                    - Pause Spotify
  • exit                            - Exit program
```

## 📋 Prerequisites

- **Python 3.7+**
- **Google Chrome** (installed at default location)
- **Spotify Desktop App** (for music playback)
- **Microphone** (for voice input modes)
- **WhatsApp Account** (for messaging features)

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/jj-voice-assistant.git
cd jj-voice-assistant
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note for Windows users:** PyAudio installation might require additional steps. If you encounter issues:

```bash
pip install pipwin
pipwin install pyaudio
```

### 3. Chrome Path Configuration

The default Chrome path is set for Windows. If your Chrome is installed elsewhere, update `config.py`:

```python
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
```

## 🎮 Usage

### Starting the Assistant

```bash
python main.py
```

### Input Modes

You'll be prompted to choose an input mode:

#### 1. **Continuous Voice Control** (Always Listening)
- The assistant continuously listens for commands
- Always start commands with "jj" (e.g., "jj play despacito in spotify")
- Press **ESC** to stop listening and exit

#### 2. **Button Voice Control** (Push-to-Talk)
- Hold **SPACE** to speak your command
- Release to transcribe
- Always start commands with "jj"
- Press **ESC** to cancel

#### 3. **Typing Mode**
- Type commands directly
- No need to say "jj" prefix

## 📝 Command Reference

### Spotify Commands

```bash
play <song name> in spotify    # Play a specific song
play <song name> on spotify    # Alternative syntax
spotify pause                  # Pause playback
spotify play                   # Resume playback
spotify next                   # Next track
spotify previous               # Previous track
pause                         # Quick pause
next                          # Quick next
previous                      # Quick previous
open spotify                  # Open Spotify app
```

### YouTube Commands

```bash
play <video name> in youtube   # Search and play video
play <video name> on youtube   # Alternative syntax
```

### WhatsApp Commands

```bash
message <contact name>         # Send message to contact
```

**Important:** WhatsApp will automatically select the **first search result**. Make sure to use distinctive contact names.

### Browser Commands

```bash
search <query>                 # Google search
open <website/app>             # Open website or application
```

Examples:
- `search python tutorials`
- `open github`
- `open youtube`
- `open notepad`

### System Commands

```bash
exit                          # Exit the assistant
```

## 🏗️ Project Structure

```
jj-voice-assistant/
│
├── main.py                   # Application entry point
├── config.py                 # Configuration settings
├── requirements.txt          # Python dependencies
├── README.md                # Documentation
│
├── commands/                # Command handlers
│   ├── __init__.py
│   ├── command_executor.py  # Main command router
│   ├── spotify_commands.py  # Spotify operations
│   ├── whatsapp_commands.py # WhatsApp operations
│   ├── youtube_commands.py  # YouTube operations
│   └── browser_commands.py  # Browser/search operations
│
└── utils/                   # Utility modules
    ├── __init__.py
    ├── driver_manager.py    # Selenium WebDriver management
    ├── input_handler.py     # Input mode handling
    ├── voice_input.py       # Voice recognition
    └── tts.py              # Text-to-speech
```

## ⚙️ Configuration

Edit `config.py` to customize:

```python
# Chrome settings
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# Voice settings
SPEECH_RATE = 175           # TTS speech rate
SPEECH_VOLUME = 0.9         # TTS volume (0.0 to 1.0)

# Timeout settings
VOICE_LISTEN_TIMEOUT = 10   # Voice listening timeout
WHATSAPP_QR_SCAN_TIMEOUT = 120  # WhatsApp QR scan timeout
```

## 🔧 First-Time Setup

### Google Account
When Chrome opens for the first time, sign in to your Google account. Your session will be saved for future use.

### WhatsApp Web
1. The first time you use WhatsApp commands, WhatsApp Web will open
2. Scan the QR code with your phone
3. Your session will be saved for future use

### Spotify
Ensure Spotify desktop app is installed on your system. The assistant uses Spotify's URI protocol to control playback.

## 🐛 Troubleshooting

### Microphone Not Working
- Check if your microphone is properly connected
- Grant microphone permissions to Python
- Adjust `MICROPHONE_CALIBRATION_DURATION` in `config.py`

### Chrome Not Opening
- Verify Chrome installation path in `config.py`
- Ensure ChromeDriver is compatible with your Chrome version
- Check if Chrome is already running with incompatible flags

### Spotify Not Responding
- Ensure Spotify desktop app is installed
- Verify Spotify is not blocked by firewall
- Try opening Spotify manually first

### WhatsApp Issues
- Ensure you're logged into WhatsApp Web
- Check your internet connection
- Increase `WHATSAPP_LOGIN_TIMEOUT` in `config.py` if needed

### Voice Recognition Errors
```bash
# Install/reinstall PyAudio
pip uninstall pyaudio
pip install pyaudio

# Or use pipwin on Windows
pip install pipwin
pipwin install pyaudio
```

## 🔐 Privacy & Security

- Chrome sessions are stored locally in `ChromeAutomation` folder in your home directory
- No credentials or personal data are transmitted outside your local machine
- WhatsApp and Google sessions are maintained by Selenium for automation purposes
- You can clear saved sessions by deleting the `ChromeAutomation` folder

## 🛠️ Dependencies

- **selenium** - Browser automation
- **webdriver-manager** - Automatic ChromeDriver management
- **SpeechRecognition** - Voice recognition
- **keyboard** - Keyboard event handling
- **pyttsx3** - Text-to-speech
- **pyautogui** - GUI automation for Spotify controls
- **PyAudio** - Microphone access

## 🤝 Contributing

Contributions are welcome! Here are some ways you can contribute:

1. Report bugs and issues
2. Suggest new features
3. Submit pull requests
4. Improve documentation

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## ⚠️ Disclaimer

This project is for educational purposes. Be mindful of:
- Web scraping policies of websites
- Terms of service for Spotify, WhatsApp, and YouTube
- Rate limiting and automation restrictions
- Responsible use of automation tools

## 👨‍💻 Author

Created with ❤️ by JJ Voice Assistant Team

## 🙏 Acknowledgments

- Google Speech Recognition API
- Selenium WebDriver
- pyttsx3 for TTS capabilities
- All open-source contributors

---

**Happy Automating! 🚀**

For issues and feature requests, please open an issue on GitHub.
