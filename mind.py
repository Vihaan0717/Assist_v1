# mind.py
import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

# Use the 2.0-flash model (It can see images!)
model = genai.GenerativeModel('gemini-2.0-flash') 

def think(user_text, context_text="", image_input=None):
    try:
        # System Instructions
        system_instruction = """
        You are J.A.R.V.I.S., an advanced AI assistant.
        RULES:
        1. LANGUAGE: Trilingual (English, Telugu, Hindi). Match the user's script.
        2. PERSONALITY: Witty, efficient, brief (1-2 sentences).
        3. VISION: If an image is provided, describe what you see in it relevant to the user's question.
        """

        # Prepare the input list (Text + Image if available)
        input_content = [system_instruction]
        
        if context_text:
            input_content.append(f"MEMORY: {context_text}")
        
        input_content.append(f"USER SAID: {user_text}")
        
        # This is the part that handles the photo
        if image_input:
            input_content.append(image_input) # Add the actual image data
            input_content.append("INSTRUCTION: Analyze this image based on the user's question.")

        # Generate content
        response = model.generate_content(input_content)
        
        # Clean up response
        clean_text = response.text.replace("*", "").replace("#", "").strip()
        return clean_text
        
    except Exception as e:
        print(f"⚠️ [Mind Error] {e}")
        return "I am unable to see that clearly, Sir."

# Test it independently
if __name__ == "__main__":
    print(think("System check."))