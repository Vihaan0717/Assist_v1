# main.py
from senses import Senses
from memory import MemorySystem
from mind import think
from voice import speak
from tools import SystemTools 

def run_jarvis():
    print("🚀 [System] Initializing Jarvis...")
    
    senses = Senses()
    brain = MemorySystem()
    tools = SystemTools()
    
    speak("System upgraded. Web drivers active.")

    # Face Check
    user = senses.see()
    if user == "Boss":
        speak("Welcome back, Boss.")
    
    while True:
        command = senses.listen()
        
        if command:
            # --- 1. SYSTEM ---
            if "stop" in command or "exit" in command or "shutdown" in command:
                speak("Powering down. Goodbye.")
                break
            
            # --- 2. THE HANDS (Tools) ---
            elif "time" in command:
                speak(f"It is {tools.get_time()}")
                continue 

            elif "battery" in command:
                speak(f"Power levels are at {tools.get_battery()}")
                continue

            elif "open" in command:
                app_name = command.replace("open", "").strip()
                speak(f"Opening {app_name}")
                tools.open_app(app_name)
                continue

            # NEW: MEDIA (YouTube)
            elif "play" in command:
                song = command.replace("play", "").strip()
                speak(f"Playing {song}")
                tools.play_video(song)
                continue

            # NEW: RESEARCH (Google)
            elif "search" in command or "google" in command:
                topic = command.replace("search", "").replace("google", "").strip()
                speak(f"Searching for {topic}")
                tools.search_google(topic)
                continue

            # --- 3. THE BRAIN (Thinking) ---
            context = brain.retrieve_context(command)
            if context == "No memory found.":
                context = "" 

            response = think(command, context_text=context)
            speak(response)
            
            if "remember" in command:
                fact = command.replace("remember", "").strip()
                brain.save_memory("general", fact)
                speak("Memory saved.")

if __name__ == "__main__":
    run_jarvis()