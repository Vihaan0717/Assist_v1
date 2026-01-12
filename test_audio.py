# test_audio.py
import asyncio
import edge_tts

# We'll try the "Aria" voice this time, it's often clearer than Christopher
VOICE = "en-US-AriaNeural"
OUTPUT_FILE = "debug_voice.mp3"

async def create_file():
    print(f"⬇️ Generating '{OUTPUT_FILE}'...")
    communicate = edge_tts.Communicate("Hello Boss. This is a test of my audio clarity.", VOICE)
    await communicate.save(OUTPUT_FILE)
    print("✅ File created successfully!")
    print(f"👉 Please go to your folder and double-click '{OUTPUT_FILE}' to play it.")

if __name__ == "__main__":
    asyncio.run(create_file())