"""
Selenium WebDriver management
"""

import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from config import Config
from utils.tts import speak

# Edge-specific imports (loaded conditionally)
try:
    from selenium.webdriver.edge.service import Service as EdgeService
    from selenium.webdriver.edge.options import Options as EdgeOptions
    from webdriver_manager.microsoft import EdgeChromiumDriverManager
    EDGE_AVAILABLE = True
except ImportError:
    EDGE_AVAILABLE = False
    print("⚠️ Edge dependencies not available. Edge browser support disabled.")


class DriverManager:
    """Manage Selenium WebDriver lifecycle"""
    
    def __init__(self):
        self.driver = None
        self.whatsapp_logged_in = False
    
    def get_driver(self):
        if self.driver:
            # Try to check if session is still alive
            try:
                self.driver.current_url  # This will fail if session is dead
            except:
                # Session is dead, clean up and create new one
                self.driver = None
    
        if not self.driver:
            self.driver = self._create_driver()
    
        return self.driver
    
    def _create_driver(self):
        """Create a new WebDriver instance based on detected browser"""
        
        # Check if browser was detected
        if not Config.BROWSER_PATH:
            error_msg = "No supported browser found. Please install Chrome or Edge."
            print(f"❌ {error_msg}")
            if Config.get_input_mode() == "voice_continuous":
                speak(error_msg)
            return None
        
        browser_type = Config.BROWSER_TYPE
        print(f"Creating {browser_type.upper()} driver...")
        
        # Create user data directory if it doesn't exist
        if not os.path.exists(Config.USER_DATA_DIR):
            os.makedirs(Config.USER_DATA_DIR)
        
        # Try to create driver based on browser type
        try:
            if browser_type == "edge":
                return self._create_edge_driver()
            else:
                # Chrome, Brave, and Chromium all use Chrome driver
                return self._create_chrome_based_driver()
                
        except Exception as e:
            print(f"Error creating {browser_type} driver: {e}")
            print("Trying fallback method...")
            
            # Fallback: try simpler configuration
            try:
                if browser_type == "edge":
                    return self._create_edge_driver_simple()
                else:
                    return self._create_chrome_based_driver_simple()
            except Exception as e2:
                print(f"Failed with fallback: {e2}")
                
                # Final fallback for Edge: use it as Chrome-like browser
                if browser_type == "edge":
                    print("Attempting Edge with Chrome driver (compatibility mode)...")
                    try:
                        return self._create_edge_as_chrome()
                    except Exception as e3:
                        print(f"Compatibility mode failed: {e3}")
                
                if Config.get_input_mode() == "voice_continuous":
                    speak("Failed to open browser")
                return None
    
    def _create_chrome_based_driver(self):
        """Create Chrome/Brave/Chromium driver with full options"""
        options = ChromeOptions()
        options.binary_location = Config.BROWSER_PATH
        
        options.add_argument(f"--user-data-dir={Config.USER_DATA_DIR}")
        options.add_argument("--profile-directory=Default")
        options.add_argument("--remote-allow-origins=*")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--start-maximized")
        options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
        options.add_experimental_option("useAutomationExtension", False)
        
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()), 
            options=options
        )
        print(f"{Config.BROWSER_TYPE.upper()} opened successfully!")
        return driver
    
    def _create_chrome_based_driver_simple(self):
        """Fallback: Create Chrome/Brave/Chromium driver with minimal options"""
        options = ChromeOptions()
        options.binary_location = Config.BROWSER_PATH
        options.add_argument("--remote-allow-origins=*")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--start-maximized")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()), 
            options=options
        )
        print(f"{Config.BROWSER_TYPE.upper()} opened (temporary session)")
        return driver
    
    def _create_edge_driver(self):
        """Create Edge driver - try auto-detection first, then webdriver-manager"""
        if not EDGE_AVAILABLE:
            raise ImportError("Edge webdriver dependencies not available")
        
        options = EdgeOptions()
        options.binary_location = Config.BROWSER_PATH
        
        options.add_argument(f"--user-data-dir={Config.USER_DATA_DIR}")
        options.add_argument("--profile-directory=Default")
        options.add_argument("--remote-allow-origins=*")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--start-maximized")
        options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
        options.add_experimental_option("useAutomationExtension", False)
        
        # Method 1: Try without specifying driver path (let Selenium auto-detect)
        try:
            print("Trying Edge auto-detection...")
            driver = webdriver.Edge(options=options)
            print("✓ EDGE opened successfully (auto-detected driver)!")
            return driver
        except Exception as e1:
            print(f"Auto-detection failed: {e1}")
        
        # Method 2: Try with webdriver-manager
        try:
            print("Trying Edge with webdriver-manager...")
            driver_path = EdgeChromiumDriverManager().install()
            print(f"Edge driver installed at: {driver_path}")
            driver = webdriver.Edge(
                service=EdgeService(driver_path), 
                options=options
            )
            print("✓ EDGE opened successfully (webdriver-manager)!")
            return driver
        except Exception as e2:
            print(f"webdriver-manager failed: {e2}")
            raise
    
    def _create_edge_driver_simple(self):
        """Fallback: Create Edge driver with minimal options"""
        if not EDGE_AVAILABLE:
            raise ImportError("Edge webdriver dependencies not available")
        
        options = EdgeOptions()
        options.binary_location = Config.BROWSER_PATH
        options.add_argument("--remote-allow-origins=*")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--start-maximized")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        # Try auto-detection first
        try:
            print("Trying Edge simple auto-detection...")
            driver = webdriver.Edge(options=options)
            print("✓ EDGE opened (simple, auto-detected)!")
            return driver
        except Exception as e1:
            print(f"Simple auto-detection failed: {e1}")
        
        # Try with webdriver-manager
        try:
            print("Trying Edge simple with webdriver-manager...")
            driver_path = EdgeChromiumDriverManager().install()
            driver = webdriver.Edge(
                service=EdgeService(driver_path), 
                options=options
            )
            print("✓ EDGE opened (simple, webdriver-manager)!")
            return driver
        except Exception as e2:
            print(f"Simple webdriver-manager failed: {e2}")
            raise
    
    def _create_edge_as_chrome(self):
        """
        Emergency fallback: Use Edge browser with Chrome WebDriver
        This works because Edge is Chromium-based
        """
        print("⚠️ Using Edge browser with Chrome driver (compatibility mode)...")
        options = ChromeOptions()
        options.binary_location = Config.BROWSER_PATH
        
        # Don't use user-data-dir in compatibility mode (causes crashes)
        options.add_argument("--remote-allow-origins=*")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
        
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()), 
            options=options
        )
        print("✓ EDGE opened using Chrome driver (compatibility mode)")
        return driver
    
    def reset_whatsapp_status(self):
        """Reset WhatsApp login status"""
        self.whatsapp_logged_in = False
    
    def is_whatsapp_logged_in(self):
        """Check if WhatsApp is logged in"""
        return self.whatsapp_logged_in
    
    def set_whatsapp_logged_in(self, status):
        """Set WhatsApp login status"""
        self.whatsapp_logged_in = status
    
    def cleanup(self):
        """Close WebDriver and cleanup"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None
            self.whatsapp_logged_in = False