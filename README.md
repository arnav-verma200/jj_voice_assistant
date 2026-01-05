# 🤖 JJ Voice Assistant

A powerful voice-controlled browser automation assistant that lets you control Spotify, send WhatsApp messages, play YouTube videos, manage volume with hand gestures, and browse the web using simple voice commands or text input.

---

## ✨ Features

- 🎵 **Spotify Control** - Play songs, control playback (pause, next, previous)
- 💬 **WhatsApp Messaging** - Send messages via WhatsApp Web
- 🎥 **YouTube Player** - Search and play videos
- 🔍 **Google Search** - Perform web searches
- 🌐 **Smart Website Launcher** - AI-powered URL detection for websites and apps
- 🎚️ **Gesture Volume Control** - Adjust system volume using hand gestures via webcam
- 🎤 **Multiple Input Modes** - Voice (continuous or button-triggered) or text
- 🖥️ **GUI Mode** - Modern graphical interface available
- 🔒 **Persistent Sessions** - Login once to Google & WhatsApp, credentials saved for future use

---

## 📋 Prerequisites

- Python 3.7+
- Google Chrome (installed)
- Spotify Desktop App (for music playback)
- Microphone (for voice input modes)
- Webcam (for gesture volume control)
- WhatsApp Account (for messaging features)
- Gemini API Key (optional, for AI-powered URL detection)

---

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

**For Windows users with PyAudio issues:**

```bash
pip install pipwin
pipwin install pyaudio
```

### 3. Setup Gemini API (Optional)

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

Get your free API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

### 4. Configure Chrome Path (if needed)

If Chrome is not installed at the default location, edit `config.py`:

```python
CHROME_PATH = r"C:\Your\Custom\Path\chrome.exe"
```

---

## 🎮 Usage

### CLI Mode

```bash
python main.py
```

**Select Input Mode:**
- `1` - Continuous Voice Control (Always Listening - say "jj" before commands)
- `2` - Button Voice Control (Hold Alt+A to speak)
- `3` - Typing Mode

### GUI Mode

```bash
python gui.py
```

---

## 📝 Commands Reference

### 🎵 Spotify Commands

```bash
# Play Songs
play despacito in spotify
play shape of you on spotify
play bohemian rhapsody in spotify

# Playback Control
spotify pause              # Pause playback
spotify play               # Resume playback
spotify next               # Next track
spotify previous           # Previous track
spotify prev               # Previous track (short)
spotify back               # Previous track (alternative)

# Quick Controls (without "spotify" prefix)
pause                      # Pause current playback
next                       # Skip to next track
previous                   # Go to previous track
skip                       # Skip track
go back                    # Previous track

# App Control
open spotify               # Launch Spotify app
```

### 🎥 YouTube Commands

```bash
# Play Videos
play nodejs tutorial in youtube
play funny cats on youtube
play how to cook pasta in youtube

# Alternative Syntax
play meditation music on youtube
play workout video on youtube

# Open YouTube
open youtube
```

### 💬 WhatsApp Commands

```bash
# Send Message (Interactive)
message John               # Send message to John
message Mom                # Send message to Mom
message Sarah              # Send message to Sarah

# Process:
# 1. Assistant searches for contact
# 2. Automatically selects FIRST result
# 3. Asks you for the message
# 4. Sends the message

# Note: WhatsApp automatically selects the first search result
```

### 🌐 Browser & Search Commands

```bash
# Google Search
search python tutorials
search best restaurants
search latest news
search how to code

# Open Websites (AI-Powered)
open youtube
open github
open facebook
open instagram
open twitter
open reddit
open netflix
open amazon
open flipkart

# Open Government Sites
open sih                   # Smart India Hackathon
open aadhaar              # UIDAI portal
open passport             # Passport Seva
open digilocker           # DigiLocker
open cowin                # CoWIN portal
open pan card             # PAN services

# Open Exam/Education Portals
open jee mains            # JEE Mains portal
open jee advanced         # JEE Advanced portal
open neet                 # NEET exam portal
open cuet                 # CUET portal
open gate                 # GATE exam portal
open upsc                 # UPSC portal
open ssc                  # SSC portal

# Open College/University Sites
open iit bombay
open iit delhi
open nit warangal
open vit vellore
open jiit 62

# Open Banking Sites
open sbi
open hdfc bank
open icici
open axis bank

# Open OTT Platforms
open netflix
open amazon prime
open hotstar
open zee5

# Open Tech Services
open chatgpt
open claude
open gemini
open gmail
open drive

# Open Any Website
open example.com           # Opens any domain
open website.co.in        # Supports all TLDs
```

### 🎚️ Volume Control Commands

```bash
# Start Gesture Control
volume control
vol control
start volume
start volume control

# Stop Gesture Control
stop volume
close volume
exit volume
close volume control
exit volume control

# How It Works:
# - Uses webcam to track hand gestures
# - Pinch thumb and index finger together
# - Move fingers apart = increase volume
# - Move fingers closer = decrease volume
# - Distance controls volume (0-100%)
```

### 🚪 System Commands

```bash
exit                       # Exit the assistant
```

---

## ⚙️ Configuration

Edit `config.py` to customize:

```python
# Chrome settings
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# Voice settings
SPEECH_RATE = 175          # TTS speech rate
SPEECH_VOLUME = 0.9        # TTS volume (0.0 to 1.0)

# Timeout settings
VOICE_LISTEN_TIMEOUT = 10
WHATSAPP_QR_SCAN_TIMEOUT = 120
```

---

## 🔑 First-Time Setup

### 1. Google Account
- Chrome will open automatically
- Sign in to your Google account
- Your session will be saved for future use

### 2. WhatsApp Web
- First WhatsApp command opens WhatsApp Web
- Scan the QR code with your phone
- Session persists across restarts

### 3. Spotify Desktop
- Install Spotify Desktop App from [spotify.com](https://www.spotify.com/download/)
- No additional login required in assistant

---

## 📁 Project Structure

```
jj-voice-assistant/
│
├── main.py                   # CLI entry point
├── gui.py                    # GUI entry point
├── config.py                 # Configuration
├── requirements.txt          # Dependencies
├── .env                      # API keys
│
├── commands/                 # Command handlers
│   ├── command_executor.py
│   ├── spotify_commands.py
│   ├── whatsapp_commands.py
│   ├── youtube_commands.py
│   ├── browser_commands.py
│   └── volume_commands.py
│
└── utils/                    # Utilities
    ├── driver_manager.py
    ├── input_handler.py
    ├── voice_input.py
    └── tts.py
```

---

## 💡 Important Notes

### Voice Mode Tips
- **Continuous Mode**: Always say "jj" before your command (e.g., "jj play despacito in spotify")
- **Button Mode**: Hold Alt+A while speaking
- Press **ESC** to stop voice mode at any time

### WhatsApp Messaging
- The assistant automatically selects the **first search result**
- Use distinctive contact names to avoid confusion
- Make sure you're logged into WhatsApp Web on your phone

### Volume Control
- Requires a working webcam
- Good lighting improves gesture detection
- Pinch thumb and index finger to control
- Press 'o' to close the volume control window

### Spotify Control
- Requires Spotify **Desktop App** (not web player)
- Media keys are used for playback control
- Works even when Spotify is in background

### AI-Powered URL Detection
- Requires Gemini API key in `.env` file
- Supports 1000+ popular websites
- Falls back to standard method if AI unavailable
- Free tier: 60 requests per minute

---

## 🔐 Privacy & Security

- All Chrome sessions are stored locally in `ChromeAutomation` folder
- No credentials are transmitted outside your local machine
- WhatsApp and Google sessions maintained by Selenium
- You can clear saved sessions by deleting the `ChromeAutomation` folder

**Clear Sessions:**
```bash
# Windows
rmdir /s "%USERPROFILE%\ChromeAutomation"

# Linux/Mac
rm -rf ~/ChromeAutomation
```

---

## 📦 Dependencies

- selenium
- webdriver-manager
- SpeechRecognition
- keyboard
- pyttsx3
- pyautogui
- PyAudio
- opencv-python
- mediapipe
- pycaw
- comtypes
- google-generativeai
- python-dotenv
- PySide6 (for GUI mode)

---

## 📄 License

This project is open source and available under the MIT License.

---

## ⚠️ Disclaimer

This project is for educational purposes. Be mindful of:
- Web scraping policies of websites
- Terms of service for Spotify, WhatsApp, and YouTube
- Rate limiting and automation restrictions
- Responsible use of automation tools

---

**Happy Automating! 🚀**
