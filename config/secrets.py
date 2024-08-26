from dotenv import load_dotenv
from pathlib import Path
import os

# Load environment variables from the .env file
load_dotenv()

# Retrieve API keys and MongoDB host from environment variables
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GROQ_BASE_URL = os.environ.get("GROQ_BASE_URL")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

MONGO_HOST = os.environ.get("MONGO_HOST")

# MongoDB configuration dictionary
MONGO_DB_CONFIG = {"host": MONGO_HOST, "db": "docai", "alias": "docai"}
