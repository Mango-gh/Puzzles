# Configuration file for API keys and settings
# Keep this file secure and never commit to git

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys
# Expect OPENAI_API_KEY to be provided via environment or .env file
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_APPS_SCRIPT_URL = os.getenv("GOOGLE_APPS_SCRIPT_URL", "https://script.google.com/macros/s/AKfycbwi-IALpYfQ7L9zJIsJdgnSfAMxoZFxVVPpBitPe-ENnzR0UapYaCsi8e92AdSTx13B/exec")

# Model settings
EMBEDDING_MODEL = "text-embedding-3-large"
EMBEDDING_DIMENSIONS = 3072  # text-embedding-3-large dimensions

# File paths
EMBEDDINGS_OUTPUT = "embeddings.jsonl"
FAISS_INDEX = "embeddings.index"
