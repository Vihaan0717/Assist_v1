# mind.py
import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash') 

def think(user_text, context_text=""):
    try:
        # --- FIXED SYSTEM PROMPT ---
        system_instruction = """
        You are J.A.R.V.I.S., an advanced AI assistant.
        
        RULES:
        1. LANGUAGE: You are TRILINGUAL. You speak English, Telugu, and Hindi fluently.
           - If the user speaks Telugu, reply in Telugu Script.
           - If the user speaks Hindi, reply in Hindi Script.
           - If the user speaks English, reply in English.
        
        2. PERSONALITY: Witty, efficient, and brief (1-2 sentences max). Call the user "Boss".
        
        3. MEMORY: IGNORE the provided memory context unless the user specifically asks for it or it is critical to the current topic.
        """

        prompt = f"""
        {system_instruction}
        
        RELEVANT MEMORY (Use only if needed): {context_text}
        
        USER SAID: {user_text}
        
        YOUR RESPONSE:
        """
        
        response = model.generate_content(prompt)
        clean_text = response.text.replace("*", "").replace("#", "").strip()
        return clean_text
        
    except Exception as e:
        print(f"⚠️ [Mind Error] {e}")
        return "I am unable to process that request at the moment, Sir."