# Configuration file for API keys and settings
# Keep this file secure and never commit to git

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("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")
GOOGLE_APPS_SCRIPT_URL = os.getenv("GOOGLE_APPS_SCRIPT_URL", "https://script.google.com/macros/s/AKfycbwi-IALpYfQ7L9zJIsJdgnSfAMxoZFxVVPpBitPe-ENnzR0UapYaCsi8e92AdSTx13B/exec")

# Model settings
EMBEDDING_MODEL = "text-embedding-3-large"
EMBEDDING_DIMENSIONS = 3072  # text-embedding-3-large dimensions

# File paths
EMBEDDINGS_OUTPUT = "embeddings.jsonl"
FAISS_INDEX = "embeddings.index"
