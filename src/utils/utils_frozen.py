"""
Utilities for handling frozen (PyInstaller) execution
"""

import sys
import os


def get_resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and PyInstaller.
    
    Args:
        relative_path: Path relative to the application root
        
    Returns:
        Absolute path to the resource
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # Running in normal Python environment
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)


def is_frozen():
    """
    Check if running as frozen executable.
    
    Returns:
        True if running as PyInstaller executable, False otherwise
    """
    return getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')


def get_exe_directory():
    """
    Get directory where executable is located.
    For development mode, returns current working directory.
    
    Returns:
        Absolute path to executable directory
    """
    if is_frozen():
        return os.path.dirname(sys.executable)
    return os.path.abspath(".")


def get_env_file_path():
    """
    Get path to .env file.
    In frozen mode, looks for .env next to the executable.
    In dev mode, looks in current directory.
    
    Returns:
        Absolute path to .env file
    """
    exe_dir = get_exe_directory()
    return os.path.join(exe_dir, ".env")
