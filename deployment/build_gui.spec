# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for JJ Voice Assistant GUI version
Build command: pyinstaller build_gui.spec
"""

block_cipher = None

a = Analysis(
    ['../src/gui.py'],
    pathex=['../src'],
    binaries=[],
    datas=[],
    hiddenimports=[
        # Text-to-speech engine
        'pyttsx3',
        'pyttsx3.drivers',
        'pyttsx3.drivers.sapi5',
        
        # Computer vision and gesture control
        'cv2',
        'mediapipe',
        
        # Audio control
        'pycaw',
        'pycaw.pycaw',
        'comtypes',
        
        # Web automation
        'selenium',
        'selenium.webdriver',
        'selenium.webdriver.chrome',
        'selenium.webdriver.chrome.service',
        'webdriver_manager',
        'webdriver_manager.chrome',
        
        # Voice recognition
        'speech_recognition',
        
        # Keyboard control
        'keyboard',
        'pyautogui',
        
        # AI integration
        'google.generativeai',
        'google.ai.generativelanguage',
        
        # Environment variables
        'dotenv',
        
        # GUI framework
        'PySide6',
        'PySide6.QtCore',
        'PySide6.QtWidgets',
        'PySide6.QtGui',
        
        # All project modules
        'config',
        'commands',
        'commands.command_executor',
        'commands.spotify_commands',
        'commands.whatsapp_commands',
        'commands.youtube_commands',
        'commands.browser_commands',
        'commands.volume_commands',
        'utils',
        'utils.driver_manager',
        'utils.input_handler',
        'utils.voice_input',
        'utils.tts',
        'utils.utils_frozen',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude other GUI frameworks
        'PyQt5',
        'PyQt6',
        'tkinter',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='jj_voice_assistant_gui',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # GUI doesn't need console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Can add custom icon later
)
