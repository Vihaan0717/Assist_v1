# setup_brain.py
import shutil
import os
from sentence_transformers import SentenceTransformer

print("🛠️  STARTING JARVIS BRAIN REPAIR...")

# 1. Delete the corrupted database
if os.path.exists("memory_db"):
    try:
        shutil.rmtree("memory_db")
        print("✅ Deleted corrupted 'memory_db' folder.")
    except Exception as e:
        print(f"❌ Could not delete memory_db: {e}")

# 2. Delete the broken cache files (The ones causing the timeout)
user_path = os.path.expanduser("~")
chroma_cache = os.path.join(user_path, ".cache", "chroma")
if os.path.exists(chroma_cache):
    try:
        shutil.rmtree(chroma_cache)
        print("✅ Deleted broken download cache.")
    except Exception as e:
        print(f"⚠️  Could not delete cache (might be empty): {e}")

# 3. Pre-download the Brain Model (Using the FAST library)
print("\n⬇️  Downloading the AI Brain Model (approx 90MB)...")
print("   (This uses your new fast library. Please wait...)")

try:
    # This forces the download to happen NOW, with a progress bar
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print("\n🎉 SUCCESS! The Brain Model is downloaded and ready.")
except Exception as e:
    print(f"\n❌ Download failed: {e}")
    print("   Check your internet connection.")