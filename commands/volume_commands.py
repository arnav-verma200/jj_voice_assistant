"""
Volume control commands using hand gestures
"""

import mediapipe as mp
import cv2
import math as m
import threading
from config import Config
from utils.tts import speak
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import pythoncom


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
            self.control_thread = threading.Thread(
                target=self.controller.run, 
                daemon=True
            )
            self.control_thread.start()
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
        self.smooth_vol = 0
        self.smoothing_factor = 0.1
        self.is_running = False
    
    def run(self):
        """Main volume control loop"""
        # Initialize COM in this thread
        pythoncom.CoInitialize()
        
        # Get speakers - this returns a POINTER
        speakers = AudioUtilities.GetSpeakers()
        # Activate returns the interface directly
        interface = speakers.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        
        self.is_running = True
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("❌ Cannot access webcam")
            return
        
        mphands = mp.solutions.hands
        hands = mphands.Hands(4)
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
            sf = 0.5
            h, w = frame.shape[:2]
            h2 = int(h * sf)
            w2 = int(w * sf)
            frame = cv2.resize(src=frame, dsize=(w2, h2), interpolation=cv2.INTER_CUBIC)
            
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(frame_rgb)
            
            if results.multi_hand_landmarks:
                for handlms in results.multi_hand_landmarks:
                    mpdraw.draw_landmarks(frame, handlms, mphands.HAND_CONNECTIONS)
                    
                    llm = []
                    
                    for id, lm in enumerate(handlms.landmark):
                        h, w, _ = frame.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        llm.append([id, cx, cy])
                    
                    cv2.line(frame, (llm[4][1], llm[4][2]), (llm[8][1], llm[8][2]), (255, 0, 0), 2)
                    dist = m.sqrt(((llm[4][1] - llm[8][1])**2) + ((llm[4][2] - llm[8][2])**2))
                    
                    min_dist = 15
                    max_dist = 150
                    
                    vol = (dist - min_dist) / (max_dist - min_dist)
                    vol = max(0.0, min(1.0, vol))
                    
                    self.smooth_vol = self.smooth_vol + (vol - self.smooth_vol) * self.smoothing_factor
                    
                    volume.SetMasterVolumeLevelScalar(self.smooth_vol, None)
                    cv2.putText(frame, f"Volume: {int(self.smooth_vol * 100)}%", (50, 100),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 23), 2)
            
            cv2.imshow(window_name, frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("🛑 Volume control stopped (pressed 'Q')")
                break
        
        cap.release()
        cv2.destroyAllWindows()
        self.is_running = False
    
    def stop(self):
        """Stop the volume control"""
        self.is_running = False