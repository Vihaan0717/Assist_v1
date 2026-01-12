# voice.py
import pyttsx3
import asyncio
import edge_tts
import os
from playsound import playsound

# --- VOICE SETTINGS ---
# Telugu: Female (Clear & Sharp)
TELUGU_VOICE = "te-IN-ShrutiNeural" 
# Hindi: Female
HINDI_VOICE = "hi-IN-SwaraNeural"

def speak_offline(text):
    """ Fast, robotic English voice (Male) """
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 160) # Speed
        
        # FORCE MALE VOICE
        # Windows voices: [0] = Male (David), [1] = Female (Zira)
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id) 
        
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"⚠️ Offline Voice Error: {e}")

async def speak_online(text, lang="te"):
    """ High-quality Neural voice (Female) """
    voice = TELUGU_VOICE if lang == "te" else HINDI_VOICE
    output_file = "voice_out.mp3"
    
    try:
        # 1. Delete old file
        if os.path.exists(output_file):
            try:
                os.remove(output_file)
            except:
                pass 

        # 2. Generate Audio
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_file)
        
        # 3. Play (Crystal Clear)
        playsound(output_file)
        
        # 4. Cleanup
        try:
            os.remove(output_file)
        except:
            pass

    except Exception as e:
        print(f"⚠️ Voice Error: {e}")

def speak(text, lang="en"):
    print(f"🤖 Jarvis: {text}")
    
    # Detect Language
    is_telugu = any('\u0c00' <= char <= '\u0c7f' for char in text)
    is_hindi = any('\u0900' <= char <= '\u097f' for char in text)
    
    if is_telugu or lang == "te":
        asyncio.run(speak_online(text, "te")) # Female
    elif is_hindi or lang == "hi":
        asyncio.run(speak_online(text, "hi")) # Female
    else:
        speak_offline(text) # Male

# TEST
if __name__ == "__main__":
    speak("Hello Boss. I am back to my male voice for English.")
    speak("నమస్కారం అండి, నేను తెలుగులో మాట్లాడుతున్నాను.", lang="te")