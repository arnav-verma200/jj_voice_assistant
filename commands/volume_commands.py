"""
Volume control commands using hand gestures
"""

import mediapipe as mp
import cv2
import math as m
import threading
from config import Config
from utils.tts import speak

# Try pycaw first, fallback to system commands
try:
    from ctypes import cast, POINTER
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    import pythoncom
    USE_PYCAW = True
except Exception as e:
    print(f"⚠️ pycaw import failed: {e}")
    USE_PYCAW = False

# Windows native volume control fallback
import subprocess
import platform


class VolumeCommands:
    """Handle volume control using hand gestures"""
    
    def __init__(self):
        self.controller = None
        self.control_thread = None
    
    def start_volume_control(self):
        """Start the volume control in a separate thread"""
        input_mode = Config.get_input_mode()
        
        if self.control_thread is None or not self.control_thread.is_alive():
            msg = "🎵 Starting volume control..."
            if input_mode == "voice_continuous":
                speak("Starting volume control")
            else:
                print(msg)
            
            print("💡 TIP: Volume control uses your webcam - pinch thumb and index finger!")
            
            self.controller = VolumeController()
            if self.controller.initialized:
                self.control_thread = threading.Thread(
                    target=self.controller.run, 
                    daemon=True
                )
                self.control_thread.start()
            else:
                msg = "❌ Failed to initialize volume controller"
                if input_mode == "voice_continuous":
                    speak("Failed to initialize volume control")
                else:
                    print(msg)
        else:
            msg = "⚠️ Volume control is already running"
            if input_mode == "voice_continuous":
                speak("Volume control is already running")
            else:
                print(msg)
    
    def stop_volume_control(self):
        """Stop the volume control"""
        input_mode = Config.get_input_mode()
        
        if self.control_thread and self.control_thread.is_alive():
            if self.controller:
                self.controller.stop()
            msg = "🛑 Stopping volume control..."
            if input_mode == "voice_continuous":
                speak("Stopping volume control")
            else:
                print(msg)
            self.control_thread.join(timeout=2)
        else:
            msg = "⚠️ Volume control is not running"
            if input_mode == "voice_continuous":
                speak("Volume control is not running")
            else:
                print(msg)


class VolumeController:
    """Internal volume controller with hand gesture recognition"""
    
    def __init__(self):
        self.smooth_vol = 0.5
        self.smoothing_factor = 0.1
        self.is_running = False
        self.initialized = False
        self.use_pycaw = False
        
        # Try to initialize pycaw with multiple methods
        if USE_PYCAW:
            try:
                # Method 1: Standard approach
                pythoncom.CoInitialize()
                devices = AudioUtilities.GetSpeakers()
                interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                self.volume = cast(interface, POINTER(IAudioEndpointVolume))
                self.smooth_vol = self.volume.GetMasterVolumeLevelScalar()
                self.use_pycaw = True
                self.initialized = True
                print("✅ Audio initialized with pycaw")
            except AttributeError:
                # Method 2: Try alternative pycaw method
                try:
                    pythoncom.CoInitialize()
                    from pycaw.api.audioclient import IMMDevice
                    devices = AudioUtilities.GetSpeakers()
                    
                    # Get the IMMDevice interface
                    if hasattr(devices, '_dev'):
                        device = devices._dev
                    else:
                        device = devices
                    
                    interface = device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                    self.volume = cast(interface, POINTER(IAudioEndpointVolume))
                    self.smooth_vol = self.volume.GetMasterVolumeLevelScalar()
                    self.use_pycaw = True
                    self.initialized = True
                    print("✅ Audio initialized with pycaw (alternative method)")
                except Exception as e2:
                    print(f"⚠️ pycaw alternative method failed: {e2}")
                    print("✅ Volume control will work in visual-only mode")
                    self.initialized = True
                    self.use_pycaw = False
            except Exception as e:
                print(f"⚠️ pycaw initialization failed: {e}")
                print("✅ Volume control will work in visual-only mode")
                self.initialized = True
                self.use_pycaw = False
        else:
            print("✅ Volume control running in visual-only mode")
            self.initialized = True
    
    def run(self):
        """Main volume control loop"""
        if not self.initialized:
            print("❌ Volume controller not initialized")
            return
        
        # IMPORTANT: Initialize COM in this thread
        if USE_PYCAW:
            try:
                pythoncom.CoInitialize()
            except:
                pass
        
        self.is_running = True
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("❌ Cannot access webcam")
            return
        
        mphands = mp.solutions.hands
        hands = mphands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        mpdraw = mp.solutions.drawing_utils
        
        # Window properties for corner placement
        window_name = "Gesture Volume Control"
        cv2.namedWindow(window_name)
        cv2.moveWindow(window_name, 50, 50)
        
        print("✅ Volume control started!")
        print("   👉 Pinch thumb and index finger to adjust volume")
        print("   👉 Press 'Q' to quit or say 'stop volume'\n")
        
        while self.is_running:
            suc, frame = cap.read()
            if not suc:
                break
            
            frame = cv2.flip(frame, 1)
            frame = cv2.GaussianBlur(frame, (5, 5), 0)
            
            # Resize for corner window (35% of original size)
            sf = 0.35
            h, w = frame.shape[:2]
            h2 = int(h * sf)
            w2 = int(w * sf)
            frame = cv2.resize(src=frame, dsize=(w2, h2), interpolation=cv2.INTER_CUBIC)
            
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(frame_rgb)
            
            # Semi-transparent white background for text
            overlay = frame.copy()
            cv2.rectangle(overlay, (0, 0), (w2, 55), (255, 255, 255), -1)
            cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)
            
            # Get current volume
            if self.use_pycaw:
                try:
                    current_vol = self.volume.GetMasterVolumeLevelScalar()
                except:
                    current_vol = self.smooth_vol
            else:
                current_vol = self.smooth_vol
            
            vol_percent = int(current_vol * 100)
            # Blue text exactly like your image
            cv2.putText(frame, f"Volume: {vol_percent}%", (10, 35),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
            
            if results.multi_hand_landmarks:
                for handlms in results.multi_hand_landmarks:
                    # Draw hand landmarks - white lines, red dots
                    mpdraw.draw_landmarks(
                        frame,
                        handlms,
                        mphands.HAND_CONNECTIONS,
                        mpdraw.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=4),
                        mpdraw.DrawingSpec(color=(255, 255, 255), thickness=2)
                    )
                    
                    llm = []
                    for id, lm in enumerate(handlms.landmark):
                        h, w, _ = frame.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        llm.append([id, cx, cy])
                    
                    # Blue line between thumb (4) and index finger (8)
                    cv2.line(frame, (llm[4][1], llm[4][2]), (llm[8][1], llm[8][2]), (255, 0, 0), 3)
                    
                    # Red circles on fingertips
                    cv2.circle(frame, (llm[4][1], llm[4][2]), 8, (0, 0, 255), -1)
                    cv2.circle(frame, (llm[8][1], llm[8][2]), 8, (0, 0, 255), -1)
                    
                    # Calculate distance
                    dist = m.sqrt(((llm[4][1] - llm[8][1])**2) + ((llm[4][2] - llm[8][2])**2))
                    
                    min_dist = 20
                    max_dist = 180
                    
                    vol = (dist - min_dist) / (max_dist - min_dist)
                    vol = max(0.0, min(1.0, vol))
                    
                    self.smooth_vol = self.smooth_vol + (vol - self.smooth_vol) * self.smoothing_factor
                    
                    # Set volume using available method
                    if self.use_pycaw:
                        try:
                            self.volume.SetMasterVolumeLevelScalar(self.smooth_vol, None)
                        except Exception as e:
                            print(f"❌ Error setting volume: {e}")
                    else:
                        # Fallback: Use Windows native volume control
                        self._set_system_volume(self.smooth_vol)
            else:
                cv2.putText(frame, "Show your hand!", (10, 35),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            
            # Bottom instruction bar
            cv2.rectangle(frame, (0, h2 - 30), (w2, h2), (0, 0, 0), -1)
            cv2.putText(frame, "Press 'Q' to quit", (10, h2 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
            
            cv2.imshow(window_name, frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("🛑 Volume control stopped (pressed 'Q')")
                break
        
        cap.release()
        cv2.destroyAllWindows()
        hands.close()
        self.is_running = False
    
    def stop(self):
        """Stop the volume control"""
        self.is_running = False
    
    def _set_system_volume(self, volume_level):
        """Set volume using Windows native commands (fallback method)"""
        try:
            if platform.system() == "Windows":
                # Use nircmd if available, otherwise it's visual-only
                volume_percent = int(volume_level * 100)
                # Try to use nircmd (needs to be installed separately)
                try:
                    subprocess.run(
                        ['nircmd.exe', 'setsysvolume', str(int(volume_level * 65535))],
                        capture_output=True,
                        timeout=1
                    )
                except FileNotFoundError:
                    # nircmd not available, running in visual-only mode
                    pass
        except Exception:
            pass