"""
Configuration management for the project.
Handles API keys and model settings.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")  # Optional, kept for future use

# Validate required keys
if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not set. Put it in a .env file or set it as an environment variable."
    )

# Set HF token for huggingface_hub if provided (optional)
if HF_TOKEN:
    os.environ["HUGGINGFACE_HUB_TOKEN"] = HF_TOKEN

# Model Configuration
GEMINI_MODEL = "gemini-2.5-flash"

# Humanization Settings
DEFAULT_P_SYN = 1.0  # Synonym replacement probability
DEFAULT_P_TRANS = 1.0  # Academic transition probability
