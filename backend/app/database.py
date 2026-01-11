import os
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client

# Load .env from the backend directory (parent of app/)
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError(
        f"Missing SUPABASE_URL or SUPABASE_KEY in environment variables. "
        f"Looked for .env at: {env_path}"
    )

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)