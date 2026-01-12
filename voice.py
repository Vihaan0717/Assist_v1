# voice.py (Offline Mode)
import pyttsx3

def speak(text):
    print(f"🤖 Jarvis: {text}")
    
    # Initialize the offline engine
    engine = pyttsx3.init()
    
    # SETTINGS
    # Speed: 170 is a good conversational pace (Default is 200, which is too fast)
    engine.setProperty('rate', 170) 
    
    # Volume: 0.0 to 1.0
    engine.setProperty('volume', 1.0)

    # Voice Selection (Optional)
    # Windows usually has: [0] David (Male), [1] Zira (Female)
    voices = engine.getProperty('voices')
    
    # Try to find a female voice (usually clearer), otherwise use default
    try:
        engine.setProperty('voice', voices[1].id) 
    except:
        engine.setProperty('voice', voices[0].id)

    # Speak
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    speak("System voice switched to offline mode. Latency is now zero.")