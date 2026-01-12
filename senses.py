# senses.py
import cv2
import face_recognition
import speech_recognition as sr
import os
import numpy as np
import time
from PIL import Image
from ultralytics import YOLO # <--- NEW IMPORT

class Senses:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        
        # Audio Settings
        self.recognizer.pause_threshold = 2.0 
        self.recognizer.non_speaking_duration = 0.5 
        self.recognizer.dynamic_energy_threshold = True
        
        try:
            self.mic = sr.Microphone()
            print("✅ [Senses] Microphone connected.")
        except:
            print("⚠️ [Senses] No Microphone found.")
            self.mic = None

        # --- NEW: LOAD LOCAL AI MODEL ---
        print("🧠 [Senses] Loading Local Vision Model (YOLO)...")
        # 'yolov8n.pt' is the "Nano" model (Fastest for CPU)
        self.model = YOLO('yolov8n.pt') 

        self.known_face_encodings = []
        self.known_face_names = []
        self.load_owner_face()

    # ... (Keep load_owner_face and listen functions exactly the same) ...
    def load_owner_face(self):
        if os.path.exists("me.jpg"):
            try:
                img = cv2.imread("me.jpg")
                if img is None: return
                rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                rgb_img = np.array(rgb_img, dtype=np.uint8)
                encodings = face_recognition.face_encodings(rgb_img)
                if len(encodings) > 0:
                    self.known_face_encodings.append(encodings[0])
                    self.known_face_names.append("Boss") 
            except Exception:
                pass

    def listen(self, lang="en-IN"):
        if not self.mic: return ""
        
        lang_map = {"en-IN": "English", "te-IN": "Telugu", "hi-IN": "Hindi"}
        print(f"👂 Listening ({lang_map.get(lang, lang)})...")
        
        with self.mic as source:
            # Adjust for noise (Reduced duration to make it faster)
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            try:
                # TIMEOUTS ADDED TO PREVENT STUCK LOOP
                # timeout=5: If you say nothing for 5 seconds, it stops waiting.
                # phrase_time_limit=10: Stops recording after 10 seconds (prevents fan noise loop).
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
                print("⚡ processing...")
                command = self.recognizer.recognize_google(audio, language=lang)
                print(f"🗣️ You said: '{command}'")
                return command.lower()
            
            except sr.WaitTimeoutError:
                # This happens if you didn't say anything. We just return empty to loop again.
                return ""
            except sr.UnknownValueError:
                return ""
            except sr.RequestError:
                print("⚠️ [Error] Network Issue.")
                return ""
            except Exception as e:
                return ""

    def see(self):
        # (Keep your existing Face ID code)
        video_capture = cv2.VideoCapture(0)
        if not video_capture.isOpened(): return None
        found_person = None
        for i in range(5): 
            ret, frame = video_capture.read()
            if not ret: continue
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            try:
                face_locations = face_recognition.face_locations(rgb_frame)
                face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                    if True in matches:
                        found_person = "Boss"
                        break
            except: pass
            if found_person: break
        video_capture.release()
        return found_person

    # --- NEW: LOCAL OBJECT DETECTION ---
    def identify_objects_locally(self):
        """ Scans the room using Offline AI (YOLO) """
        video_capture = cv2.VideoCapture(0)
        if not video_capture.isOpened(): return []
        
        print("👀 Scanning environment (Offline)...")
        ret, frame = video_capture.read()
        video_capture.release()
        
        if not ret: return []

        # Run YOLO Inference (This is the magic line)
        results = self.model(frame, verbose=False) # verbose=False hides junk logs
        
        detected_items = []
        
        # Parse results
        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0]) # Get ID (e.g., 0)
                confidence = float(box.conf[0]) # Get Confidence (e.g., 0.85)
                
                # Only count if AI is >50% sure
                if confidence > 0.5:
                    item_name = self.model.names[class_id] # Convert 0 -> "Person"
                    detected_items.append(item_name)
        
        # Remove duplicates (e.g. don't say "cup, cup, cup")
        return list(set(detected_items))

    # (Keep take_snapshot for Gemini use later)
    def take_snapshot(self):
        video_capture = cv2.VideoCapture(0)
        if not video_capture.isOpened(): return None
        print("📸 Taking a picture...")
        ret, frame = video_capture.read()
        video_capture.release()
        if ret:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            return Image.fromarray(rgb_frame)
        return None