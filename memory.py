# memory.py
import chromadb
from chromadb.utils import embedding_functions
import uuid
import os
from config import DB_PATH

class MemorySystem:
    def __init__(self):
        # 1. Initialize the Database
        print("🧠 [Init] Connecting to Brain...")
        self.client = chromadb.PersistentClient(path=DB_PATH)
        
        # 2. Force usage of the Local Model (SentenceTransformers)
        # We explicitly tell it to use the model we downloaded in setup_brain.py
        print("🔌 [Init] Loading Offline Engine...")
        self.embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        
        # 3. Create/Get the Collection
        self.facts_collection = self.client.get_or_create_collection(
            name="facts",
            embedding_function=self.embed_fn
        )
        print("✅ [Init] Brain is Online.")
        
    def save_memory(self, category, text):
        print(f"📝 [Memory] Processing: '{text}'")
        try:
            # Check for duplicates
            existing = self.facts_collection.query(query_texts=[text], n_results=1)
            if existing['documents'] and existing['distances'][0][0] < 0.3:
                print(f"   ↳ 🛑 I already know this.")
                return "Already in memory."
        except Exception:
            pass # Ignore errors on first run

        # Save new info
        self.facts_collection.add(
            documents=[text],
            metadatas=[{"category": category}],
            ids=[str(uuid.uuid4())]
        )
        print(f"   ↳ 💾 Saved to database.")
        return "Memory saved."

    def retrieve_context(self, query_text):
        print(f"🔍 [Search] Looking for: '{query_text}'")
        results = self.facts_collection.query(query_texts=[query_text], n_results=1)
        if results['documents'] and results['documents'][0]:
             answer = results['documents'][0][0]
             print(f"   ↳ 💡 Found: {answer}")
             return answer
        return "No memory found."

if __name__ == "__main__":
    # Test the system
    brain = MemorySystem()
    brain.save_memory("health", "The user is allergic to peanuts.")
    brain.retrieve_context("Can I eat peanuts?")