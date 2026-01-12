# senses.py
import cv2
import face_recognition
import speech_recognition as sr
import os
import numpy as np
import time

class Senses:
    def __init__(self):
        # 1. Setup Ears (Microphone)
        self.recognizer = sr.Recognizer()
        try:
            self.mic = sr.Microphone()
        except:
            print("⚠️ [Senses] No Microphone found.")
            self.mic = None

        # 2. Setup Eyes (Load your face)
        self.known_face_encodings = []
        self.known_face_names = []
        self.load_owner_face()

    def load_owner_face(self):
        """ Loads 'me.jpg' safely using OpenCV. """
        if os.path.exists("me.jpg"):
            print("👁️ [Senses] Loading your face data...")
            try:
                img = cv2.imread("me.jpg")
                if img is None: return
                rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                rgb_img = np.array(rgb_img, dtype=np.uint8)
                encodings = face_recognition.face_encodings(rgb_img)
                if len(encodings) > 0:
                    self.known_face_encodings.append(encodings[0])
                    self.known_face_names.append("Boss") 
                    print("✅ [Senses] Face learned successfully.")
            except Exception as e:
                print(f"⚠️ [Senses] Error loading 'me.jpg': {e}")
        else:
            print("⚠️ [Senses] 'me.jpg' not found.")

    def listen(self):
        """ Listens for 5 seconds """
        if not self.mic: return ""
        print("👂 Listening...")
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source)
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                command = self.recognizer.recognize_google(audio)
                print(f"🗣️ You said: '{command}'")
                return command.lower()
            except:
                return ""

    def see(self):
        """ Checks camera for 3 seconds to find a face """
        video_capture = cv2.VideoCapture(0)
        if not video_capture.isOpened():
            return None

        print("👀 Looking for you (Hold still)...")
        found_person = None

        # LOOP: Try 15 times (approx 3 seconds)
        for i in range(15):
            ret, frame = video_capture.read()
            if not ret: continue

            # Convert to RGB & Integers
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            rgb_frame = np.array(rgb_frame, dtype=np.uint8)
            
            # Look for faces
            try:
                face_locations = face_recognition.face_locations(rgb_frame)
                face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                    if True in matches:
                        found_person = "Boss"
                        break # Stop looking if we found you!
            except:
                pass
            
            if found_person:
                break
            
            # Wait a tiny bit before next check
            time.sleep(0.1)
        
        video_capture.release()
        return found_person

if __name__ == "__main__":
    sense = Senses()
    
    # Test Eyes
    person = sense.see()
    print(f"📸 Result: I saw {person}")
    
    # Test Ears
    text = sense.listen()