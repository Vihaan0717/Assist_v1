# main.py
from senses import Senses
from memory import MemorySystem
from mind import think
from voice import speak
from tools import SystemTools
from automation import SystemController
from vision_ui import HologramUI # <--- NEW IMPORT

def run_jarvis():
    print("🚀 [System] Initializing Jarvis...")
    
    senses = Senses()
    brain = MemorySystem()
    tools = SystemTools()
    sys_ops = SystemController()
    holo = HologramUI() # <--- NEW INITIALIZATION
    
    # Define this OUTSIDE the loop
    current_lang = "en-IN"
    
    speak("Systems online.", lang="en")

    user = senses.see()
    if user == "Boss":
        speak("Welcome back, Boss.", lang="en")
    
    while True:
        command = senses.listen(lang=current_lang)
        
        if command:
            # --- 0. LANGUAGE SWITCHING (UPDATED) ---
            
            # Switch to Telugu (English command OR Telugu command)
            if ("telugu" in command and "switch" in command) or \
               ("తెలుగు" in command): # Checks for Telugu script
                current_lang = "te-IN"
                speak("Changing language to Telugu.", lang="en")
                speak("నేను ఇప్పుడు తెలుగు వింటున్నాను.", lang="te")
                continue 
            
            # Switch to Hindi
            elif ("hindi" in command and "switch" in command) or \
                 ("हिंदी" in command):
                current_lang = "hi-IN"
                speak("Changing language to Hindi.", lang="en")
                speak("नमस्ते, अब मैं हिंदी सुन रहा हूँ.", lang="hi")
                continue

            # Switch to English (CRITICAL FIX: Checks for Telugu/Hindi script saying "English")
            elif ("english" in command) or \
                 ("ఇంగ్లీష్" in command) or \
                 ("అంగ్లం" in command) or \
                 ("अंग्रेजी" in command):
                current_lang = "en-IN"
                speak("Switching back to English.", lang="en")
                continue

            # --- 1. SYSTEM COMMANDS ---
            if "stop" in command or "exit" in command or "shutdown" in command or "ఆపు" in command:
                if current_lang == "en-IN":
                    speak("Powering down.", lang="en")
                else:
                    speak("వెళ్తున్నాను.", lang="te") 
                break
            
            # MEDIA CONTROLS
            elif "play" in command or "pause" in command or "stop music" in command:
                speak("Media control.", lang=current_lang)
                sys_ops.media_control("play")
                continue

            elif "next song" in command or "next track" in command:
                sys_ops.media_control("next")
                continue

            elif "previous song" in command:
                sys_ops.media_control("previous")
                continue

            elif "volume up" in command or "increase volume" in command:
                sys_ops.media_control("volume up")
                continue

            elif "volume down" in command or "decrease volume" in command:
                sys_ops.media_control("volume down")
                continue
            
            # --- 2. HANDS (Tools) ---
            # TIME
            elif "time" in command or "samayam" in command or "టైమ్" in command or "టైం" in command: 
                speak(f"Time is {tools.get_time()}", lang=current_lang)
                continue 

            # BATTERY
            elif "battery" in command or "charge" in command:
                speak(f"Power is {tools.get_battery()}", lang=current_lang)
                continue
            
            # WEATHER (Token-Free)
            elif "weather" in command or "climate" in command or "వాతావరణం" in command:
                speak("Checking report...", lang=current_lang)
                
                # Default City
                target_city = "Rajamahendravaram"
                
                # Extract City Name: "weather in Hyderabad" -> "Hyderabad"
                if " in " in command:
                    target_city = command.split(" in ")[1].strip()
                elif "lo " in command: # Telugu syntax "Hyderabad lo"
                    target_city = command.split(" lo ")[0].strip()
                
                report = tools.get_weather(target_city)
                speak(f"{target_city}: {report}", lang=current_lang)
                continue

            # NEWS (Token-Free)
            elif "news" in command or "headlines" in command or "వార్తలు" in command:
                speak("Fetching headlines...", lang=current_lang)
                news = tools.get_news()
                speak(f"Top stories: {news}", lang=current_lang)
                continue

            # --- VISION 1: LOCAL (FAST SCAN - YOLO) ---
            # Zero Gemini Tokens. Runs on CPU.
            elif ("scan" in command) or \
                 ("what is around" in command) or \
                 ("objects" in command) or \
                 ("ఇక్కడ ఏముంది" in command) or \
                 ("ఏమి ఉన్నాయి" in command): 
                
                speak("Scanning...", lang=current_lang)
                items = senses.identify_objects_locally()
                
                if items:
                    item_string = ", ".join(items)
                    if current_lang == "en-IN":
                        speak(f"I can see: {item_string}", lang="en")
                    elif current_lang == "te-IN":
                        speak(f"నాకు {item_string} కనిపిస్తున్నాయి.", lang="te")
                else:
                    speak("I don't see any objects I know.", lang=current_lang)
                continue

            # --- VISUAL INTERFACE ---
            elif ("visual mode" in command) or ("hologram" in command):
                speak("Launching AR Lab...", lang=current_lang)
                holo.start()
                speak("Lab closed.", lang=current_lang)
                continue

            # --- ANALYSIS COMMAND (NEW) ---
            # Triggers: "Analyze this model", "What do you think about my drawing"
            elif ("analyze this" in command) or ("check my project" in command):
                
                # Check if file exists
                import os
                if os.path.exists("project_analysis.jpg"):
                    speak("Analyzing your virtual project...", lang=current_lang)
                    
                    # Load the Saved AR Image
                    from PIL import Image
                    image_path = "project_analysis.jpg"
                    img = Image.open(image_path)
                    
                    # Ask Gemini
                    prompt = "I drew this in my AR lab. Analyze the structure, the 3D objects, and the drawing. Tell me what it looks like."
                    response = think(prompt, image_input=img)
                    speak(response, lang=current_lang)
                else:
                    speak("I don't see a project saved. Press 'S' in visual mode first.", lang=current_lang)
                continue

            # --- VISION 2: CLOUD (DESCRIPTION - GEMINI) ---
            elif ("describe" in command) or \
                 ("explain" in command) or \
                 ("వివరించు" in command) or \
                 ("చూడు" in command) or \
                 ("కన" in command): # <--- CHANGED: Catches "Kanapadu", "Kanabaduthundi", etc.
                
                speak("Looking...", lang=current_lang)
                photo = senses.take_snapshot()
                
                if photo:
                    lang_instruction = f" (Reply in {current_lang} language script)"
                    response = think(command + lang_instruction, image_input=photo)
                    speak(response, lang=current_lang)
                else:
                    speak("Camera error.", lang=current_lang)
                continue

            # [IMPORTANT] This must be BEFORE the Brain!
            elif ("open" in command) or ("launch" in command):
                app_name = command.replace("open", "").replace("launch", "").strip()
                speak(f"Opening {app_name}...", lang=current_lang)
                sys_ops.open_app(app_name)
                continue

            elif ("close" in command) and ("window" not in command):
                app_name = command.replace("close", "").strip()
                speak(f"Closing {app_name}...", lang=current_lang)
                sys_ops.close_app(app_name)
                continue

            elif ("type" in command) or ("write" in command):
                text_to_type = command.replace("type", "").replace("write", "").strip()
                speak("Typing...", lang=current_lang)
                sys_ops.type_text(text_to_type)
                continue
            
            elif "screenshot" in command:
                speak("Taking screenshot.", lang=current_lang)
                sys_ops.take_screenshot()
                speak("Saved.", lang=current_lang)
                continue

            # --- 3. BRAIN (Thinking) ---
            context = brain.retrieve_context(command)
            if context == "No memory found.":
                context = "" 

            # --- FIX FOR HINDI MIXING ---
            # We create a STRICT instruction based on the current mode
            if current_lang == "en-IN":
                lang_instruction = " (STRICTLY reply in English only)"
            elif current_lang == "te-IN":
                lang_instruction = " (STRICTLY reply in Telugu language script only)"
            elif current_lang == "hi-IN":
                lang_instruction = " (STRICTLY reply in Hindi language script only)"
            
            # Send command + strict instruction
            response = think(command + lang_instruction, context_text=context)
            
            # Error check
            if "unable to process" in response:
                if current_lang == "te-IN":
                    speak("క్షమించండి, సర్వర్ బిజీగా ఉంది.", lang="te")
                else:
                    speak("My brain is tired. Please wait a moment.", lang="en")
            else:
                speak(response, lang=current_lang)
            
            if "remember" in command:
                fact = command.replace("remember", "").strip()
                brain.save_memory("general", fact)
                speak("Memory saved.", lang=current_lang)

if __name__ == "__main__":
    run_jarvis()