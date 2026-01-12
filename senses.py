# senses.py
import cv2
import face_recognition
import speech_recognition as sr
import os
import numpy as np
import time

class Senses:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        
        # --- PATIENCE SETTINGS ---
        # 1. Wait 2 full seconds of silence before deciding you are done
        self.recognizer.pause_threshold = 2.0 
        
        # 2. Don't cut off if you speak softly for a split second
        self.recognizer.non_speaking_duration = 0.5 
        
        # 3. Dynamic sensitivity (Adjusts to your room automatically)
        self.recognizer.dynamic_energy_threshold = True
        
        try:
            self.mic = sr.Microphone()
            print("✅ [Senses] Microphone connected.")
        except:
            print("⚠️ [Senses] No Microphone found.")
            self.mic = None

        self.known_face_encodings = []
        self.known_face_names = []
        self.load_owner_face()

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
            # Listen to background noise for 1 second (longer = better accuracy)
            self.recognizer.adjust_for_ambient_noise(source, duration=1.0)
            
            try:
                # timeout=None: Wait forever for you to START speaking
                # phrase_time_limit=None: Let you speak for as long as you want
                audio = self.recognizer.listen(source, timeout=None, phrase_time_limit=None)
                print("⚡ processing...")
                
                command = self.recognizer.recognize_google(audio, language=lang)
                print(f"🗣️ You said: '{command}'")
                return command.lower()
            
            except sr.WaitTimeoutError:
                return ""
            except sr.UnknownValueError:
                # print("⚠️ Unclear") # Muted to keep logs clean
                return ""
            except sr.RequestError:
                print("⚠️ [Error] Network Issue.")
                return ""
            except Exception as e:
                return ""

    def see(self):
        video_capture = cv2.VideoCapture(0)
        if not video_capture.isOpened(): return None
        found_person = None
        # Reduced frames to 5 for faster startup
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