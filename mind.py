# mind.py
import google.generativeai as genai
from config import GEMINI_API_KEY

# Configure the API
genai.configure(api_key=GEMINI_API_KEY)

# Use the fast, free model
model = genai.GenerativeModel('models/gemini-flash-latest')

def think(user_text, context_text=""):
    """
    Sends text to Gemini with a 'Personality' filter.
    """
    try:
        # THE PERSONALITY UPGRADE
        # We tell the AI exactly how to behave.
        system_instruction = """
        You are J.A.R.V.I.S., an advanced AI assistant created by the Boss.
        Your personality is: Witty, sarcasm-capable, highly efficient, and briefly spoken.
        
        RULES:
        1. Keep answers SHORT (max 1-2 sentences). You are a voice assistant, not a book.
        2. Call the user "Boss" or "Sir".
        3. If the user asks about personal preferences, be charmingly robotic.
        4. ONLY mention memory/context if it is directly relevant to the user's current question.
        """

        prompt = f"""
        {system_instruction}
        
        RELEVANT MEMORY (Use only if needed):
        {context_text}
        
        USER SAID:
        {user_text}
        
        YOUR RESPONSE:
        """
        
        response = model.generate_content(prompt)
        
        # Clean up text (remove * or # symbols that mess up the voice)
        clean_text = response.text.replace("*", "").replace("#", "").strip()
        return clean_text
        
    except Exception as e:
        print(f"⚠️ [Mind Error] {e}")
        return "I am unable to process that request at the moment, Sir."

if __name__ == "__main__":
    print(think("Who are you?"))